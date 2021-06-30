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

    @staticmethod
    def resolve_persons(parent, info, **kwargs):
        return Person.objects.all()

    @staticmethod
    def resolve_cars(parent, info, **kwargs):
        return Car.objects.all()