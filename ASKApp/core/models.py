from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver 
from django.db.models.signals import post_save
from PIL import Image 


class Skill(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', default='blank_image.png')
    skills = models.ManyToManyField(Skill, through='SkillRate')
    bio = models.TextField(max_length=200, default='', blank=False)

    def __str__(self):
        return f'{self.user.first_name} Profile'
    
    def update(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)
            
@receiver(post_save, sender=User)
def save_profile(sender,instance, created, **kwargs):

    print('instance',instance)
    user = instance

    if created:
        profile = Profile(user = user)
        profile.save()
        

class SkillRate(models.Model):
   author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
   skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True)
   #rate = models.IntegerField(default=0)
   @property
   def rate(self):
        # Calculate the average rate of answers for the profile on questions with this skill
        if self.author and self.skill:
            related_answers = Answers.objects.filter(
                author=self.author,
                question__skills=self.skill
            )
            total_rate = sum(answer.rate for answer in related_answers)
            count = related_answers.count()
            average_rate = total_rate / count if count else 0
            return average_rate
        else:
            return 0
   

class Questions(models.Model):
   question_text = models.TextField(blank=False, null=False)
   author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
   is_anonymous = models.BooleanField(default=False)
   is_answered = models.BooleanField(default=False)
   created_at = models.DateTimeField(auto_now_add=True) #todo asked at in Front-End
   skills = models.ManyToManyField(Skill, blank=False)
   def __str__(self):
        return f'{self.question_text[:10]}...'
 
   
class Answers(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    answer_text = models.TextField(blank=False, null=False)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    up_vote = models.ManyToManyField(Profile, related_name='answers_voted_up',blank=False)
    down_vote = models.ManyToManyField(Profile, related_name='answers_voted_down',blank=False)
    @property
    def rate(self):
        up_votes_count = self.up_vote.filter(answer=self).count()
        down_votes_count = self.down_vote.filter(answer=self).count()
        rate = up_votes_count - down_votes_count
        return rate
    
    def __str__(self):
        return f'{self.answer_text[:10]}...' 

class Notification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE)  # Change to ForeignKey
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=Answers)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification for the user who asked the question
        question_text = instance.question.question_text
        Notification.objects.create(
            profile=instance.author,
            message=f"Your question '{question_text}' has a new answer.",
            answer=instance
        )
