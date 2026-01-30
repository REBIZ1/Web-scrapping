import json
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from core.webdriver import get_chrome_driver
from scraping.utils import build_automation


class ArticlesScraping:
    def __init__(self, words: list[str]):
        self.browser = get_chrome_driver()
        self.words = words
        self.automation = build_automation(self.words)

    def _get_articles_list(self, link: str) -> list:
        """
        Возвращает список Web элементов статей
        """
        self.browser.get(link)
        articles_block = WebDriverWait(self.browser, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.tm-articles-list'))
        )
        articles_list = articles_block.find_elements(By.CSS_SELECTOR, 'article.tm-articles-list__item')
        return articles_list

    def _search_words(self, text: str) -> bool:
        """
        Поиск слов в тексте
        """
        text = text.lower()
        for _ in self.automation.iter(text):
            return True
        return False

    def _get_full_article_text(self, href: str) -> str:
        """
        Возвращает полный текст статьи
        """
        self.browser.get(href)
        content_text = WebDriverWait(self.browser, 3).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div.article-formatted-body')
            )
        ).text
        tags = self.browser.find_elements(
            By.CSS_SELECTOR,
            'ul.tm-separated-list__list li span'
        )
        tags_text = ' '.join(tag.text for tag in tags)
        return f'{tags_text} {content_text}'

    def _extract_article_preview(self, article: WebElement) -> dict:
        """
        Возвращает текст статьи с превьюшки
        """
        title = article.find_element(By.CSS_SELECTOR, 'a.tm-title__link')
        return{
            'title': title.text,
            'link': title.get_attribute('href'),
            'date': article.find_element(By.CSS_SELECTOR, 'time').get_attribute('datetime'),
            'preview_text': article.find_element(
                By.CSS_SELECTOR, 'div.article-formatted-body'
            ).text,
            'preview_tags': ' '.join(
                tag.text for tag in article.find_elements(
                    By.CSS_SELECTOR, 'div.tm-publication-hubs span'
                )
            )
        }

    def _save_json(self, result: list[dict]) -> None:
        """
        Сохраняет найденные статьи в JSON
        """
        with open('articles.json', 'w', encoding='utf-8') as file:
            json.dump(result, file,ensure_ascii=False, indent=2)

    def collect_articles(self, count: int) -> list[dict]:
        """
        Объединяет текст превью и статьи, ищет нужные статьи и возвращает их.
        count - кол-во необходимых статей.
        """
        result = []
        page = 1
        while len(result) < count:
            articles = self._get_articles_list(f'https://habr.com/ru/articles/page{page}/')
            previews = [self._extract_article_preview(article) for article in articles]
            for preview in previews:
                full_text = self._get_full_article_text(preview['link'])
                combined_text = ' '.join([
                    preview['title'],
                    preview['preview_text'],
                    preview['preview_tags'],
                    full_text
                ])
                if self._search_words(combined_text):
                    result.append({
                        'date': preview['date'],
                        'title': preview['title'],
                        'link': preview['link']
                    })
                    if len(result) == count:
                        break
            page += 1
        self._save_json(result)
        return result