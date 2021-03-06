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


class CarInput(graphene.InputObjectType):
    # person_id = graphene.Int()
    persons_id = graphene.List(graphene.ID)
    name = graphene.String()
    year = graphene.Int()


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


class UpdatePerson(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        input = PersonInput()

    person = graphene.Field(PersonType)
    ok = graphene.Boolean(default_value=False)

    @staticmethod
    def mutate(parent, info, id, input=None):
        person_instance = Person.objects.get(id=id)
        person_instance.name = input.name if input.name is not None else person_instance.name
        person_instance.age = input.age if input.age is not None else person_instance.age
        person_instance.save()
        ok = True
        return UpdatePerson(person=person_instance, ok=ok)


class DeletePerson(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    person = graphene.Field(PersonType)
    ok = graphene.Boolean(default_value=False)

    @staticmethod
    def mutate(parent, info, id):
        person_instance = Person.objects.get(id=id)
        person_instance.delete()
        ok = True
        return DeletePerson(person=person_instance, ok=ok)


class CreateCar(graphene.Mutation):
    class Arguments:
        input = CarInput()

    car = graphene.Field(CarType)
    ok = graphene.Boolean(default_value=False)

    # @staticmethod
    # def mutate(parent, info, input=None):
    #     person_instance = Person.objects.get(id=input.person_id)
    #     car_instance = Car.objects.create(person=person_instance, name=input.name, year=input.year)
    #     ok = True
    #     return CreateCar(car=car_instance, ok=ok)

    @staticmethod
    def mutate(parent, info, input=None):
        persons_list = list()
        for person_id in input.persons_id:
            person_instance = Person.objects.get(id=person_id)
            persons_list.append(person_instance)

        car_instance = Car.objects.create(name=input.name, year=input.year)
        car_instance.person.set(persons_list)
        ok = True
        return CreateCar(car=car_instance, ok=ok)


class Mutate(graphene.ObjectType):
    create_person = CreatePerson.Field()
    update_person = UpdatePerson.Field()
    delete_person = DeletePerson.Field()

    create_car = CreateCar.Field()
