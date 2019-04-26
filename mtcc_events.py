#importing libraries
from selenium import webdriver
import random
import time
from selenium.webdriver.chrome.options import Options
import csv
from bs4 import BeautifulSoup
import re
import xlsxwriter

def main():

    
    # A randomizer for the delay
    seconds = 5 + (random.random() * 5)
    #creating list of months 
    monthlist = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    #final_link will save all the link related to all the events.
    final_link = []
    options = Options()
    options.headless = True
    # create a new Chrome session
    driver = webdriver.Chrome('C:/Users/xxxx/chromedriver.exe')
    driver.implicitly_wait(30)
    # driver.maximize_window()

    # navigate to the application home page
    driver.get("http://www.mtccc.com/events/")
    
    #getting all the links for events 
    for month in monthlist:
        time.sleep(1)
        time.sleep(1)
        #To get element find xpath of the elementt in html using cro-path extension in crome browser.
        #For Jan it was '//a[contains(text(),'Jan')]' and so on for other months
        #so we have created a list of months that is running in this for loop.
        #below line will click the Jan month on home page
        driver.find_element_by_xpath(str("// a[contains(text(), '"+month+"')]")).click()
        time.sleep(1)
        driver.implicitly_wait(30)

        pagehtml = driver.page_source
        soup = BeautifulSoup(pagehtml, "html.parser")
        # print(soup)
        PageContent = []
        content = str(soup.find('ul',attrs={"id": "eventList"}))
        #content = soup.findAll('ul')
        print(content)
        content1 = BeautifulSoup(content, "html.parser")
        #Running for loop for getting all the event links for current month in the loop
        for a in content1.find_all('a', href=True):

            print("Found the URL:", a['href'])
            final_link.append(a['href'])

    print(final_link)
    #Uncomment to save the data in csv
    #with open("Mttceventlist.csv", 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     for row in final_link:
    #         writer.writerow(row)
    # f.close()
    driver.quit()
    # So We have all the links of events now we will get social meadia links related to the events

    data_table = [['website name','facebook ','twitter','instagram','website link']]
    for link in final_link:
        print(link)
        options = Options()
        #using headless browser so that the code runs in back ground with out poping up the browser window
        options.headless = True
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver1 = webdriver.Chrome('C:/Users/xxxxxxx/chromedriver.exe')
        driver1.implicitly_wait(30)
        data_row=[]
        driver1.get(link)
        time.sleep(1)
        time.sleep(1)
        pagehtml1 = driver1.page_source

        soup2 = BeautifulSoup(pagehtml1, "html.parser")
        driver1.quit()
        content2 = str(soup2.find('div', attrs={"class": "col-sm-12 col-md-8 col-lg-8 event-single-title"}))
        soup3 = BeautifulSoup(content2, "html.parser")
        #print(str(soup3))
        event_name = soup3.find('h3').text
        data_row.append(event_name)
        print(event_name)
        #checking if facebook link is present or not if present append link if not present append none
        try:
            facebook_link = str(soup3.find('em', attrs={"class": "fa fa-facebook"}).find_previous())
            soup4 = BeautifulSoup(facebook_link, "html.parser")
            for a in soup4.find_all('a', href=True):
               temp_f_link = a['href']
               data_row.append(temp_f_link)
        except AttributeError as e:
            data_row.append("None")
        #checking if twitter link is present or not if present append link if not present append none
        try:
            twitter_link = str(soup3.find('em', attrs={"class": "fa fa-twitter"}).find_previous())
            soup5 = BeautifulSoup(twitter_link, "html.parser")
            for a in soup5.find_all('a', href=True):
                temp_t_link = a['href']
                data_row.append(temp_t_link)
        except AttributeError as e:
            data_row.append("None")
        #checking if insta link is present or not if present append link if not present append none
        try:
            instagram_link = str(soup3.find('em', attrs={"class": "fa fa-instagram"}).find_previous())
            soup6 = BeautifulSoup(instagram_link, "html.parser")
            for a in soup6.find_all('a', href=True):
                temp_i_link = a['href']
                data_row.append(temp_i_link)
        except AttributeError as e:
            data_row.append("None")
        #checking if website link is present or not if present append link if not present append none
        try:
            website_link = soup3.find('a', attrs={"target": "_blank"})
            if str(website_link) == None or website_link =="":
               data_row.append("None")
            else:
                data_row.append(website_link['href'])
            print(data_row)
        except TypeError as e:
            data_row.append("None")
        print(data_row)
        data_table.append(data_row)
    print(data_table)
    # code to write the data on csv
    # MttceventSocialMedia is name of the file
    with open("MttceventSocialMedia.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        for row in data_table:
            writer.writerow(row)
    f.close()

#Calling Main
main()
