from sqlalchemy import Column, Float, String, UniqueConstraint, Integer

from .config import db


class Market(db.Model):
    name = Column(String(100), primary_key=True, nullable=False)
    address = Column(String(100), nullable=False)
    product_prices = db.relationship('ProductPrice', backref='market')
    opening_time = Column(String(5), nullable=False)
    closing_time = Column(String(5), nullable=False)

    def as_dict(self):
        return {
            'name': self.name,
            'address': self.address,
            'opening_time': self.opening_time,
            'closing_time': self.closing_time
        }

    @staticmethod
    def filter(json_data):
        return {'name': json_data['name']}


class Product(db.Model):
    name = Column(String(100), primary_key=True, nullable=False)
    brand = Column(String(100), primary_key=True, nullable=False)
    calories = db.Column(Float, nullable=False)
    # todo, add max and min values
    sugar_percentage = Column(Float, nullable=False)
    saturated_fats_percentage = Column(Float, nullable=False)
    product_prices = db.relationship('ProductPrice', backref='product')
    __table_args__ = (UniqueConstraint('name', 'brand', name='unique_product_brand'),)

    def as_dict(self):
        return {
            'name': self.name,
            'brand': self.brand,
            'calories': self.calories,
            'sugar_percentage': self.sugar_percentage,
            'saturated_fats_percentage': self.saturated_fats_percentage,
        }

    @staticmethod
    def filter(json_data):
        return {
            'name': json_data['name'],
            'brand': json_data['brand'],
        }


class ProductPrice(db.Model):
    id = Column(Integer, primary_key=True)
    market_name = db.Column(db.Integer, db.ForeignKey('market.name'))
    product_name = db.Column(db.Integer, db.ForeignKey('product.name'))
    price = Column(Float, nullable=False)

    def as_dict(self):
        return {
            'market': self.market.as_dict(),
            'product': self.product.as_dict(),
            'price': self.price,
        }
