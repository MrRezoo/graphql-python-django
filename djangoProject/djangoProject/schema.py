import graphene

import accounts.schema
import home.schema


class Query(home.schema.HomeQuery, accounts.schema.AccountsQuery, graphene.ObjectType):
    pass


class Mutation(home.schema.Mutate, accounts.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
