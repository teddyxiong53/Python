# -*- coding:utf-8 -*-

from django.http import HttpResponse
from TestModel.models import Test

def testdb(request):
    test1 = Test(name='Allen')
    test1.save()
    return HttpResponse("<h1>数据库添加内容成功</h1>")
    
def getdb(request):
    response = Test.objects.get(id=1)
    name = response.name
    return HttpResponse("<h1>" + str(name) + "</h1>")
    
def updatedb(request):
    test1 = Test.objects.get(id=1)
    test1.name = "Bob"
    test1.save()
    return HttpResponse("<p>修改成功</p>")
    
def deldb(request):
    test1 = Test.objects.get(id=1)
    test1.delete()
    return HttpResponse("删除成功")
    