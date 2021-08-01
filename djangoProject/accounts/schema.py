import graphene
import graphql_jwt
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType, ObjectType
from graphql_jwt.decorators import login_required


class UserType(DjangoObjectType):
    class Meta:
        model = User


class AccountsQuery(ObjectType):
    user = graphene.Field(UserType, id=graphene.ID())

    @login_required
    @staticmethod
    def resolve_user(parent, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("you are not logged in")
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
        input = UserInput(required=True)

    ok = graphene.Boolean(default_value=False)
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(parent, info, input=None):
        user_instance = User.objects.create_user(input.username, input.email, input.password)
        ok = True
        return CreateUser(user=user_instance, ok=ok)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
