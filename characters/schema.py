import graphene
from graphene_django import DjangoObjectType
from .models import Character
from users.schema import UserType
from characters.models import Vote
from graphql import GraphQLError
from django.db.models import Q

class CharacterType(DjangoObjectType):
    class Meta:
        model = Character

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class CreateCharacter(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    lastname = graphene.String()
    house = graphene.String()
    age = graphene.Int()
    patronus = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        name = graphene.String()
        lastname = graphene.String()
        house = graphene.String()
        age = graphene.Int()
        patronus = graphene.String()
        description = graphene.String()

    def mutate(self, info, name, lastname, house, age, patronus, description=None):
        user = info.context.user

        if not user.is_authenticated:
            raise GraphQLError('You must be logged in to create a character!')

        character = Character(
            name=name,
            lastname=lastname,
            house=house,
            age=age,
            patronus=patronus,
            description=description or "",
            posted_by=user,
        )
        character.save()

        return CreateCharacter(
            id=character.id,
            name=character.name,
            lastname=character.lastname,
            house=character.house,
            age=character.age,
            patronus=character.patronus,
            description=character.description,
            posted_by=user,
       )


class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    character = graphene.Field(CharacterType)

    class Arguments:
        character_id = graphene.Int()

    def mutate(self, info, character_id):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError('You must be logged in to vote!')

        character = Character.objects.filter(id=character_id).first()
        if not character:
            raise Exception('Invalid Character!')

        Vote.objects.create(
            user=user,
            character=character,
        )

        return CreateVote(user=user, character=character)

class Query(graphene.ObjectType):
    characters = graphene.List(
        CharacterType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    votes = graphene.List(VoteType)

    def resolve_characters(self, info, search=None, first=None, skip=None, **kwargs):
        qs = Character.objects.all()

        if search:
            filter = (
                Q(name__icontains=search) |
                Q(lastname__icontains=search) |
                Q(house__icontains=search) |
                Q(patronus__icontains=search) |
                Q(description__icontains=search)
            )
            qs = qs.filter(filter)
        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

class Mutation(graphene.ObjectType):
    create_character = CreateCharacter.Field()
    create_vote = CreateVote.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
