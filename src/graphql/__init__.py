import graphene
from src.graphql.queries import Query
from src.graphql.mutations import Mutations

from src.graphql.models import (
    Organization
)


schema = graphene.Schema(
    query=Query, mutation=Mutations, types=[Organization]
)
