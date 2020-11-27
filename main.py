"""
Ce programme est un web scraper des cours de https://www.fun-mooc.fr/
Nous recherchons des cours d'informatique en rapport avec les données.
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import re
import time

WORDS_TO_CATCH = ["Deep Learning","Machine Learning","Intelligence Artificielle", "Data Science","Big data","Business intelligence","Informatique décisionelle"]

courses =  []
date_debut = []
ecole =  []

def clean_date_str(date_str):
    """
    Permet d'éliminer tous les blanc et retours chariot à l'intérieur de la date.
    """
    list_str = list(date_str)
    new_str_list =[]
    for i in range(len(list_str)):
        if(list_str[i]!=" " and list_str[i]!="\n"):
            new_str_list.append(list_str[i])
        elif(list_str[i]==" " and list_str[i+1]!=" "):
            new_str_list.append(list_str[i])
        else:
            continue
    return ''.join(new_str_list)

def filter_courses(soup_elts):
    """
    Permet de filtrer les cours pour ne garder que ceux qui répondent aux critères.
    """
    for div in soup_elts:
        course_name  = div.find('div', attrs={"class":"title"})
        course_name = str(course_name.string).strip()
        course_date = div.find('div', attrs={"class":"date"})
        course_date = str(course_date.text).strip()
        course_date = clean_date_str(course_date)
        print(course_date)
        course_universite = div.find('div',attrs={"class":"universities"}) 
        course_universite = str(course_universite.string).strip()
        for word in WORDS_TO_CATCH :
            word=word.lower()
            word_search = re.compile(word)
            if word_search.search(course_name.lower()):
                courses.append(course_name)
                date_debut.append(course_date)
                ecole.append(course_universite)
            else:
                continue

driver =  webdriver.Chrome("E:\LOGICIELS\DEV-TOOLS\webdriver\chromedriver_win32\chromedriver")

driver.get("https://www.fun-mooc.fr/cours/#filter/subject/informatique?page=1&rpp=50")
time.sleep(10)
page_source = driver.page_source
beauti =  BeautifulSoup(page_source, features='html.parser')
beauti_elements = beauti.findAll(name='div', attrs={'class':"course-block"})
filter_courses(beauti_elements)
df = pd.DataFrame({'Titre du cours':courses, 'Date de début':date_debut,'Université':ecole})
df.to_csv('cours.csv',index=False, encoding='utf-8')