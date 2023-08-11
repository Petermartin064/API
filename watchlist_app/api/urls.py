from django.urls import path
# from watchlist_app.api.views import movie_list, movie_detail
from watchlist_app.api.views import MovieListAV, MovieDetailAV
 
urlpatterns = [
    path('list/', MovieListAV.as_view(), name='movie-list'),
    path('<int:pk>', MovieDetail.as_view(), name='movie-detail'),
]
 