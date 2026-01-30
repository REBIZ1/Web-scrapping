## Установка и запуск проекта

### 1. Клонирование репозитория

```bash
git clone git@github.com:REBIZ1/Web-scrapping.git
```

### 2. Создание и активация виртуального окружения

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS / Linux:
```bash
source .venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Запуск 

```bash
python main.py
```

### Входные данные

- words - по каким словам искать статьи;
- count - Кол-во необходимых статей;
- path - путь куда сохранить .json. 


