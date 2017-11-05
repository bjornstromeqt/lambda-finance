import graphene
import graphql_relay

from src.graphql import helpers
from src.graphql.models import (
    Organization, OrganizationModel
)


# -----------------------------------------------------
# Mutations for Organization
# -----------------------------------------------------
class OrganizationInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    symbol = graphene.String()
    market = graphene.String()


class CreateOrganization(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(OrganizationInput, required=True)

    organization = graphene.Field(Organization)

    # noinspection PyUnusedLocal
    @classmethod
    def mutate(cls, root, info, data):
        created_organization = OrganizationModel.add(**data)
        return CreateOrganization(organization=created_organization)


class UpdateOrganization(graphene.Mutation):
    class Arguments:
        global_id = graphene.Argument(OrganizationInput, required=True)
        data = graphene.ID(required=True)

    organization = graphene.Field(Organization)

    # noinspection PyUnusedLocal
    @classmethod
    def mutate(cls, root, info, global_id, data):
        model_id = helpers.convert_from_global_id(global_id, Organization)
        updated_organization = OrganizationModel.update(model_id, **data)
        return UpdateOrganization(organization=updated_organization)


class DeleteOrganization(graphene.Mutation):
    class Arguments:
        global_id = graphene.ID(required=True)

    organization_id = graphene.ID()

    # noinspection PyUnusedLocal
    @classmethod
    def mutate(cls, root, info, global_id):
        model_id = helpers.convert_from_global_id(global_id, Organization)
        deleted_id = OrganizationModel.delete(model_id)
        global_deleted_id = graphql_relay.to_global_id(Organization.__name__, deleted_id)
        return cls(organization_id=global_deleted_id)


class Mutations(graphene.ObjectType):
    create_organization = CreateOrganization.Field()
    update_organization = UpdateOrganization.Field()
    delete_organization = DeleteOrganization.Field()
