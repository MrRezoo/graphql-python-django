import graphene
from graphene import String


class Query(graphene.ObjectType):
    name = graphene.String(username=String(default_value='world'))

    def resolve_name(self, info, username):
        return f"Hello {info.context.get('username')}"


schema = graphene.Schema(query=Query, auto_camelcase=False)
result = schema.execute("""
    query{
        name
    }
""", context={'username': 'reza'})

print(result.data)
