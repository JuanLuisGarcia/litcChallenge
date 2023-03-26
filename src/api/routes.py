from flask import request, jsonify, send_from_directory
from .config import app
from .exceptions import UnknowError
from .helpers.data_transactions import get_or_create, create_or_update, save_data, get_market, get_product
from .helpers.filters import get_product_filter_values, get_market_filter
from. models import ProductPrice, Product, Market


@app.route('/api/product/<market_name>', methods=['GET'])
def get_products_by_market(market_name):
    return parse_response(ProductPrice.query.filter_by(market_name=market_name).all())


@app.route('/api/product', methods=['POST'])
def create_product():
    json_data = request.get_json()
    filter_values = get_product_filter_values(json_data)
    instance = get_or_create(Product, filter_values, **json_data)
    return parse_response([instance])


@app.route('/api/product/assign_price', methods=['POST'])
def assign_product_market_price():
    json_data = request.get_json()
    try:
        market = get_market(json_data['market'])
        product = get_product({"name": json_data['product'], "brand": json_data['brand']})
    except Exception as exc:
        return raise_exception(exc)
    product_price_data = {
        'market': market,
        'product': product,
        'price': json_data['price'],
    }
    instance = create_or_update(ProductPrice, **product_price_data)
    return parse_response([instance])


@app.route('/api/product', methods=['PUT'])
def edit_product():
    json_data = request.get_json()
    filter_values = Product.filter(json_data)
    try:
        product = get_product(filter_values)
        product.price = json_data['price']
        product.sugar = json_data['sugar']
        product.calories = json_data['calories']
    except Exception as exc:
        return raise_exception(exc)

    save_data(product)
    return parse_response([product])


@app.route('/api/product', methods=['GET'])
def get_all_products():
    return parse_response(Product.query.all())


@app.route('/api/market', methods=['GET'])
def get_all_markets():
    return parse_response(Market.query.all())


@app.route('/api/market', methods=['POST'])
def create_market():
    json_data = request.get_json()
    filter_values = get_market_filter(json_data)
    try:
        instance = get_or_create(Market, filter_values, **json_data)
    except Exception as exc:
        return raise_exception(exc)
    return parse_response([instance])


@app.route('/api/swagger.json')
def swagger_definition():
    return send_from_directory('.', "swagger.json")


def parse_response(items):
    results = []
    for item in items:
        results.append(item.as_dict())
    return jsonify(results)

def raise_exception(exception):
    try:
        return jsonify(exception.description), exception.code
    except Exception as exc:
        # catch all possible errors so as not to leak application data by error
        unknown_error = UnknowError(exc)
        return jsonify(unknown_error.description), unknown_error.code