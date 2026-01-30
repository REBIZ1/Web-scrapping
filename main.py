import json
from scraping.base import ArticlesScraping

if __name__ == '__main__':
    words = input("Enter words: ").split()
    count = int(input("Enter count: "))
    path = input("Enter path: (по умолчанию: articles.json)")
    Article = ArticlesScraping(words)
    result = Article.collect_articles(count)
    Article.save_json(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
