from bs4 import BeautifulSoup
import os
import re
import requests
from urllib.request import urlretrieve

keyword = input("Keyword: ")

response = requests.get('https://www.comcbt.com/xe/anne')

soup = BeautifulSoup(response.text, 'lxml')

first = soup.find("div", {"id": "column"})

for i in first.find_all("a", attrs={'class':'a3'}):
    if i.text == keyword: 
        response = requests.get('https://www.comcbt.com/xe/' + i['href'][26:])

        soup = BeautifulSoup(response.text, 'lxml')

        total = 0
        num = 0
        
        # 총 페이지수 구하기
        if soup.find("a", title="끝 페이지"):
            num = int(soup.find("a", title="끝 페이지").text)
        else:
            num = 1
        
        # 한 게시글씩 들어가서 모든 첨부파일 다운로드
        for j in range(num):
            board = requests.get('https://www.comcbt.com/xe/index.php?mid={0}&page={1}'.format(i['href'][26:], j+1))

            soup = BeautifulSoup(board.text, 'lxml')

            for link in soup.find("tbody").find_all('a', attrs={'href': re.compile("https://")}):

                r = requests.get(link.get('href'))

                page = BeautifulSoup(r.text, 'lxml')

                for link in page.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['bubble']):
                    print(link.get('href'),link.get_text().strip())
                    urlretrieve(link.get('href'), link.get_text().strip())

        print(keyword + " download finished.")
