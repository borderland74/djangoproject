from django.shortcuts import render

# Create your views here.
from axf.models import SlideShow,Product,Maindescription,CategorieGroup,Childgroup,User,Order,Address,Cart
from axf.serializers import SlideShowSerializer,ProductSerializer,MaindescriptionSerializer,CategorieGroupSerializer,ChildgroupSerializer,UserSerializer,OrderSerializer,AddressSerializer,CartSerializer
# from rest_framework import mixins
from rest_framework import generics

class Slideshows(generics.ListAPIView):
    queryset = SlideShow.objects.all()
    serializer_class = SlideShowSerializer

