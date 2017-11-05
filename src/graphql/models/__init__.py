from graphene import relay
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from src.graphql import custom_types
from src.organizations.models import Organization as OrganizationModel


class StockPrice(graphene.ObjectType):
    """
    Stock prices
    """
    open = graphene.Float()
    high = graphene.Float()
    low = graphene.Float()
    close = graphene.Float()
    volume = graphene.Float()

    date = graphene.Field(custom_types.DateType)
    market = graphene.String()
    symbol = graphene.String()


class Organization(SQLAlchemyObjectType):
    class Meta:
        model = OrganizationModel
        interfaces = (relay.Node, )

    symbol = graphene.String()
    market = graphene.String()

    stock_prices = graphene.List(
        StockPrice, start_date=graphene.Argument(custom_types.DateType), end_date=graphene.Argument(custom_types.DateType)
    )

    def resolve_stock_prices(self, info, **kwargs):
        from src.google_finance import historical
        if None in [self.symbol, self.market]:
            return []
        data = historical.get_data(symbol=self.symbol, market=self.market, **kwargs)
        return [StockPrice(**row) for row in data.to_dict(orient="records")]


class Company(graphene.ObjectType):
    name = graphene.String()
    symbol = graphene.String()
    market = graphene.String()
    stock_prices = graphene.List(
        StockPrice, start_date=graphene.Argument(custom_types.DateType), end_date=graphene.Argument(custom_types.DateType)
    )

    def resolve_stock_prices(self, info, **kwargs):
        from src.google_finance import historical
        if None in [self.symbol, self.market]:
            return []
        data = historical.get_data(symbol=self.symbol, market=self.market, **kwargs)
        return [StockPrice(**row) for row in data.to_dict(orient="records")]
