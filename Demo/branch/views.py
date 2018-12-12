from django.shortcuts import render,HttpResponse
#数据库
from branch import models
from branch.models import FastFood,Shop,Bill,Authentication
#短信
from qcloudsms_py import SmsSingleSender 
from qcloudsms_py.httpclient import HTTPError
import random
import hashlib
from django.core import signing


#该类对密码 token 加/解密 创建数据保存在数据库中
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
    def checkToken(self,token):
        try:
            phone=self.get_token(token)
            print(phone)
            return phone["number"] 
        except:
            return 0



import urllib.request
class Tian:
  key = '0e6229b55b7f48c8a7b1a7a17585c2ab'
  location = '张家港'
  location_name = {'张家港': 'zhangjiagang', '上海': 'shanghai'}
  location_hname = location_name.get(location)
  def __init__(self):
      pass
  def nowtq(self,datanowtq):
    C='%s'%(datanowtq['tmp'])
    rain=datanowtq['pcpn']
    wind=datanowtq['wind_sc']
    if rain=='0.0':
      rain='0'
    
    content=[{
    "C":C,
    "rain":rain,
    "wind":wind
    }]
    return content



  def get_1_json(self):
    url = 'https://free-api.heweather.com/s6/weather/now?location=' + self.location_hname + '&key=' + self.key
    html = urllib.request.urlopen(url).read() 
    hjson = json.loads(html)
    nowtq_status = hjson['HeWeather6'][0]['now']
    return self.nowtq(nowtq_status)


#注册
def duanxin(request):
 if request.method=='POST':
  phone=request.POST.get('coachid')
  State=models.Authentication.objects.filter(phone=phone).first()
  if State!=None:
      if State.sty=='1' :
         return HttpResponse('已注册')
  else:
        number=''
        for i in range(6): 
           ch=chr(random.randrange(ord('0'),ord('9')+1))
           number+=ch
        models.Authentication.objects.filter(phone=phone).update(phone=phone,number=number,sty='0')
        return HttpResponse(number)
  
     # appid=1400112426
     # appkey="e8100999c3d47a649e25ce678202825e"
     # phone_numbers=[phone]
     # template_id=242074
     # sms_sign="两人随纪"
     # ssender = SmsSingleSender(appid, appkey)
     # params=[]
     # params.append(number)
     # result = ssender.send_with_param(86, phone_numbers[0],
     # template_id, params, sign=sms_sign, extend="", ext="")
     #  


#无异常
def checktoken(request):
    if request.method=='POST':
       token=request.POST.get('token')
       print(token)
       check=Password_module('1')
       State=check.checkToken(token)
       if State==0: #失败
         return HttpResponse('0')
       else:
        return HttpResponse('1')


#无异常
def checkphon(request):
    if request.method=='POST':
       phone=request.POST.get('phone')
       State=models.Authentication.objects.filter(phone=phone).first()
       if State!=None and State.sty!='0':
           return HttpResponse(1)
       else:
          return HttpResponse(0)



import os
import base64
from PIL import Image
from io import StringIO
def register(request):
    if request.method=='POST':
        possword=request.POST.get('coachpassword') #密码
        yanzhengma=request.POST.get('VerificationCode')  #验证码
        phone=request.POST.get('coachid') #手机号
        Name=request.POST.get('Name')
        file=request.FILES.get('file') 
        State=models.Authentication.objects.filter(phone=phone).first()
        if State!=None and yanzhengma==State.number:
           images=[]
           if len(file)>0: #判断是否为空
              if not os.path.exists(settings.MEDIA_ROOT):
                 os.makedirs(settings.MEDIA_ROOT)
              extension=os.path.splitext(file.name)[1] #获取文件后缀名
              file_name='{}{}'.format(uuid.uuid4(),extension)#从命名
              file_path='{}{}'.format(settings.MEDIA_ROOT,file_name)#文件路径
              images.append('{}{}'.format(settings.MEDIA_URL,file_name))
              with open (file_path,'wb') as f:
                 for c in file.chunks():
                    f.write(c)
              models.Authentication.objects.filter(phone=phone).update(sty='1')
              t=Password_module(phone)
              token=t.create_db()
              models.FastFood.objects.create(phone=phone,password=possword,Name=Name,StudentToken=token)
              models.FastFood.objects.get(phone=phone,password=possword,Name=Name,StudentToken=token).update(imgs=images)
              return HttpResponse(token)
        else:
           return HttpResponse('0')
               

#无异常
def login(request):
  if request.method=='POST':
      phone=request.POST.get('username')
      password=request.POST.get('password')
      try:
          State=models.FastFood.objects.get(phone=phone,password=password)
          if State.phone:
               return HttpResponse(State.StudentToken) 
          else:
              return HttpResponse("no")
      except:
           return HttpResponse("no")
      


#无异常
import datetime
import json
from datetime import datetime
import time
def business(request):
  if request.method=='GET':
     day=str(time.strftime("%Y-%m-%d", time.localtime()))
     Time=str(time.strftime("%H:%M",time.localtime()))
     if Time>'12:00':
         apm='下午'
     elif Time<'12:00':
          apm='上午'
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

#无异常
def GrabSingle(request):
  if request.method=='POST':
    goods_token=request.POST.get('token')
    good_id=request.POST.get('id')
    PasswordClass=Password_module('0')

    phone=PasswordClass.checkToken(goods_token)
    if phone!=0:
       user=models.FastFood.objects.filter(phone=phone).first()
       if user.sty=='0':
          return HttpResponse("0") #没有实名验证
       else:
           bill=models.Bill.objects.filter(billId=good_id,sty='0').first()
           print(bill,'账单')
           if bill!=None:
              models.Bill.objects.filter(billId=good_id).update(sty='1',FastPhon_id=user.phone)
              return HttpResponse('Success') #成功
           else:
              return HttpResponse('1')#账单被抢
    else:
      return HttpResponse('-1') #伪造的token 
                  


    



#无异常
def tianqi(request):
    if request.method=='POST':
       allmoney=0
       name='暂无登录'
       usemoney=0
       use_token=request.POST.get('token')
       T=Tian()
       a=T.get_1_json()
       checktoken=Password_module('1')
       phone=checktoken.checkToken(use_token)
       if phone!=0:
          user=models.FastFood.objects.filter(phone=phone)
          name=user[0].Name
          day=str(time.strftime("%Y-%m-%d", time.localtime()))
          use_today_all=models.Bill.objects.filter(FastPhon_id=phone,date=day,sty='1')
          for i in use_today_all:
            if i.Get=='1':
               usemoney+=i.money
            allmoney+=1
       money={"money":allmoney,'name':name,"usemoney":usemoney}
       a.append(money)
       return HttpResponse(json.dumps(a))



def Getmoney(request):
  if request.method=='POST':
    token=request.POST.get('token')
    pwdVal=request.POST.get('pwdVal')
    user_password=Password_module('1')
    phone=user_password.checkToken(token)
    print(pwdVal,phone)
    try:
       C=models.FastFood.objects.get(phone=phone,password=pwdVal)
    except:
      return HttpResponse('-1')
    if phone!=0:
        if C:
          models.Bill.objects.filter(FastPhon_id=phone,Get='1').update(Get='0')
          return HttpResponse('1')
        else:
           return HttpResponse('0')
    else:
       return HttpResponse('-1')


from django.db.models import Q #用来进行or ->Q
from django.db.models import F
def CheckMoney(request):
  if request.method=='POST':
     token=request.POST.get('token')
     user_password=Password_module('1')
     phone=user_password.checkToken(token)
     if phone!=0:
        day=str(time.strftime("%Y-%m", time.localtime()))
        all_bill=models.Bill.objects.filter(FastPhon_id=phone,date__contains=day).order_by(F('date'),F('apm')).select_related()
  
        if len(all_bill)!=0:
          content=[]
          for i in all_bill:
            date=i.date
            apm=i.apm
            money=i.money
            c={'date':date,'apm':apm,'money':money }
            content.append(c)
          return HttpResponse(json.dumps(content))
        else:
          return HttpResponse('0')
     else:
       return HttpResponse('0') 


def Shopping(request):
   if request.method=='POST':
      shooping_id=request.POST.get('id')
      content=[]
      try:
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








import  json
import requests
import base64
class PhotoID:
  request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
  access_token='24.78008b997a495d0448dc093ef27f812b.2592000.1546491467.282335-10890686'
  def __ini__(self,img_1,img_2):
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
        request_url = request_url + "?access_token=" + access_token
        headers={'Content-Type': 'application/json'}
        response=requests.post(request_url,data=params,headers=headers)
        content = response.text
        content=json.loads(content)
        if content:
          try:
            if content['result']['score']>89:
              return 1
            else:
             return 2
          except:
             return 3










def IDcard (request):
   if request.method=='POST':
     token=request.POST.get('token')
     file=request.FILES.get('file')
     PasswordClass=Password_module('0')
     phone=PasswordClass.checkToken(token)
     Tell=models.FastFood.objects.filter(phone=phone,sty='0').first()
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
        models.FastFood.objects.get(phone=phone,password=possword,Name=Name,StudentToken=token).update(imgs_1=images)

        img_2=images
        img_1=models.FastFood.objects.get(phone=phone,password=possword,Name=Name,StudentToken=token).select_related().imgs
        stay=PhotoID(img_1,img_2)
        susses=stay.Requ()
        if susses==1:
           models.FastFood.objects.get(phone=phone,password=possword,Name=Name,StudentToken=token).update(sty='1')
           return HttpResponse('ok')
        else:
          return HttpResponse('no')
     else:
        return  HttpResponse('no')
 

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
