from django.urls import path
# from watchlist_app.api.views import movie_list, movie_detail
from watchlist_app.api.views import WatchListAV, WatchDetailAV, StreamPlatformAV
 
urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>', WatchDetailAV.as_view(), name='movie-detail'),
    path('stream', StreamPlatformAV.as_view(), name='stream'),
    path('<int:pk>', StreamPlatformAV.as_view(), name='stream-detail'),
]
 