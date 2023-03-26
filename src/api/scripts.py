import csv, os, random
from faker import Faker
from flask.cli import AppGroup

from .config import app

script_cli = AppGroup('script')


@script_cli.command('generate_data')
def generate_data():
    fake = Faker()

    def save_data(csv_name, columns, dict_data):
        try:
            with open(csv_name, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writeheader()
                for data in dict_data:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

    def create_markets_csv():
        market_columns = ['name', 'address', 'opening_time', 'closing_time']

        market_data = [
            {'name': 'mercadona', 'address': f"c/{fake.name()}", 'opening_time': '9:00', 'closing_time': '9:00'},
            {'name': 'lidl', 'address': f"c/{fake.name()}", 'opening_time': '9:00', 'closing_time': '9:00'},
            {'name': 'erosky', 'address': f"c/{fake.name()}", 'opening_time': '9:00', 'closing_time': '9:00'},
            {'name': 'suma', 'address': f"c/{fake.name()}", 'opening_time': '9:00', 'closing_time': '9:00'},
            {'name': 'ahorro', 'address': f"c/{fake.name()}", 'opening_time': '9:00', 'closing_time': '9:00'},
        ]
        save_data(os.path.join(app.config['GENERATED_DIR'], 'markets.csv'), market_columns, market_data)

        return market_data

    def create_products_csv():
        product_columns = ['name', 'brand', 'calories', 'sugar_percentage', 'saturated_fats_percentage']
        product_data = []
        for i in range(random.randint(50, 100)):
            product_data.append({
                "name": fake.name(),
                "brand": fake.name(),
                "calories": random.randint(0, 100),
                "sugar_percentage": random.randint(0, 100),
                "saturated_fats_percentage": random.randint(0, 100),
            })
        save_data(os.path.join(app.config['GENERATED_DIR'], 'products.csv'), product_columns, product_data)
        return product_data

    def create_products_price_csv(market_data, products_data):
        product_price_columns = ["market", "brand", "product", "price"]
        product_length = len(products_data)
        product_price_data = []
        for market in market_data:
            # number of products to this market
            number_of_products = random.randint(1, 10)
            for _ in range(number_of_products):
                product = products_data[random.randint(0, product_length-1)]
                product_price_data.append({
                    "market": market['name'],
                    "brand": product['brand'],
                    "product": product['name'],
                    "price": random.randint(0, 100),
                })
        save_data(os.path.join(app.config['GENERATED_DIR'], 'product_price.csv'), product_price_columns,
                  product_price_data)

    market_data = create_markets_csv()
    products_data = create_products_csv()
    create_products_price_csv(market_data, products_data)


@script_cli.command('load_data')
def load_data():
    import asyncio

    import aiohttp

    def get_objects(file_name):
        objects = list()
        with open(file_name) as f:
            reader = csv.DictReader(f)
            for row in reader:
                objects.append(row)
        return objects

    async def create_objets(url, object):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=object) as resp:
                print(resp.status)

    async def load_by_api_data():
        markets = get_objects(os.path.join(app.config['GENERATED_DIR'], 'markets.csv'))
        products = get_objects(os.path.join(app.config['GENERATED_DIR'], 'products.csv'))
        product_price = get_objects(os.path.join(app.config['GENERATED_DIR'], 'product_price.csv'))
        print('Start create markets')
        await asyncio.gather(*[create_objets('http://127.0.0.1:5000/api/market', market) for market in markets])
        print('Markets ready')
        print('Start create products')
        await asyncio.gather(*[create_objets('http://127.0.0.1:5000/api/product', product) for product in products])
        print('Products ready')
        print('Start create product prices')
        await asyncio.gather(
            *[create_objets('http://127.0.0.1:5000/api/product/assign_price', product_price) for product_price in
              product_price])
        print('Products prices ready')

    asyncio.run(load_by_api_data())


app.cli.add_command(script_cli)
