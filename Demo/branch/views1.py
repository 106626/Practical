from django.shortcuts import render,HttpResponse
from branch import models
from branch.models import FastFood,Shop,Bill,Authentication

#该类对密码 token 加/解密 创建数据保存在数据库中
import hashlib
from django.core import signing
class Password_module:
    # TIME_OUT=30*60 #30min
    HEADER={'typ':'JWP','alg':'default'}
    KEY='JUST_16_JXJ_F'
    SALT='WWW.Kind.cn'
    def __init__(self,phone):
        self.phone=phone

    def jia_mi(self,cls):#加密
         value=signing.dumps(cls,key=self.KEY,salt=self.SALT)
         mima=signing.b64_encode(value.encode()).decode()
         return mima    

    def jie_mi(self,cls):#解密
        s=signing.b64_decode(cls.encode()).decode()
        jie_mi=signing.loads(s,key=self.KEY,salt=self.SALT)
        return jie_mi
         
    def create_db(self):#创建 
        header=self.jia_mi(self.HEADER)
        body={"number":self.phone}#token信息
        body=self.jia_mi(body)      
        md5=hashlib.md5() #md5加密
        md5.update(("%s.%s" % (header,body)).encode())
        lat=md5.hexdigest()#16进制
        token="%s.%s.%s"%(header,body,lat)
        return token

    def  get_token(self,token):
        paylode=str(token).split('.')[1]
        paylode=self.jie_mi(paylode)
        return paylode

    def checkToken(self,token): #检查token
        try:
            phone=self.get_token(token)
            print(phone)
            return phone["number"] 
        except:
            return 0



#发送短信API 
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
class ShortMessageAPI:
     appid = 1400112426
     appkey = "e8100999c3d47a649e25ce678202825e"

     def __init__(self,template_id,number,content):
       self.template_id=template_id
       self.number=number
       self.content=content

     def send(self):
        ssender = SmsSingleSender(self.appid, self.appkey)
        params = [self.content]
        result = ssender.send_with_param(86, self.number,self.template_id, params, sign="两人随纪", extend="", ext="")



#识别是否为人脸 接口2代
from aip import AipFace
class FaceAPI:
    APP_ID='10890686'
    API_KEY='fYGS3GkmhQ0E0iELBS1dZWkY'
    SECRET_KEY='tEz5IptAAwG27tNn4itrBGW0uXurgU3N'
    def __init__(self,filePath):
         self.filePath=filePath

    def get_file_content(self):
        with open(self.filePath, 'rb') as fp:
            return fp.read()

    def return_face(self):
        options = {'max_face_num': 1, 'face_fields': "age,beauty,expression,faceshape",}
        aipFace = AipFace(self.APP_ID,self.API_KEY,self.SECRET_KEY)
        result = aipFace.detect(self.get_file_content(),options)
        if result['result']==[]:
            return "illegal" #没人脸
        elif   result['result'][0]['face_probability'] >0.7:
            return "res"  #符合
        else:
            return "vague"    #模糊



import requests
import base64
class PhotoID:
  request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
  access_token='24.78008b997a495d0448dc093ef27f812b.2592000.1546491467.282335-10890686'
  def __init__(self,img_1,img_2):
    self.img_1=img_1
    self.img_2=img_2
  def Requ(self):
        with open(self.img_1, "rb") as f:
           
           base64_data = base64.b64encode(f.read())
           f.close()
        with open(self.img_2, "rb") as f:
            base64_data_1 = base64.b64encode(f.read())
            f.close()
        params = json.dumps([{"image": str(base64_data,'utf-8'), "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"},{"image":str(base64_data_1,'utf-8') , "image_type": "BASE64", "face_type": "CERT", "quality_control": "LOW"}])
        url = self.request_url + "?access_token=" + self.access_token
        headers={'Content-Type': 'application/json'}
        response=requests.post(url,data=params,headers=headers)
        content = response.text
        content=json.loads(content)
        print(content)
        if content:
          try:
            if content['result']['score']>89:
              return 1 #成功
            else:
             return 2 #不成功
          except:
             return 3 #可能不是身份证



#天气API
import urllib.request
class Weather:
    key = '0e6229b55b7f48c8a7b1a7a17585c2ab'
    location = '张家港'
    location_name = {'张家港': 'zhangjiagang', '上海': 'shanghai'}
    location_hname = location_name.get(location)
    def __init__(self):
      pass

    def nowtq(self,datanowtq):
        temperature='%s'%(datanowtq['tmp']) #温度
        rain=datanowtq['pcpn'] #不下雨返回0.0
        wind=datanowtq['wind_sc'] #返回几级风
        if rain=='0.0':
           rain='0'
        content=[{"C":temperature,"rain":rain,"wind":wind }]
        return content

    def get_1_json(self):
        url = 'https://free-api.heweather.com/s6/weather/now?location=' + self.location_hname + '&key=' + self.key
        html = urllib.request.urlopen(url).read() 
        hjson = json.loads(html.decode('utf-8'))
        nowtq_status = hjson['HeWeather6'][0]['now']
        return self.nowtq(nowtq_status)




#用户注册时检查手机号是否被注册
def CheckPhon(request):
    if request.method=='POST':
       phone=request.POST.get('phone')
       State=models.Authentication.objects.filter(phone=phone).first()
       if State!=None and State.sty!='0':
           return HttpResponse('1') #已注册
       else:
          return HttpResponse('0')#未注册



#注册发送验证码并保存手机号
#242074 用户登录短信证码{1},
import random
def Information(request): #duanxin Information
 if request.method=='POST':
  phone=request.POST.get('coachid')
  try:
      State=models.Authentication.objects.filter(phone=phone).first()
      number=''
      for i in range(6): 
          ch=chr(random.randrange(ord('0'),ord('9')+1))
          number+=ch
      if State!=None and State.sty=='1': #判断用户的手机在数据库存在 并且注册成功
         return HttpResponse('已注册')
      elif State!=None and State.sty=='0':#该用户输入过手机并获得过验证码但并没有真正注册
                models.Authentication.objects.filter(phone=phone).update(number=number)
                template_id=242074
                content=number
                number=phone
                # send_phone=ShortMessageAPI(template_id,number,content) #发送短信
                # send_phone.send()
                time.sleep(2)
                return HttpResponse(content)
      else: #该用户第一次申请
        models.Authentication.objects.create(phone=phone,number=number,sty='0')
        template_id=242074
        content=number
        number=phone
        # send_phone=ShortMessageAPI(template_id,number,content)
        # send_phone.send()
        time.sleep(2)
        return HttpResponse(content)
  except:
     return HttpResponse('500')
    



#用户注册账号
import os
import base64
from io import *
def register(request): 
    if request.method=='POST':
        possword=request.POST.get('coachpassword') #密码
        yanzhengma=request.POST.get('VerificationCode')  #获取之前发送验证码
        phone=request.POST.get('coachid') #获取之前填写的手机号
        Name=request.POST.get('Name')   #用户的姓名
        file=request.FILES.get('file')  #用户的照片
        State=models.Authentication.objects.filter(phone=phone).first() #检查该手机号系统是否发送过验证码
        if State!=None  : #发送过  无需检查验证码 用户是无法填写验证码 input框写死了
          if State.sty=='0' and len(file)!=0:
              images=[] 
              if not os.path.exists(settings.MEDIA_ROOT):
                  os.makedirs(settings.MEDIA_ROOT)
              extension=os.path.splitext(file.name)[1] #获取文件后缀名
              file_name='{}{}'.format(uuid.uuid4(),extension)#从命名
              file_path='{}{}'.format(settings.MEDIA_ROOT,file_name)#文件路径
              images.append('{}{}'.format(settings.MEDIA_URL,file_name))
              with open (file_path,'wb') as f: #保存图片
                  for c in file.chunks():
                      f.write(c)
                      f.close()
              state=FaceAPI(file_path) #验证照片是否符合人脸
              face=state.return_face()
              print(face)
              if face=='illegal': #
                state="-1" #不是人脸
              elif face=='res': #是人脸
                 models.Authentication.objects.filter(phone=phone).update(sty='1') #j将次号码改为已被注册
                 t=Password_module(phone)#对手机号进行加密
                 token=t.create_db()
                 # #创建骑手数据库
                 print(type(file_path))
                 models.FastFood.objects.create(phone=phone,password=possword,Name=Name,StudentToken=token,imgs=file_path)
                 state=token
              else: #人脸照片模糊
                 state="-2"
              return HttpResponse(state)
          else:#手机号已注册
              state="-3"
              return HttpResponse(state) 
        else:#没有发送验证码
           state="00"
           return HttpResponse(state)   
       




#用于用户快速登录无需检查 token
def   CheckToken(request):#checktoken
    if request.method=='POST':
       token=request.POST.get('token')
       check=Password_module('1') 
       State=check.checkToken(token)
       if State==0: #失败
         return HttpResponse('0')
       else:
        return HttpResponse('1')


              
#用户账号密码登录
def login(request):
  if request.method=='POST':
    try:
      phone=request.POST.get('username')
      password=request.POST.get('password')
    except:
      return HttpResponse("500")
    State=models.FastFood.objects.filter(phone=phone,password=password).first()
    if State!=None:
        return HttpResponse(State.StudentToken) 
    else:
        return HttpResponse("密码错误")
      


#未接的账单查询
import json
from django.core import serializers
import time
def business(request):
  if request.method=='GET':
     day=str(time.strftime("%Y-%m-%d", time.localtime()))
     Time=str(time.strftime("%H:%M",time.localtime()))
     if Time>'12:00':
         apm='下午'
     elif Time<'12:00':
          apm='上午'
     print(day,apm)
     Data=models.Bill.objects.filter(date=day,apm=apm,sty='0').select_related()
     content=[]
     if Data!=[]:
        for i in Data:
          bill_id=i.billId
          Name=i.shop_name.ShopName
          img=i.shop_name.Shop_Img
          addres=i.addres
          m=i.shop_name.m,  #i.外键的属性.外键的属性
          c={"name":Name,"addres":addres,"m":m,"key":bill_id,"img":img}
          content.append(c)
        return HttpResponse(json.dumps(content))
     else:
        return HttpResponse(content)



#骑手抢单
def GrabSingle(request):
  if request.method=='POST':
    goods_token=request.POST.get('token')#获取token
    good_id=request.POST.get('id')#获取账单中的id
    PasswordClass=Password_module('0')#检查token
    phone=PasswordClass.checkToken(goods_token)
    if phone!=0:
       user=models.FastFood.objects.filter(phone=phone).first()
       if user!=None and user.sty=='0':
          return HttpResponse("0") #骑手没有实名验证不能抢单
       else:
           #预防两个人同时抢 先判断
           bill=models.Bill.objects.filter(billId=good_id,sty='0').first() #找这个id的账单  
           if bill!=None:
              models.Bill.objects.filter(billId=good_id).update(sty='1',FastPhon_id=user.phone) 
              return HttpResponse('Success') #成功
           else:
              return HttpResponse('1')#账单被抢
    else:
      return HttpResponse('-1') #伪造的token 
       


#商店的详情页面
def Shopping(request):
   if request.method=='POST':
      shooping_id=request.POST.get('id')
      content=[]
      try:
          #通过订单查看商店的信息
          Data=models.Bill.objects.filter(billId=shooping_id).select_related() 
          if Data!=[]:
             for i in Data:
                name=i.shop_name.ShopName
                img=i.shop_name.Shop_Img
                text=i.shop_name.Shop_text
                fen=i.shop_name.fraction
                addres=i.shop_name.addres
                c={"name":name,"img":img,"text":text,"fen":fen,"addres":addres}
                content.append(c)
             return HttpResponse(json.dumps(content))
          else:
             return HttpResponse(content)
      except:
            return HttpResponse(content)
    


#天气情况/骑手的姓名/骑手余额/骑手今天订单数目/ 
def weather(request):
    if request.method=='POST':
       bill=0 #今日接单数
       name='暂无登录'
       usemoney=0 #余额
       use_token=request.POST.get('token')
       Today=Weather()
       state=Today.get_1_json() #今日天气情况
       checktoken=Password_module('1')
       phone=checktoken.checkToken(use_token) #检查token
       if phone!=0:
          user=models.FastFood.objects.filter(phone=phone)
          name=user[0].Name #骑手名字
          day=str(time.strftime("%Y-%m-%d", time.localtime())) #今天
          use_today_all=models.Bill.objects.filter(FastPhon_id=phone,sty='1') #实名以后才会有金额
          for i in use_today_all:
            if i.Get=='1':
               usemoney+=i.money
            if i.date==day:
                bill+=1
       money={"money":bill,'name':name,"usemoney":usemoney}
       state.append(money)
       return HttpResponse(json.dumps(state))



#取钱
#242078 思必驰实训:{1}您的余额已被提出 
def Getmoney(request):
  if request.method=='POST':
    token=request.POST.get('token')
    password=request.POST.get('pwdVal')
    user_password=Password_module('1') #检查token
    phone=user_password.checkToken(token)
    if phone!=0:
      try:
        state=models.FastFood.objects.get(phone=phone,sty='1') #查看骑手是否验证
      except:
        return HttpResponse('-2') #未注册
      user=models.FastFood.objects.filter(phone=phone,password=password).first() #密码是否正确
      if user!=None:
        money=models.Bill.objects.filter(FastPhon_id=phone,Get='1').first() #查看该用户余额
        if money!=None:
          models.Bill.objects.filter(FastPhon_id=phone,Get='1').update(Get='0') #余额全部提走
          get_user=models.FastFood.objects.filter(phone=phone).first()
          template_id=242078
          number=phone
          content=get_user.Name #骑手名字
          send_phone=ShortMessageAPI(template_id,number,content) #发送短信
          send_phone.send()
          time.sleep(1)#信息发送的慢 等待信息送达
          return HttpResponse('1')#成功
        else:
           return HttpResponse('0')#余额不足
      else:
          return HttpResponse('2')#密码错误
    else:
       return HttpResponse('-1')#登录过期




#查看该用户历史账单 返回值按时间排序
from django.db.models import Q 
from django.db.models import F
def CheckMoney(request):
  if request.method=='POST':
     token=request.POST.get('token')
     user_password=Password_module('1')
     phone=user_password.checkToken(token)
     if phone!=0:
        day=str(time.strftime("%Y-%m", time.localtime()))
        all_bill=models.Bill.objects.filter(FastPhon_id=phone).order_by(F('date'),F('apm')).select_related()
        if all_bill!=0:
          content=[]
          for i in all_bill:
            date=i.date
            addres=i.addres
            money=i.money
            c={'date':date,'apm':addres,'money':money }
            content.append(c)
          return HttpResponse(json.dumps(content))
        else:
          return HttpResponse('0')
     else:
       return HttpResponse('0') 

   

#用户实名认证
#上传身份证 用注册时候的照片与身份证照片进行对比
#243770 思必驰实训通知:{1}骑手通过实名认证
from django.conf import settings
import uuid
def IDcard (request):
   if request.method=='POST':
     token=request.POST.get('token')
     file=request.FILES.get('file')#获取照片
     PasswordClass=Password_module('0')#检查token
     phone=PasswordClass.checkToken(token) 
     Tell=models.FastFood.objects.filter(phone=phone,sty='0').first()#查看用户是否实名
     if phone!=0 and Tell!=None:
        images=[]
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
        extension=os.path.splitext(file.name)[1] #获取文件后缀名
        file_name='{}{}'.format(uuid.uuid4(),extension)#从命名
        file_path='{}{}'.format(settings.MEDIA_ROOT,file_name)#文件路径
        images.append('{}{}'.format(settings.MEDIA_URL,file_name))
        with open (file_path,'wb') as f:
            for c in file.chunks():
                    f.write(c)
        get_user=models.FastFood.objects.filter(phone=phone).first()
        img_1=get_user.imgs
        img_2=file_path
        user=PhotoID(img_1,img_2) #  用户与身份证对比
        state=user.Requ()
        if state==1: #通过实名验证 并发送短信
          template_id=243770
          number=phone
          content=get_user.Name #骑手名字
          send_phone=ShortMessageAPI(template_id,number,content) #发送短信
          send_phone.send()
          models.FastFood.objects.filter(phone=phone).update(imgs_1=file_path,sty='1')#骑手实名
          return HttpResponse('ok')
        else:
          return HttpResponse('no')
     else:
          return HttpResponse('no')



#查看用户是否被验证
def checkimg(request):
  if request.method=='POST':
    token=request.POST.get('token')
    PasswordClass=Password_module('0')
    phone=PasswordClass.checkToken(token)
    Tell=models.FastFood.objects.filter(phone=phone,sty='0').first()
    if phone!=0 and Tell!=None:
        return HttpResponse('1')
    else:
       return HttpResponse('2')
