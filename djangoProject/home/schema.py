import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Person, Car


class PersonType(DjangoObjectType):  # something like serialize in django rest framework
    class Meta:
        model = Person


class CarType(DjangoObjectType):
    class Meta:
        model = Car


class HomeQuery(ObjectType):
    persons = graphene.List(PersonType)
    cars = graphene.List(CarType)
    person = graphene.Field(PersonType, name=graphene.String())
    car = graphene.Field(CarType, id=graphene.Int())

    @staticmethod
    def resolve_persons(parent, info, **kwargs):
        return Person.objects.all()

    @staticmethod
    def resolve_cars(parent, info, **kwargs):
        return Car.objects.all()

    @staticmethod
    def resolve_person(parent, info, **kwargs):
        person_name = kwargs.get('name')
        if person_name is not None:
            return Person.objects.get(name=person_name)
        return None

    @staticmethod
    def resolve_car(parent, info, **kwargs):
        car_id = kwargs.get('id')
        if car_id is not None:
            return Car.objects.get(id=car_id)
        return None


class PersonInput(graphene.InputObjectType):
    name = graphene.String()
    age = graphene.Int()


class CreatePerson(graphene.Mutation):
    class Arguments:
        input = PersonInput(required=True)

    # show response
    person = graphene.Field(PersonType)
    ok = graphene.Boolean(default_value=False)

    @staticmethod
    def mutate(parent, info, input=None):
        person_instance = Person.objects.create(name=input.name, age=input.age)
        # show response
        return CreatePerson(person=person_instance, ok=True)


class Mutate(graphene.ObjectType):
    create_person = CreatePerson.Field()
