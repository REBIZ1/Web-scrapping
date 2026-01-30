import json
from scraping.base import ArticlesScraping

if __name__ == '__main__':
    words = input("Enter words: ").split()
    count = int(input("Enter count: "))
    Article = ArticlesScraping(words)
    result = Article.collect_articles(count)
    print(json.dumps(result, ensure_ascii=False, indent=2))
