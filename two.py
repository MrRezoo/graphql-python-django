import graphene
import uuid
from datetime import datetime


class User(graphene.ObjectType):
    id = graphene.ID(default_value=uuid.uuid4())
    username = graphene.String()
    create_time = graphene.DateTime(default_value=datetime.now())


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()

    def mutate(self, info, **kwargs):
        user = User(username=kwargs['username'])
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(mutation=Mutation, auto_camelcase=False)
result = schema.execute("""
    mutation{
        create_user(username:"reza"){
            user{
                id
                username
                create_time
            }
        }
    }

""")

print(result)