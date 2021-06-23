import graphene
import uuid
from datetime import datetime


class User(graphene.ObjectType):
    id = graphene.ID(default_value=uuid.uuid4())
    username = graphene.String()
    create_time = graphene.DateTime(default_value=datetime.now())


class UserInput(graphene.InputObjectType):
    username = graphene.String(required=True)


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        user_data = UserInput()

    def mutate(self, info, user_data=None):
        user = User(username=user_data.username)
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(mutation=Mutation, auto_camelcase=False)
result = schema.execute("""
    mutation{
        create_user(user_data:{
            username:"mr.rezoo"
        }){
            user{
                id
                username
                create_time
            }
        }
    }

""")

print(result)
