import requests
import click
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import json


def get_init(url, user_id, user_password, show_chrome):

    global browser
    global article_url
    article_url = 'https://hiro-unipa.itp.kindai.ac.jp/up/faces/up/po/pPoa0202A.jsp?fieldId='
    global user_name
    user_name = user_id[:10]

    options = Options()
    if (show_chrome is False):
        options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    check_timeout()
    userNameField = browser.find_element_by_id("form1:htmlUserId")
    passwordField = browser.find_element_by_id("form1:htmlPassword")
    submitButton = browser.find_element_by_id("form1:login")
    userNameField.send_keys(user_id)
    passwordField.send_keys(user_password)
    submitButton.click()


def check_timeout():
    try:
        browser.find_element_by_id("form1:login")
    except:
        pagemove_button = browser.find_element_by_id("form1:logout")
        pagemove_button.click()


def get_stream_info():
    open_stream_field_button = browser.find_element_by_id(
        "form1:Poa00201A:htmlParentTable:0:htmlDisplayOfAll:0:allInfoLink")
    open_stream_field_button.click()
    html = browser.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")
    for s in soup('script'):
        s.decompose()
    for s in soup.select("br"):
        s.replace_with("\n")

    global info_title
    global info_len

    list_num = 0
    info_title = []
    info_url = []

    for class_name in soup.find_all("a", class_="outputLinkEx"):
        name = soup.find_all("a", class_="outputLinkEx")[list_num].get_text()
        id = soup.find_all("a", class_="outputLinkEx")[list_num].get('id')
        url = article_url + id
        info_title.append(name)
        info_url.append(url)
        list_num += 1
    move_to_main_stream()
    del info_title[0:8]
    del info_url[0:8]
    info_len = len(info_title)


def get_stream_education():
    open_stream_field_button = browser.find_element_by_id(
        "form1:Poa00201A:htmlParentTable:1:htmlDisplayOfAll:0:allInfoLink")
    open_stream_field_button.click()
    html = browser.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")
    for s in soup('script'):
        s.decompose()
    for s in soup.select("br"):
        s.replace_with("\n")

    global education_title
    global education_release_date
    global education_len

    list_num = 0
    education_title = []
    education_release_date = []
    education_url = []

    for class_name in soup.find_all("a", class_="outputLinkEx"):
        name = soup.find_all("a", class_="outputLinkEx")[list_num].get_text()
        id = soup.find_all("a", class_="outputLinkEx")[list_num].get('id')
        url = article_url + id
        education_title.append(name)
        education_url.append(url)
        list_num += 1

    list_num = 0

    for class_data in soup.find_all("span", class_="insDate"):
        data = soup.find_all("span", class_="insDate")[list_num].get_text()
        if data == '':
            break
        str = data[2:12].split('/')
        release_date = str[0] + '-' + str[1] + '-' + str[2]
        education_release_date.append(release_date)
        list_num += 1
    move_to_main_stream()
    del education_title[0:8]
    del education_url[0:8]
    education_len = len(education_title)


def get_stream_student():
    open_stream_field_button = browser.find_element_by_id(
        "form1:Poa00201A:htmlParentTable:2:htmlDisplayOfAll:0:allInfoLink")
    open_stream_field_button.click()
    html = browser.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")
    for s in soup('script'):
        s.decompose()
    for s in soup.select("br"):
        s.replace_with("\n")

    global student_title
    global student_release_date
    global student_len

    list_num = 0
    student_title = []
    student_release_date = []
    student_url = []

    for class_name in soup.find_all("a", class_="outputLinkEx"):
        name = soup.find_all("a", class_="outputLinkEx")[list_num].get_text()
        id = soup.find_all("a", class_="outputLinkEx")[list_num].get('id')
        url = article_url + id
        student_title.append(name)
        student_url.append(url)
        list_num += 1

    list_num = 0

    for class_data in soup.find_all("span", class_="insDate"):
        data = soup.find_all("span", class_="insDate")[list_num].get_text()
        if data == '':
            break
        str = data[2:12].split('/')
        release_date = str[0] + '-' + str[1] + '-' + str[2]
        student_release_date.append(release_date)
        list_num += 1
    move_to_main_stream()
    del student_title[0:8]
    del student_url[0:8]
    student_len = len(student_title)


def move_to_main_stream():
    back_button = browser.find_element_by_id(
        "form1:Poa00201A:htmlParentTable:0:htmlHeaderTbl:0:retrurn")
    back_button.click()


def get_scraping_date():
    today = datetime.date.today()
    year = str(today.year)
    month = str(today.month)
    day = str(today.day)
    if today.month < 10:
        month = '0' + month
    if today.day < 10:
        day = '0' + day
    global scraping_date
    scraping_date = year + '-' + month + '-' + day


def create_json():
    info = []
    education = []
    student = []
    data = []
    json_num = 0

    while json_num < info_len:
        info_json = {'ID': json_num,
                     'title': info_title[json_num]}
        info.append(info_json)
        json_num += 1

    json_num = 0

    while json_num < education_len:
        education_json = {
            'ID': json_num, 'title': education_title[json_num], 'release-date': education_release_date[json_num]}
        education.append(education_json)
        json_num += 1

    json_num = 0

    while json_num < student_len:
        student_json = {
            'ID': json_num, 'title': student_title[json_num], 'release-date': student_release_date[json_num]}
        student.append(student_json)
        json_num += 1

    info_data = {'info': info}
    education_data = {'education': education}
    student_data = {'student': student}

    data.append(info_data)
    data.append(education_data)
    data.append(student_data)

    scraping_json = {'get-date': scraping_date,
                     'user-name': user_name, 'data': data}

    global data_json

    data_json = json.dumps(scraping_json, indent=4, ensure_ascii=False)


def main(url, user_id, user_password, show_chrome):
    get_init(url, user_id, user_password, show_chrome)
    get_stream_info()
    get_stream_education()
    get_stream_student()
    get_scraping_date()
    create_json()

    return data_json


if __name__ == "__main__":
    main()

