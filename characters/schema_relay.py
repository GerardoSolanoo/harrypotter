import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Character, Vote


#1
class CharacterFilter(django_filters.FilterSet):
    class Meta:
        model = Character
        fields = ['name', 'lastname', 'house', 'age', 'patronus']


#2
class CharacterNode(DjangoObjectType):
    class Meta:
        model = Character
        #3
        interfaces = (graphene.relay.Node, )


class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (graphene.relay.Node,)


class RelayQuery(graphene.ObjectType):
    #4
    relay_character = graphene.relay.Node.Field(CharacterNode)
    #5
    relay_character = DjangoFilterConnectionField(CharacterNode, filterset_class=CharacterFilter)

class RelayCreateCharacter(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterNode)

    class Input:
        name = graphene.String()
        lastname = graphene.String()
        house = graphene.String()
        age = graphene.Int()
        patronus = graphene.String()
        description = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user or None

        character = Character(
            name=input.get('name'),
            lastname=input.get('lastname'),
            house=input.get('house'),
            age=input.get('age'),
            patronus=input.get('patronus'),
            description=input.get('description'),
            posted_by=user,
        )
        character.save()

        return RelayCreateCharacter(character=character)


class RelayMutation(graphene.AbstractType):
    relay_create_character = RelayCreateCharacter.Field()