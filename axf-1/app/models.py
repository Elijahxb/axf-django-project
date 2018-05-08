from django.db import models

# Create your models here.


class Main(models.Model):
    img = models.CharField(max_length=200)  # 图片
    name = models.CharField(max_length=100)  # 名称
    trackid = models.CharField(max_length=16)  # 通用id

    class Meta:
        abstract = True


class MainWheel(Main):
    # 轮循 banner
    class Meta:
        db_table = 'axf_wheel'


class MainNav(Main):
    # 导航
    class Meta:
        db_table = 'axf_nav'


class MainMustBuy(Main):
    # 必购
    class Meta:
        db_table = 'axf_mustbuy'


class MainShop(Main):
    # 商店
    class Meta:
        db_table = 'axf_shop'


# 主要商品
class MainShow(Main):
    '''
    编号 id
    分类名称 name
    分类图片 img
    图片1 img1
    名称1 longname1
    优惠价格1 price1
    原始价格1 marketprice1
    图片2 img2
    名称2 longname2
    优惠价格2 price2
    原始价格2 marketprice2
    图片3 img3
    名称3 longname3
    优惠价格3 price3
    原始价格3 marketprice3
    '''
    categoryid = models.CharField(max_length=16)
    brandname = models.CharField(max_length=100)
    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=16)
    productid1 = models.CharField(max_length=16)
    longname1 = models.CharField(max_length=100)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=1)
    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=16)
    productid2 = models.CharField(max_length=16)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=1)
    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=16)
    productid3 = models.CharField(max_length=16)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=1)

    class Meta:
        db_table = 'axf_mainshow'


# 左侧类型表
class FoodType(models.Model):
    typeid = models.CharField(max_length=16)
    typename = models.CharField(max_length=100)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    '''
    编号       id            integer
    商品id     productid    integer
    商品图片   productimg
    商品名称   productname
    商品规格   productlongname
    规格      specifics
    折后价格   price
    原价       marketprice
    分类id     categoryid
    子分类id     childcid
    子id名称     childcidname
    排序       storenums
    销量       productnum
    '''
    productid = models.CharField(max_length=16)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=100)
    productlongname = models.CharField(max_length=200)
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=1)
    categoryid = models.CharField(max_length=16)
    childcid = models.CharField(max_length=16)
    childcidname = models.CharField(max_length=100)
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_goods'


class UserModel(models.Model):
    '''
    username   名称
    password   密码
    email      邮箱
    sex        性别
    icon       头像
    is_delete  是否删除
    '''
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64, unique=True)
    sex = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='icons')
    is_delete = models.BooleanField(default=False)
    ticket = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'axf_users'


# 购物车
class CartModel(models.Model):
    '''
    user   关联用户
    goods  关联商品
    c_num  商品个数
    is_select  是否选择商品
    '''
    user = models.ForeignKey(UserModel)
    goods = models.ForeignKey(Goods)
    c_num = models.IntegerField(default=1)
    is_select = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'


class OrderModel(models.Model):
    '''
    user       关联用户
    o_num      数量
    o_status   状态
    o_create   订单创建时间
    '''
    user = models.ForeignKey(UserModel)
    o_num = models.CharField(max_length=64)
    # 0代表已下单，但是未付款，1已付款未发货，2已付款已发货
    o_status = models.IntegerField(default=0)
    o_create = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'axf_order'


class OrderGoodsModel(models.Model):
    '''
    goods     关联的商品
    order     关联的订单
    good_num  商品的个数
    '''
    goods = models.ForeignKey(Goods)
    order = models.ForeignKey(OrderModel)
    goods_num = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_order_goods'

