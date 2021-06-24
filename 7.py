import graphene
from graphene import String


class Person(graphene.ObjectType):
    full_name = String()

    @staticmethod
    def resolve_full_name(root, info):
        return f'{root["fname"]} {root["lname"]}'


class Query(graphene.ObjectType):
    ps = graphene.Field(Person)

    @staticmethod
    def resolve_ps(root, info):
        return {'fname': 'reza', 'lname': 'mobaraki'}


schema = graphene.Schema(query=Query)
result = schema.execute("""
    {
        ps {
            fullName
        }
    }
""")

print(result.data)
print(result.errors)
