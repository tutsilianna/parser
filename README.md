# Парсер для сайта METRO

**Цель:** спарсить любую категорию, где более 100 товаров, для городов Москва и Санкт-Петербург и выгрузить в любой удобный формат(csv, json, xlsx). Важно, чтобы товары были в наличии.


**Необходимые данные:**
* id товара из сайта/приложения, 
* наименование, 
* ссылка на товар, 
* регулярная цена, 
* промо цена, 
* бренд.

## Структура проекта
```
.
├───data
│   └───metro_shokolad-batonchiki.csv  # собранные данные из категории "Шоколад и батончики"
├───metro_parser                         
│   └───main.py                        # скрипт по парсингу сайта магазина Metro
├───requirements.txt
└───README.md
```

## Использование
1. `git clone https://github.com/tutsilianna/parser.git`
2. `python -m venv env_name`
3. `source env_name/bin/activate`
4. `pip install -r requirements.txt`
5. `python metro_parser/main.py`
