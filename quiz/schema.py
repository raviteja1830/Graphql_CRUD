import graphene
from graphene_django import DjangoObjectType,DjangoListField
from .models import *



class CategoryType(DjangoObjectType):
    class Meta:
        model=Category
        fields=("id","name")


class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id","title","category")


class QuestionType(DjangoObjectType):
    class Meta:
        model=Question
        fields=("title","quiz")

class AnswerType(DjangoObjectType):
    class Meta:
        model=Answer
        fields=("question","answer_text")


class Query(graphene.ObjectType):
    all_quizzes = graphene.Field(QuizzesType,id=graphene.Int())

    def resolve_all_quizzes(root,info,id):
        return Quizzes.objects.get(pk=id)

class CategoryAddMutation(graphene.Mutation):
    
    class Arguments:
        name=graphene.String(required=True)
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls,root,info,name):
        category = Category(name=name)
        category.save()
        return CategoryAddMutation(category=category)

class CategoryUpdateMutation(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls,root,info,id,name):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return CategoryUpdateMutation(category=category)


class CategoryDeleteMutation(graphene.Mutation):
    
    class Arguments:
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls,root,info,id):
        category = Category.objects.get(id=id)
        category.delete()
        return

class Mutation(graphene.ObjectType):
    Add_category = CategoryAddMutation.Field()
    Update_category = CategoryUpdateMutation.Field()
    Delete_category = CategoryDeleteMutation.Field()



schema = graphene.Schema(query=Query,mutation=Mutation)
