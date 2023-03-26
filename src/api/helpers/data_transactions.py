from api.config import db
from api.exceptions import UnknowError, TypeError, RelatedObjectNotFound
from werkzeug.exceptions import NotFound

from api.models import Market, Product


def get_or_create(model, filter, **kwargs):
    try:
        instance = model.query.filter_by(**filter).first()
        if not instance:
            instance = model(**kwargs)
            save_data(instance)
        return instance
    except TypeError as exc:
        raise TypeError(exc)
    except Exception as exc:
        raise UnknowError(exc)


def create_or_update(model, **kwargs):
    try:
        instance = model(**kwargs)
        db.session.merge(instance)
        db.session.commit()
        return instance
    except Exception as exc:
        raise UnknowError(exc)


def save_data(instance):
    db.session.add(instance)
    db.session.commit()


def get_market(market_filter):
    try:
        return Market.query.get_or_404(market_filter)
    except NotFound as exc:
        raise RelatedObjectNotFound(exc, 'Market')


def get_product(product_filter):
    try:
        return Product.query.get_or_404(product_filter)
    except NotFound as exc:
        raise RelatedObjectNotFound(exc, 'Product')
