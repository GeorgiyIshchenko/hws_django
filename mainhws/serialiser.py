from rest_framework import serializers

from .models import Article

class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    body = serializers.CharField()
    date = serializers.CharField()
    slug = serializers.CharField()

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.date = validated_data.get('date', instance.date)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance