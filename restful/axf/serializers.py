from rest_framework import serializers
from axf.models import SlideShow,Product,Maindescription,CategorieGroup,Childgroup,User,Order,Address,Cart
class SlideShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlideShow
        fields = ("name","img","sort","trackid")

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model =Product
        fields =("name","productId","longName","storeNums","specifics","sort","marketPrice","price","categoryId","childCid","img","keywords","brandId","brandName","safeDay","safeUnit","safeUnitDesc")


class MaindescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maindescription
        fields = ("categoryID","categoryName","sort","img","product1","product2","product3")






class CategorieGroupSerializer(serializers.ModelSerializer):
    class Meta:
       model = CategorieGroup
       fields =("name","categorieID","sort")
class ChildgroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Childgroup
        fields = ("cid","name","sort","categorie")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phoneNum","tokenValue","headImg","integral","vipLevel","createTime","lastLoginTim")
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("name","sex","phoneNum","postCode","address","province","city","county","street","detailAddress","user")

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ("user","product","order","num")

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("orderId","user","address","price","flag","createTime","lastTime")