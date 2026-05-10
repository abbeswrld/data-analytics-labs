# Вторая лабораторная работа

в качестве модели используется nvidia/nemotron-3-nano-30b-a3b, с сайта [openrouter.ai](https://openrouter.ai/)

# Пайплайн

в файле input.csv содержатся две колонки - title, text
в ллм отправляется запрос на саммаризацию текста, используется системный промпт + юзер промпт
ответы записываются в output.txt

# Быстрый старт
1. Склонировать репозиторий: 
```ssh 
git clone https://github.com/abbeswrld/data-analytics-labs.git
cd data-analytics-labs
cd lab2
```
2. Создать виртуальное окружение: 
```ssh
python -m venv .venv
.venv/Scripts/activate
```
3. Установить зависимости
```ssh
pip install -r requirements.txt
```
4. Получить API ключ на сайте [openrouter.ai](https://openrouter.ai/)
5. Заполнить .env по примеру .env.example
6. Выполнить команду 
```ssh 
python main.py
```
