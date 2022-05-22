import algoliasearch_django as algoliasearch
from bottle.models import (
    Range,
    Stock,
    StockList,
    Warehouse,
)


algoliasearch.register(Range)
algoliasearch.register(Stock)
algoliasearch.register(StockList)
algoliasearch.register(Warehouse)
