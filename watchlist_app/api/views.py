from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
#from rest_framework.decorators import api_view

from watchlist_app.models import StreamPlatform, WatchList, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        serializer.save(Watchlist = movie)
         
class ReviewList(generics.ListAPIView):
    
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(Watchlist = pk)
        
    
    
class ReviewDetail( generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class WatchListAV(APIView):

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
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
<<<<<<< HEAD
# class StreamplatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True, context ={'request':request})
#         return Response(serializer.data)

#     def retrieve(self, request, pk):
#         queryset = StreamPlatform.objects.all()
#         Watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(Watchlist, context ={'request':request})
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors) 

=======
    
class StreamplatformVS(viewsets.ViewSet):
    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True, context ={'request':request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        Watchlist = get_object_or_404(queryset, pk=pk, context ={'request':request})
        serializer = StreamPlatformSerializer(Watchlist)
        return Response(serializer.data)
>>>>>>> d0050c47d127061fed648010edb9b1b0664a70c3

class StreamPlatformAV(APIView):
    
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
