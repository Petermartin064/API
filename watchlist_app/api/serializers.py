from rest_framework import serializers
from watchlist_app.models import StreamPlatform, WatchList, Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('Watchlist',)
        # fields = '__all__'

class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        platform_id = representation['Platform']
        platform_name = StreamPlatform.objects.get(id=platform_id).Name
        representation['Platform'] = platform_name
        return representation


        
    
class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    WatchList = WatchListSerializer(many = True, read_only = True)
    class Meta:
        model = StreamPlatform
        fields = '__all__'
        
# def name_Length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name must be at least 2 characters long")
    
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only = True)
#     name = serializers.CharField(validators=[name_Length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()   
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data) 
    
#     def update(self, instance, validated_data,):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     #Object level validation
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and Description cannot be the same")
#         return data
    
    # #Field level validation
    # def validate_name(self, value):
    # if len(value) < 2:
    #     raise serializers.ValidationError("Name must be at least 2 characters long")
    # else:
    #     return value