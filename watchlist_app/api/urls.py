from django.urls import include, path
from rest_framework.routers import DefaultRouter
# from watchlist_app.api.views import movie_list, movie_detail
from watchlist_app.api.views import (
    WatchListAV, 
    WatchDetailAV, 
    StreamPlatformAV, 
    ReviewDetail,                          
    ReviewList,
    ReviewCreate,
    StreamplatformVS,
    UserReview,
    WatchListSF
    )
 
router = DefaultRouter()
router.register('stream', StreamplatformVS, basename ='streamplatform')
 
urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('lists/', WatchListSF.as_view(), name='movie-lists'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='movie-detail'),
    # path('stream/', StreamPlatformAV.as_view(), name='stream'),
    path('', include(router.urls)),
    path('<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('<int:pk>/createreview/', ReviewCreate.as_view(), name='review-create'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('review/', UserReview.as_view(), name='user-review'),
]
 