import graphene
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType, ObjectType


class UserType(DjangoObjectType):
    class Meta:
        Model = User


class AccountsQuery(ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())

    @staticmethod
    def resolve_user(parent, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return User.objects.get(id=id)
        return None


class UserInput(graphene.InputObjectType):
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(Required=True)

    ok = graphene.Boolean(default_value=False)
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(parent, info, input=None):
        user_instance = User.objects.create_user(input.username, input.email, input.password)
        ok = True
        return CreateUser(user=user_instance, ok=ok)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
