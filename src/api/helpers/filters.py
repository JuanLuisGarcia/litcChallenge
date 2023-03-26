def get_product_filter_values(json_data):
    return {
        'name': json_data['name'],
        'brand': json_data['brand'],
    }


def get_market_filter(json_data):
    return {'name': json_data['name']}
