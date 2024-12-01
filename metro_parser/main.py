"""
Скрипт для парсинга данных с сайта metro-cc.ru
"""
import csv
import requests
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
                   AppleWebKit/537.36 (KHTML, like Gecko) \
                   Chrome/131.0.0.0 Safari/537.36'
}

shop_ids = {
    "Москва": "19",          # Москва, ул. Шоссейная, д. 2Б
    "Санкт-Петербург": "16"  # Санкт-Петербург, пр-т Косыгина, д. 4, лит. А
}
CATEGORY_SLUG = "shokolad-batonchiki"
OUTPUT_FILE = f"data/metro_{CATEGORY_SLUG}.csv"
URL = "https://online.metro-cc.ru"


def fetch_products(shop_id):
    '''
    Функция для выполнения запроса к API
    '''
    data = {
        "query": """
        query Query($storeId: Int!, $slug: String!, $from: Int!, 
                    $size: Int!, $sort: InCategorySort, $in_stock: Boolean) {
            category (storeId: $storeId, slug: $slug, inStock: $in_stock) {
                products(from: $from, size: $size, sort: $sort) {
                    id
                    name
                    url
                    stocks {
                        prices_per_unit {
                            price
                            old_price
                        }
                    }
                    manufacturer {
                        name
                    }
                }
            }
        }
        """,
        "variables": {
            "storeId": int(shop_id),
            "slug": CATEGORY_SLUG,
            "from": 0,
            "size": 200,
            "sort": "default",
            "in_stock": True
        },
    }

    response = requests.post(
        "https://api.metro-cc.ru/products-api/graph",
        headers=headers,
        json=data,
        timeout=10
    )
    if response.status_code == 200:
        return response.json()

    print(f"Ошибка запроса: {response.status_code}, {response.text}")
    return None


def process_and_save(products, city):
    '''
    Функция для обработки и сохранения
    '''
    rows = []
    for product in products:
        product_id = product.get("id")
        name = product.get("name")

        url = URL + product.get("url", "")

        stocks = product.get("stocks", [])
        price = None
        old_price = None

        if stocks:
            prices_per_unit = stocks[0]["prices_per_unit"]
            if prices_per_unit:
                price = prices_per_unit['price']
                old_price = prices_per_unit['old_price']

        brand = product.get("manufacturer", {}).get("name")

        rows.append({
            "id": product_id,
            "name": name,
            "url": url,
            "price": price,
            "old_price": old_price,
            "brand": brand,
            "city": city,
        })
    return rows


def save_to_csv(rows):
    """
    Функция для сохранения данных в CSV файл
    """
    with open(OUTPUT_FILE, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["id", "name", "url", "price", "old_price", "brand", "city"])
        writer.writeheader()
        writer.writerows(rows)


def delete_duplicates():
    """
    Функция для удаления дубликатов с помощью pandas
    """
    data = pd.read_csv(OUTPUT_FILE)
    data.drop_duplicates(inplace=True)
    data.to_csv(OUTPUT_FILE, index=False)


def main():
    '''
    Главная функция: запрос, обработка, сохранение
    '''
    all_rows = []
    for city, shop_id in shop_ids.items():
        print(f"Сбор данных для города: {city}")
        data = fetch_products(shop_id)
        if data:
            products = data.get("data", {}).get(
                "category", {}).get("products", [])
            if len(products) > 100:
                city_rows = process_and_save(products, city)
                all_rows.extend(city_rows)

    save_to_csv(all_rows)
    delete_duplicates()

    print(f"Данные успешно сохранены в файл: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
