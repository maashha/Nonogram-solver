from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv
for number in range(3,1003):
    url='https://www.nonograms.org/nonograms/i/' + str(number)
    driver = webdriver.Chrome()
    driver.get(url)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('td', {'class': 'nmtl'})
    w = soup.find_all('div', {'class': 'content'})
    file = open("test"+str(number)+".txt", "w")
    if len(w)>0:
        if len(w[0].find_all('td'))>0:
            if len(((w[0].find_all('td')[0].text)[(w[0].find_all('td')[0].text).find(' ') + 1:]).split('x')) == 2:
                n = ((w[0].find_all('td')[0].text)[(w[0].find_all('td')[0].text).find(' ') + 1:]).split('x')[1]
                m = ((w[0].find_all('td')[0].text)[(w[0].find_all('td')[0].text).find(' ') + 1:]).split('x')[0]
            else:
                continue
        else:
            continue
    else:
        continue
    file.write(n+" "+m+"\n")
    for i in links:
        r = i.find_all('tr')
        we = ''
        for j in range(len(r)):
            for h in range(len(r[j].find_all('td', {'class': 'num'}))):
                if h!=(len(r[j].find_all('td', {'class': 'num'})) - 1):
                    we = we + r[j].find_all('td', {'class': 'num'})[h].text + " "
                else:
                    we = we + r[j].find_all('td', {'class': 'num'})[h].text + "\n"
        file.write(we)
    links = soup.find_all('td', {'class': 'nmtt'})
    result = {}
    for i in links:
        r = i.find_all('tr')
        for j in range(len(r)):
            count = 0
            for h in range(len(r[j].find_all('td'))):
                count += 1
                if r[j].find_all('td')[h].text != "\xa0":
                    if count in result.keys():
                        result[count].append(int(r[j].find_all('td')[h].text))
                    else:
                        result[count] = [int(r[j].find_all('td')[h].text)]
    for i in range(1,len(result.keys())+1):
        we = ''
        for j in range(len(result[i])):
            if j!=len(result[i]) - 1:
                we = we + str(result[i][j]) + " "
            else:
                we = we + str(result[i][j]) + "\n"
        file.write(we)
    file.close()