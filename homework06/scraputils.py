import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import News

engine = create_engine("sqlite:///news.db")
Session = sessionmaker(bind=engine)


def extract_news(parser):
    news_list = []
    items = parser.select("tr.athing")

    for item in items:
        title = item.select_one("span.titleline > a")
        subtext = item.find_next_sibling("tr")
        user = subtext.select_one("a.hnuser")
        comments = subtext.select_one("a[href*='item?id=']")

        if title:
            link = title["href"]  # ссылка
            title_text = title.get_text()  # название
        else:
            link = None
            title_text = None

        if user:
            author = user.get_text()  # автор
        else:
            author = None

        if comments and "comment" in comments.get_text():
            comments_text = comments.get_text()
            comments_value = int(comments_text.split()[0])
        else:
            comments_value = 0

        points = subtext.select_one("span.score")
        if points:
            points_value = int(points.get_text().split()[0])  # количество лайков
        else:
            points_value = None

        if link and title_text:
            if link.startswith("item"):
                link = "https://news.ycombinator.com/" + link
            news_list.append(
                News(title=title_text, author=author, url=link, points=points_value, comments=comments_value)
            )

    return news_list


def extract_next_page(parser):
    next_page = str(parser.select_one("a.morelink")["href"])
    return next_page


def get_news(url, n_pages=1):
    news = []
    for i in range(n_pages):
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        print(response.status_code)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
    return news


def save_news_to_db(news_list):
    session = Session()
    for news_item in news_list:
        session.add(news_item)
    session.commit()
    session.close()


if __name__ == "__main__":
    news = get_news("https://news.ycombinator.com/newest", 1000 // 30 + 1)
    save_news_to_db(news)
