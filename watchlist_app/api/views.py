from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle
#from rest_framework.decorators import api_view

from watchlist_app.api.permissions import IsReviewUserOrReadOnly, IsAdminOrReadOnly
from watchlist_app.models import StreamPlatform, WatchList, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer

# class ThrottleView(APIView):
#     throttle_classes = [UserRateThrottle]

#     def get(self, request, format=None):
#         content = {
#             'status': 'request was permitted'
#         }
#         return Response(content)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(Watchlist = movie, review_user = review_user)
        
        if review_queryset.exists():
            raise ValidationError("You already reviewed this movie!")
        
        if movie.Avg_rating == 0:
            movie.Avg_rating = serializer.validated_data['Rating']
        else:
            movie.Avg_rating = (movie.Avg_rating + serializer.validated_data['Rating'])
        
        movie.Number_rating = movie.Number_rating + 1
        movie.save()
                
        serializer.save(Watchlist = movie, review_user = review_user)
class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(Watchlist = pk)
        
    
    
class ReviewDetail( generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors) 
    
class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk = pk)
        except WatchList.DoesNotExist: 
            return Response({'Error' : 'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND) 
          
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk = pk)
        except WatchList.DoesNotExist: 
            return Response({'Error' : 'MOVIE NOT FOUND'}, status=status.HTTP_404_NOT_FOUND) 
          
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, pk):
        try:
            movie = WatchList.objects.get(pk = pk)
        except WatchList.DoesNotExist: 
            return Response({'Error' : 'MOVIE NOT FOUND'}, status=status.HTTP_404_NOT_FOUND) 
          
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StreamplatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    

class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        Platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(Platform, many = True, context ={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors) 

class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            Platform = StreamPlatform.objects.get(pk = pk)
        except StreamPlatform.DoesNotExist: 
            return Response({'Error' : 'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND) 
          
        serializer = StreamPlatformSerializer(Platform, context = {'request':request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            Platform = StreamPlatform.objects.get(pk = pk)
        except StreamPlatform.DoesNotExist: 
            return Response({'Error' : 'PLATFORM NOT FOUND'}, status=status.HTTP_404_NOT_FOUND) 
          
        serializer = StreamPlatformSerializer(Platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, pk):
        try:
            Platform = StreamPlatform.objects.get(pk = pk)
        except StreamPlatform.DoesNotExist: 
            return Response({'Error' : 'PLATFORM NOT FOUND'}, status=status.HTTP_404_NOT_FOUND) 
          
        Platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#@api_view(['GET', 'POST'])
#def movie_list(request):
    
    #if request.method == 'GET':  
       # movies = Movie.objects.all()
        #serializer = MovieSerializer(movies, many = True)
        #return Response(serializer.data)
    
    #if request.method == 'POST':
        #serializer = MovieSerializer(data = request.data)
        #if serializer.is_valid():
            #serializer.save()
            #return Response(serializer.data)
        #else:
            #return Response(serializer.errors) 
  
#@api_view(['GET', 'PUT', 'DELETE'])
#def movie_detail(request, pk):
    
    #if request.method == 'GET':
        
        #try:
            #movie = Movie.objects.get(pk = pk)
        #except Movie.DoesNotExist: 
            #return Response({'Error' : 'MOVIE NOT FOUND'}, #status=status.HTTP_404_NOT_FOUND) 
          
        #serializer = MovieSerializer(movie)
        #return Response(serializer.data)
    
    #if request.method == 'PUT':
        #movie = Movie.objects.get(pk=pk)
        #serializer = MovieSerializer(movie, data=request.data)
        #if serializer.is_valid():
            #serializer.save()
            #return Response(serializer.data)
        #else:
            #return Response(serializer.errors, status=status.#HTTP_400_BAD_REQUEST)

    #if request.method == 'DELETE':
          #movie = Movie.objects.get(pk=pk)
          #movie.delete()
          #return Response(status=status.HTTP_204_NO_CONTENT) 
