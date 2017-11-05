
import graphene

from src.organizations import get_organizations, get_organization
from src.graphql.filterable_connection_field import FilterableSQLAlchemyConnectionField
from src.graphql.models import (
    Organization,
    Company
)


class Query(graphene.ObjectType):
    organization = graphene.Node.Field(Organization, name=graphene.String())

    all_organizations = FilterableSQLAlchemyConnectionField(Organization, name=graphene.String())

    all_companies = graphene.List(Company)

    # noinspection PyUnusedLocal
    @staticmethod
    def resolve_all_companies(_, info):
        companies = get_organizations()
        return [Company(**row) for row in companies]

    company = graphene.Field(Company, name=graphene.String(required=True))

    def resolve_company(self, info, name):
        company = get_organization(name)
        return Company(**company)
