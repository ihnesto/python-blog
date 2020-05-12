# pip install BeautifulSoup4
# pip install lxml
# pip install requests


from bs4 import BeautifulSoup
import requests

import pymysql.cursors

# CREATE TABLE articles (
#     id int(11) NOT NULL AUTO_INCREMENT,
#     article_header_text varchar(2048) NOT NULL,
#     article_header_link varchar(2048) NOT NULL,
#     article_content text NOT NULL,
#     article_img_link varchar(2048) NOT NULL,
#     PRIMARY KEY (id)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
# AUTO_INCREMENT=1;

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='cnx-data',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

html = requests.get("https://cnx-software.ru").text

soup = BeautifulSoup(html, 'lxml')

# print(soup.title)
articles = soup.find_all('article', class_= "post")
for article in articles :
    h3 = article.find('h3', class_="entry-title")
    article_header_text = h3.a.text
    article_header_link = h3.a.get('href')

    divImg = article.find('div', class_="post-thumbnail")
    article_img_link = divImg.a.img.get('src')

    divContent = article.find('div', class_="entry-content")
    contentP = article.find_all('p')
    article_content = ''
    for para in contentP :
        article_content += para.__repr__()

    cursor = connection.cursor()

    sql = "INSERT INTO articles (article_header_text, article_header_link, article_content, article_img_link) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (article_header_text, article_header_link, article_content, article_img_link))

    connection.commit()

    
connection.close()





# https://cnx-software.ru/page/2/



# https://cnx-software.ru/2020/05/page/2/
# https://cnx-software.ru/tag/iot/page/2/

# <div class="wp-block-image">
# h2
# ul
# p



