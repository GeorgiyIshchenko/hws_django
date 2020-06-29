from rest_framework import serializers
from .models import Article
from django.db.models.fields import*
from django.contrib.auth.models import User

class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    body = serializers.CharField()
    date = serializers.CharField()
    author= serializers.CharField()
    published_date=serializers.CharField()


    def create(self, validated_data):
        title=validated_data.get('title')
        body = validated_data.get('body')
        date = validated_data.get('date')
        published_date=validated_data.get('published_date')
        users=User.objects.all()
        for i in users:
            if i.username==validated_data.get('author'):
                author = i
        return Article.objects.create(title=title,body=body,date=date,author=author,published_date=published_date)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.date = validated_data.get('date', instance.date)
        users=User.objects.all()
        for i in users:
            if i.username==validated_data.get('username',instance.author):
                instance.author = i
        instance.published_date=validated_data.get('published_date',instance.published_date)
        instance.save()
        return instance

class UserSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=16)
    email=serializers.EmailField()
    password=serializers.CharField(min_length=8)

    def create(self,validated_data):
        username=validated_data.get('username')
        email=validated_data.get('email')
        password=validated_data.get('password')
        return User.objects.create_user(username=username,email=email,password=password)

    def update(self,instance,validated_data):
        instance.username=validated_data.get('username',instance.username)
        instance.email=validated_data.get('email',instance.email)
        instance.password=validated_data.get('password',instance.password)
        instance.save()
        return instance

