import graphene
from graphene import String


class Query(graphene.ObjectType):
    name = String()

    @staticmethod
    def resolve_name(root, info):
        print(root)
        return "Hello"


schema = graphene.Schema(query=Query, auto_camelcase=False)
result = schema.execute("""
    query {
        name
    }
""",root={'name':'reza'})

print(result.data)
print(result.errors)
