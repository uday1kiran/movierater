from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Movie,Rating

# Create your views here.
from .serializers import MovieSerializer, RatingSerializer


class MovieViewSet(viewsets):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=True,methods=['POST'])
    def rate_movie(self,request,pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars=request.data['stars']
            user=request.user
            try:
                rating = Rating.objects.get(user=user.id,movie=movie.id)
                rating.stars=stars
                rating.save()
                serializer=RatingSerializer(rating,many=False)
                response = {'message': 'Rating updated','result':serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating=Rating.objects.create(user=user,movie=movie,stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'You need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer