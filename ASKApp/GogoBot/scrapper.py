from bs4 import BeautifulSoup
from itertools import zip_longest
import requests
import csv
import time

i = 0
def append_file(filename, data):
    global i
    try:
        with open(filename, 'a', encoding='UTF-8') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow(data)
        print(f"Text appended to file {filename} successfully. {i}")
        i += 1
    except IOError:
        print("Error: could not append to file " + filename)

def remove_empty_lines(input_str):
    lines = input_str.splitlines()
    non_empty_lines = [line for line in lines if line.strip() != '']
    result_str = ''.join(non_empty_lines)
    return result_str

def get_content(url):
    page = requests.get(url)
    src = page.content
    soup = BeautifulSoup(src, 'lxml')

    post_txt = ''

    post = soup.find('div', {'class': 'post-layout'})
    if post:
      post_txt = post.find('div', {'class': 's-prose js-post-body'}).text.strip()
    else:
      pass

    return post_txt

def main(url, start_page, end_page):
    file_path = 'questionsDF.csv'
    questions_details = {}

    # loop over pages
    for i in range(start_page, end_page+1):
        page = requests.get(str(url + str(i)))
        src = page.content
        soup = BeautifulSoup(src, 'lxml')

        questions = soup.find('div', {'id': 'questions'})

        questions_content = questions.find_all('div', {'class': 's-post-summary--content'})
        questions_meta = questions.find_all('div', {'class': 's-post-summary--meta'})

        for content, meta in zip_longest(questions_content, questions_meta):
            question_title = content.find('a').text
            question_href = content.find('a').get('href')
            question_url = 'https://stackoverflow.com/' + question_href
            question_content = get_content(question_url)
            question_content = remove_empty_lines(question_content)
            questions_tags = meta.find_all('a', {'class': 'post-tag'})
            question_tags = ''

            for tag in questions_tags:
                if tag.text == questions_tags[-1].text:
                    question_tags += (tag.text)
                else:
                    question_tags += (tag.text + '_')

            questions_details = {'title': question_title, 'content': question_content, 'tags': question_tags}
        # print(questions)
            append_file(file_path, questions_details)
        time.sleep(60)


if __name__ == '__main__':
  # 'frontend', 'machine-learning',
  specific_tags = [ 'embedded', 'artificial-intelligence', 'android', 'backend']

  for x in specific_tags:
     url = f"https://stackoverflow.com/questions/tagged/{x}?sort=MostVotes&edited=true&page="
     main(url, 1, 10)
     time.sleep(30)
