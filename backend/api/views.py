from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .serializers import *
from todo.models import Todo
class TodoList(generics.ListAPIView):
# ListAPIView requires two mandatory attributes, serializer_class and
# queryset.
# We specify TodoSerializer which we have earlier implemented
    serializer_class = TodoSerializer
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')



class TodoListCreate(generics.ListCreateAPIView):
# ListAPIView requires two mandatory attributes, serializer_class and
# queryset.
# We specify TodoSerializer which we have earlier implemented
    serializer_class = TodoSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')

    def perform_create(self, serializer):
        #serializer holds a django model
      serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        # user can only update, delete own posts
        return Todo.objects.filter(user=user)


class TodoToggleComplete(generics.UpdateAPIView):
    serializer_class = TodoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)
    def perform_update(self,serializer):
        serializer.instance.completed=not(serializer.instance.completed)
        serializer.save()


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request) # data is a dictionary
            user = User.objects.create_user(
            username=data['username'],
            password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)},status=201)
        except IntegrityError:
            return JsonResponse(
               {'error':'username taken. choose another username'},
              status=400)

            