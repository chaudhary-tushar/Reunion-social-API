from rest_framework import serializers

from .models import Post,Profile,User

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    class Meta :
        model = Profile
        fields =['username','count_followers','count_following']
    
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=['Post_id','title','description','created_at']
        
class All_serializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields = ['Post_id','title','description','created_at','comments','count_likes']

        
        
class GetpostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['Post_id','count_likes','count_comments']
        