# Третья лабораторная работа

в качестве модели используется llama-3.3-70b-versatile, с сайта [Groq](https://console.groq.com/)
# Быстрый старт
1. Склонировать репозиторий: 
```ssh 
git clone https://github.com/abbeswrld/data-analytics-labs.git
cd data-analytics-labs
cd lab3
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
4. Получить API ключ на сайте [Groq](https://console.groq.com/)
5. Заполнить .env по примеру .env.example
6. Выполнить команду 
```ssh 
streamlit run main.py
```
