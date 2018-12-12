from django.db import models

#外卖员信息
class FastFood(models.Model): 
    phone=models.CharField(max_length=11,primary_key=True)
    Name=models.CharField(max_length=12) 
    imgs=models.CharField(max_length=100,default=None)
    imgs_1=models.CharField(max_length=100,default=None)
    password=models.CharField(max_length=10)
    sty=models.CharField(max_length=2,default='0') #是否验证
    StudentToken=models.CharField(max_length=300)
    def __str__(self):
       return self.phone

#商家
class Shop(models.Model):
    ShopName=models.CharField(max_length=12,primary_key=True)
    Shop_Img=models.CharField(max_length=2,default='1')
    addres=models.CharField(max_length=30)
    Shop_text=models.TextField(default="")
    m=models.CharField(max_length=5)
    fraction=models.CharField(max_length=4,default='3.0')

#账单
class Bill(models.Model):
    billId=models.AutoField(primary_key=True) #订单编号
    FastPhon_id=models.CharField(max_length=30,default=None) #外卖人
    shop_name=models.ForeignKey('Shop',on_delete=models.CASCADE)
    addres=models.CharField(max_length=30) #买家地址
    date= models.CharField(max_length=10) #日期
    apm=models.CharField(max_length=6)   #上下午
    money=models.IntegerField()     #每单的钱
    sty=models.CharField(max_length=2,default='0') #是否接单 0没有接单 1接单
    Get=models.CharField(max_length=2,default='0')#是否提钱 0没有提 1提

#注册短信
class Authentication(models.Model):
    phone=models.CharField(max_length=11,primary_key=True)
    number=models.CharField(max_length=6)
    sty=models.CharField(max_length=3)


		




