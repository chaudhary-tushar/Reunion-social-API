from rest_framework.response import Response
from django.http import HttpResponse
from .models import Profile,Post,Comments
from .serializers import ProfileSerializer,PostSerializer,All_serializer,GetpostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication



# Create your views here.

def index(request):
    return HttpResponse("Welcome to Social Api")

#done follow user
class Follow(APIView):
    """POST /api/follow/{id} authenticated user would follow user with {id}"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,id):
        follower =Profile.objects.get(user=request.user)
        #id = int(request.data['id'])
        id=id
        
        try:
            following = Profile.objects.get(id_user=id)
        except :
            return Response({"error": f"User with id_user {id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        
        if id == follower.id_user:
            return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
        elif following.user.username in follower.following:
            return Response({'detail': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            follower.following.append(following.user.username)
            follower.count_following += 1
            follower.save()
            
            # Add the follower to the followed user's followers list
            following.followers.append(follower.user.username)
            following.count_followers += 1
            following.save()
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": f"You are now following user with id {id}"}, status=status.HTTP_201_CREATED)
  
        
#done unfollow user
class UnFollow(APIView):
    """POST /api/unfollow/{id} authenticated user would unfollow a user with {id}"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,id):
        follower =Profile.objects.get(user=request.user)
        # id = int(request.data['id'])
        id=id
        
        
        try:
            following = Profile.objects.get(id_user=id)
        except :
            return Response({"error": f"User with id_user {id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if id == follower.id_user:
            return Response({"error": "You cannot unfollow yourself"}, status=status.HTTP_400_BAD_REQUEST)
        elif following.user.username not in follower.following:
            return Response({'detail': 'You are already not following this user'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            follower.following.remove(following.user.username)
            follower.count_following -= 1
            follower.save()

            # Add the follower to the followed user's followers list
            following.followers.remove(follower.user.username)
            following.count_followers -= 1
            following.save()
        except Exception as e:
            print(str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": f"You have now unfollowed user with id {id}"}, status=status.HTTP_201_CREATED)
        
        
# done hexadecimal url problem
class Like(APIView):
    """POST /api/like/{id} would like the post with {id} by the authenticated user."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,id):
        id=id
        user=request.user
        
        try:
            getpost=Post.objects.get(Post_id=id)
        except:
            return Response({"error": f"Post with {id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if user.username in getpost.likes:
            return Response({"error": "You have already liked it ."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            getpost.likes.append(user.username)
            getpost.count_likes+=1
            getpost.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"success": f"You have now liked post with id {id}"}, status=status.HTTP_201_CREATED)         
   
        
# done hexadecimal url problem
class Unlike(APIView):
    """POST /api/unlike/{id} would unlike the post with {id} by the authenticated user."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,id):
        id=id
        user=request.user
        
        try:
            getpost=Post.objects.get(Post_id=id)
        except:
            return Response({"error": f"Post with {id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if user.username  not in getpost.likes:
            return Response({"error": "You have already unliked it ."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            getpost.likes.remove(user.username)
            getpost.count_likes-=1
            getpost.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"success": f"You have now unliked post with id {id}"}, status=status.HTTP_201_CREATED)


#done post a post
class Postit(APIView):
    """- POST api/posts/ would add a new post created by the authenticated user.
    - Input: Title, Description
    - RETURN: Post-ID, Title, Description, Created Time(UTC)."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        user=request.user
        title=request.data['title']
        description=request.data['description']
        new_post=Post.objects.create(user=user.username,title=title,description=description)
        new_post.save()
        serializer=PostSerializer(new_post)
        return Response(serializer.data,status.HTTP_201_CREATED)


#done
class Comment(APIView):
    """- POST /api/comment/{id} add comment for post with {id} by the authenticated user.
    - Input: Comment
    - Return: Comment-ID"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,id):
        user=request.user
        id=id
        comment=request.data['comment']
        try:
            getpost=Post.objects.get(Post_id=id)
        except:
            return Response({"error": f"Post with {id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        new_comment=Comments.objects.create(comment=comment)
        new_comment.save()
        
        getpost.comments.append({user.username:comment})
        getpost.count_comments+=1
        getpost.save()
        return Response({'Comment-Id':new_comment.commentid },status=status.HTTP_201_CREATED)
        


#done get and delete operations on post
class Get_Post(APIView):
    """GET api/posts/{id} would return a single post with {id} 
    populated with its number of likes and comments
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,id):
        user=request.user
        post_id=id
        try:
            getpost=Post.objects.get(Post_id=post_id)
            serializer=GetpostSerializer(getpost)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            
            
    def delete(self,request,id):
        user=request.user
        try:
            getpost=Post.objects.get(Post_id=id)
            if user.username==getpost.user:
                getpost.delete()
                
                return Response({"message":"Post with {id} deleted"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


#done get authenticated user
class Get_user(APIView):
    """- GET /api/user should authenticate the request and return the respective user profile.
    - RETURN: User Name, number of followers & followings.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        profile=Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


#done get all post of the authenticated user
class All_Post(APIView):
    """- id: ID of the post
- title: Title of the post
- desc: Description of the post
- created_at: Date and time when the post was created
- comments: Array of comments, for the particular post
- likes: Number of likes for the particular post"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        user = request.user
        allpost=Post.objects.filter(user=user.username)
        serializer=All_serializer(allpost,many=True)
        return Response(serializer.data)
