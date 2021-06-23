import graphene
from graphene import String


class Query(graphene.ObjectType):
    name = graphene.String(username=String(default_value='world'))
    is_admin = graphene.Boolean()

    def resolve_name(self, info, username):
        return f"Hello User - {username}"

    def resolve_is_admin(self, info):
        return True


schema = graphene.Schema(query=Query, auto_camelcase=False)
result = schema.execute("""
    query {
        name(username:"reza")
        is_admin
    }

""")

print(result.data)
print(result.errors)
