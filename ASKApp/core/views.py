from xmlrpc.client import DateTime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import  *
from django.utils import timezone
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.hashers import make_password
from .models import Profile, Skill, Questions, Answers, Notification
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from GogoBot.NaiveBayesEnhanced import NaiveBayes


def identify(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        newpassword = request.POST['password']
        Cnewpassword = request.POST['Cpassword']

        if User.objects.filter(email = email, username = username).exists():
            if newpassword == Cnewpassword:
                edituser = User.objects.get(username = username)
                edituser.set_password(newpassword)
                edituser.save()
                messages.success(request, 'Password resets successfully')
                return redirect('core:login')
            else:
                messages.error(request, 'Password not Matching')
                return redirect('core:identify')
        else:
            messages.error(request, 'User doesn\'t exists')
            return redirect('core:identify')
    else:
        return render(request, 'register/identify.html', {'title': 'Reset Password'})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            #form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('core:login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'title': 'Register',
    }

    return render(request, 'register/signup.html', context)


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:home')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('core:login_view')


@login_required
def profile(request, id):
    try:
        user = User.objects.get(id=id)
        profile = Profile.objects.get(user=user)
        skills = SkillRate.objects.filter(author=profile)
        
        # Dictionary to store skills,
        # rate and total answers of each skill
        skills_rates = {}
        for skill_rate in skills:
            skill = skill_rate.skill
            rate = skill_rate.rate

            total_answers = Answers.objects.filter(author=profile, question__skills=skill).count()

            skills_rates[skill.name] = {
                'rate': rate,
                'total_answers': total_answers
            }
        questions = Questions.objects.filter(author = profile)

            
        context = {
            'user': user,
            'profile': profile,
            'skills_rates': skills_rates,
            'questions' : questions
        }

        if request.method == 'GET':
            return render(request, 'profile/profile.html', context)

        elif request.method == 'POST':
            # Check if the user making the request is the owner of the profile
            if request.user != user:
                messages.success(request, 'You can not update this profile')
                return render(request, 'profile/profile.html', context)

            user_form = UserUpdateForm(request.POST, instance=user)
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your account has been updated!')
                
                # Render the profile page with the updated information
                context = {
                    'user': user,
                    'profile': profile,
                    'skills_rates': skills_rates,
                }
                return render(request, 'profile/profile.html', context)
                
            else:
                messages.error(request, 'Invalid form data. Please check your inputs.')

                # Redirect to the profile page with the original information
                context = {
                    'user': user,
                    'profile': profile,
                    'skills_rates': skills_rates,
                }
                return render(request, 'profile/profile.html', context)

    except User.DoesNotExist:
        # Return a 404 page for non-existing user
        return render(request, '404.html', status=404)

    except Profile.DoesNotExist:
        # Return a 404 page for non-existing profile
        return render(request, '404.html', status=404)

    except Http404 as e:
        # Return a 404 page for the user is not the owner of the profile
        context = {'message': str(e)}
        return render(request, '404.html', context, status=404)
'''
    except Exception as e:
        # Return a generic error page for other exceptions that might occur
        context = {'error_message': str(e)}
        return render(request, '500.html', context, status=500)'''
    
    
@login_required
def ask(request):
    if request.method == 'POST':
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            form = AskQuestionForm(request.POST)

            # Validate the form
            if form.is_valid():
                question_text = form.cleaned_data['question_text']

                # Create the question
                question = Questions.objects.create(
                    author=profile,
                    question=question,
                    question_text=question_text,
                    created_at = timezone.now()
                )

            predicted_tag = predict_tag(form.cleaned_data['question_text'])

            context = {
                'title': 'Ask',
                'Predicted Tag': predicted_tag,
                'Details': 'Asked Successfully'
            }

            return render(request, 'core:home.html', context)
        else:
            messages.error(request, 'Invalid form data. Please check your inputs.')
    else:
        form = AskQuestionForm()

    context = {
        'form': form,
        'title': 'Ask',
    }

    return render(request, 'feed/ask.html', context)
  
'''   # this view become the home now
@login_required
def questions(request):
    user_profile = Profile.objects.get(user=request.user)
    skills_list = user_profile.skills.all()
    question_list = Questions.objects.filter(
            (Q(is_answered=False, skills__in=skills_list)) | (Q(is_answered=False, skills__name='General'))
        ).exclude(author=user_profile).distinct()
    
    skills = request.GET.getlist('skills', [])
    if skills:
        question_list = question_list.filter(skills__in=skills).distinct()

    search_sentence = request.GET.get('search', '')
    if search_sentence:
        question_list = question_list.filter(question_text__icontains=search_sentence)

    for question in question_list:
        if question.is_anonymous:
            question.author = None

    return (question_list)
''' 
    
@login_required
def home(request):
    userprofile = Profile.objects.get(user=request.user)
    
    user_profile = Profile.objects.get(user=request.user)
    skills_list = user_profile.skills.all()
    question_list = Questions.objects.filter(
            (Q(is_answered=False, skills__in=skills_list)) | (Q(is_answered=False, skills__name='General'))
        ).exclude(author=user_profile).distinct()
    
    skills = request.GET.getlist('skills', [])
    if skills:
        question_list = question_list.filter(skills__in=skills).distinct()

    search_sentence = request.GET.get('search', '')
    if search_sentence:
        question_list = question_list.filter(question_text__icontains=search_sentence)

    for question in question_list:
        if question.is_anonymous:
            question.author = None
    
    context = {
        'title': 'Feed',
        'questions' : question_list,
        'userprofile': userprofile,
        'skills': skills_list,
    }
    return render(request, 'feed/home.html', context)


@login_required
def archive(request):
    user_profile = Profile.objects.get(user=request.user)
    skills_list = user_profile.skills.all()
    question_list = Questions.objects.filter(is_answered=True)
    
    skills = request.GET.getlist('skills', [])
    if skills:
        question_list = question_list.filter(skills__in=skills).distinct()

    search_sentence = request.GET.get('search', '')
    if search_sentence:
        question_list = question_list.filter(question_text__icontains=search_sentence)

    for question in question_list:
        if question.is_anonymous:
            question.author = None

    context = {
        "questions": question_list,
        "profile": user_profile,
        "title": 'Questions'
    }

    return render(request, 'archive.html', context)


@login_required
def about(request):
    context = {
        'title': 'About',
    }
    return render(request, 'feed/about.html', context)

    
# ml model to predict question tags
def predict_tag(question):
    NB = NaiveBayes()
    predictedTag = NB.predict(question)
    return predictedTag


@login_required
def answer(request, id):
    question = get_object_or_404(Questions, id=id)
    profile = get_object_or_404(Profile, user=request.user)

    user_skills = profile.skills.all()
    question_skills = question.skills.all()

    # Check if user skills match question skills to allow answering
    if not any(element in user_skills for element in question_skills):
        return HttpResponseBadRequest("Not your business")

    if request.method == 'POST':
        form = AnswerForm(request.POST)

        # Validate the form
        if form.is_valid():
            answer_text = form.cleaned_data['answer_text']

            # Create the answer
            answer = Answers.objects.create(
                author=profile,
                question=question,
                answer_text=answer_text,
                created_at = timezone.now()
            )

            # Mark the question as answered
            question.is_answered = True
            question.save()

            question_answers
        else:
            return HttpResponseBadRequest("Invalid form data")
    else:
        form = AnswerForm()

    context = {
        'form': form,
        'title': 'Answer',
    }

    return render(request, 'answer.html', context)


def question_answers(request, id):
    question = Questions.objects.get(pk=id)
    answers = Answers.objects.filter(question = question)
    
    if question.is_anonymous:
        question.author = None
    context = {
        'title': 'question answers',
        'question':question,
        'answers':answers,
    }
    
    return render(request, 'core/question.html', context)

@login_required
def toggle_vote(request, id, flag):
    try:
        profile = Profile.objects.get(user=request.user)
        answer = get_object_or_404(Answers, id=id)

        if flag == 'up':
            if profile in answer.down_vote.all():
                answer.down_vote.remove(profile)
                answer.up_vote.add(profile)
                
            elif profile not in answer.up_vote.all():
                answer.up_vote.add(profile)
                
            else:
                answer.up_vote.remove(profile)
                
        elif flag == 'down':
            if profile in answer.up_vote.all():
                answer.up_vote.remove(profile)
                answer.down_vote.add(profile)
                
            elif profile not in answer.down_vote.all():
                answer.down_vote.add(profile)
                
            else:
                answer.down_vote.remove(profile)

        answer.save()

        return redirect('core:question_answers', id=answer.question.id)

    except Answers.DoesNotExist:
        return HttpResponse('Answer not found', status=404)

    except Profile.DoesNotExist:
        return HttpResponse('Profile not found', status=404)

    except Exception as e:
        return HttpResponse(str(e), status=500)
    
#This view is used for to display all notifications that is not readed to specific user
@login_required
def notifications(request):
    profile = Profile.objects.get(user=request.user)
    user_notifications = Notification.objects.filter(profile=profile, is_read=False)
    context={
        "title":"Notification",
        "Notifications":user_notifications
    }
    return render('core:home', context)


#mark specific notification as read
@login_required
def mark_notifications_as_read(request,id):
    notification = Notification.objects.get(id=id)
    notification.is_read = True
    notification.save()
    question = notification.answer.question

    return redirect('core:question_answers', id=question.id)
