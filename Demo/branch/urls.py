from django.conf.urls import url
from . import views1
urlpatterns=[
    url(r'^register/',views1.register),  #注册
    url(r'^duanxin/',views1.Information), #注册发送验证码
    url(r'^checktoken/',views1.CheckToken), #token快速登录
    url(r'^login/',views1.login),#用户账号密码登录
    url(r'^business/',views1.business),#未接的账单查询
    url(r'^grabsingle/',views1.GrabSingle),#骑手抢单
    url(r'^tianqi/',views1.weather),#天气情况/骑手的姓名/骑手余额/骑手今天订单数目/ 
    url(r'^checkphon/',views1.CheckPhon),#用户注册时检查手机号是否被注册
    url(r'^getmoney/',views1.Getmoney),#取钱
    url(r'^checkmoney/',views1.CheckMoney),#查看历史账单
    url(r'^shopping/',views1.Shopping),#查看商家详情
    url(r'^idcard/',views1.IDcard),#进行实名
    url(r'^checkimg/',views1.checkimg)#检查是否实名
]