import graphene
from graphene import String


class Query(graphene.ObjectType):
    name = graphene.String(username=String(default_value='world'))

    def resolve_name(self, info, username):
        return f"Hello {username}"


schema = graphene.Schema(query=Query, auto_camelcase=False)
result = schema.execute("""
    query ($user:String){
        name(username:$user)
    }
""", variables={'user': 'reza'})

print(result.data)
print(result.errors)
