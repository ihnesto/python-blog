from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import requests
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'sffdgfsdaergthgewfghtrewfghtgrewwwgr'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1234@localhost/blog"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(2048), nullable=False)
    content = db.Column(db.Text, nullable=False)
    dateCreation = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"{self.id}:('{self.title[0:20]}' - '{self.content[0:10]}')"

# links = [ 'https://cnx-software.ru' ]
# for i in range(2, 6) :
#     links.append(f'{links[0]}/page/{i}/')
# for link in links :
#     print(link)
#     html = requests.get(link).text

#     soup = BeautifulSoup(html, 'lxml')

#     # print(soup.title)
#     articles = soup.find_all('article', class_= "post")
#     for article in articles :
#         h3 = article.find('h3', class_="entry-title")
#         article_header_text = h3.a.text
#         article_header_link = h3.a.get('href')

#         divImg = article.find('div', class_="post-thumbnail")
#         article_img_link = divImg.a.img.get('src')

#         divContent = article.find('div', class_="entry-content")
#         contentP = article.find_all('p')
#         article_content = ''
#         for para in contentP :
#             article_content += para.__repr__()
#         item = Article(title=article_header_text, content=article_content)
#         db.session.add(item)
#         db.session.commit()

@app.route('/')
def index() :  # ?page=2
    pageNum = request.args.get('page', 1, type=int)
    articles = Article.query.paginate(page=pageNum, per_page=4)
    # articles = Article.query.all()
    return render_template('index.html', articles=articles)

if __name__ == '__main__' :
    app.run(debug=True)
