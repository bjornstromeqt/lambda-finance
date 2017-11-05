
import graphene

from src.intrinio import IntrionioClient
from src.organizations import get_organizations, get_organization
from src.graphql.filterable_connection_field import FilterableSQLAlchemyConnectionField
from src.graphql.models import (
    Organization,
    Company,
    Owner
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

    owner = graphene.Field(Owner, identifier=graphene.String(required=True))

    # noinspection PyUnusedLocal
    @staticmethod
    def resolve_owner(_, info, identifier):
        client = IntrionioClient()
        result = client.make_request('GET', 'owners', params={'identifier': identifier})
        if result.get('errors'):
            return None

        return Owner(**result)

    search_owner = graphene.List(Owner, name=graphene.String(required=True))

    # noinspection PyUnusedLocal
    @staticmethod
    def resolve_search_owner(_, info, name):
        client = IntrionioClient()
        result = client.make_request('GET', 'owners', params={'query': name})

        if result.get('errors'):
            return []

        return [Owner(**row) for row in result['data']]

