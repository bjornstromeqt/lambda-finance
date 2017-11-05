import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from src.intrinio import IntrionioClient
from src.graphql import custom_types
from src.organizations.models import Organization as OrganizationModel
from src.graphql.models.financials import IncomeStatement, BalanceSheet, FinancialStatements


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

    # noinspection PyUnusedLocal
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

    # noinspection PyUnusedLocal
    def resolve_stock_prices(self, info, **kwargs):
        from src.google_finance import historical
        if None in [self.symbol, self.market]:
            return []
        data = historical.get_data(symbol=self.symbol, market=self.market, **kwargs)
        return [StockPrice(**row) for row in data.to_dict(orient="records")]

    income_statement = graphene.List(
        IncomeStatement,
        start_year=graphene.Argument(graphene.String),
        end_year=graphene.Argument(graphene.String)
    )

    # noinspection PyUnusedLocal
    def resolve_income_statement(self, info, start_year=None, end_year=None):
        # https://api.intrinio.com/financials/standardized?identifier={symbol}&statement={statement}&fiscal_year={fiscal_year}&fiscal_period={fiscal_period}
        client = IntrionioClient()
        url = 'fundamentals/standardized'
        params = {'identifier': self.symbol, 'statement': FinancialStatements.INCOME_STATEMENT, 'type': 'FY'}
        response = client.make_request('GET', url, params=params)

        start_year = start_year if start_year else 2010
        end_year = end_year if end_year else None

        income_statements = []
        for filing in response['data']:
            if filing['fiscal_year'] < start_year:
                break

            _params = {
                'identifier': self.symbol,
                'statement': 'income_statement',
                'fiscal_year': filing['fiscal_year'],
                'fiscal_period': filing['fiscal_period']
            }
            _response = client.make_request('GET', 'financials/standardized', params=_params)
            financial_data = {row['tag']: row['value'] for row in _response['data']}
            income_statements.append(IncomeStatement(**filing, **financial_data))

        return income_statements

    balance_sheet = graphene.List(
        BalanceSheet,
        start_year=graphene.Argument(graphene.String),
        end_year=graphene.Argument(graphene.String)
    )

    # noinspection PyUnusedLocal
    def resolve_balance_sheet(self, info, start_year=None, end_year=None):
        # https://api.intrinio.com/financials/standardized?identifier={symbol}&statement={statement}&fiscal_year={fiscal_year}&fiscal_period={fiscal_period}
        client = IntrionioClient()
        url = 'fundamentals/standardized'
        params = {'identifier': self.symbol, 'statement': FinancialStatements.BALANCE_SHEET, 'type': 'FY'}
        response = client.make_request('GET', url, params=params)

        start_year = start_year if start_year else 2010
        end_year = end_year if end_year else None

        balance_sheets = []
        for filing in response['data']:
            if filing['fiscal_year'] < start_year:
                break

            _params = {
                'identifier': self.symbol,
                'statement': FinancialStatements.BALANCE_SHEET,
                'fiscal_year': filing['fiscal_year'],
                'fiscal_period': filing['fiscal_period']
            }
            _response = client.make_request('GET', 'financials/standardized', params=_params)
            financial_data = {row['tag']: row['value'] for row in _response['data']}
            balance_sheets.append(BalanceSheet(**filing, **financial_data))

        return balance_sheets


class InsiderHolding(graphene.ObjectType):
    ticker = graphene.String()
    company_cik = graphene.String()
    company_name = graphene.String()
    last_reported_date = graphene.Field(custom_types.DateType)
    value = graphene.Float()
    amount = graphene.Float()


class Owner(graphene.ObjectType):
    owner_cik = graphene.String()
    owner_name = graphene.String()
    state = graphene.String()
    state_inc = graphene.String()
    country_inc = graphene.String()
    business_address = graphene.String()
    business_phone_no = graphene.String()
    mailing_address = graphene.String()
    institutional = graphene.Boolean()

    insider_holdings = graphene.List(InsiderHolding)

    # noinspection PyUnusedLocal
    def resolve_insider_holdings(self, info):
        client = IntrionioClient()
        result = client.make_request('GET', 'owners/insider_holdings', params={'cik': self.owner_cik})

        return [InsiderHolding(**row) for row in result['data']]
