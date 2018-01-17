#coding:utf-8

from django.db import models
class Article(models.Model):
    title = models.CharField(u'标题',max_length=256)
    content = models.TextField(u"内容")
    pub_date = models.DateTimeField(u'发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True, null=True)
    
    def __unicode__(self):
        return self.title
        
class Author(models.Model):
    username = models.CharField(u'用户名', max_length=32, unique=True)
    join_time = models.DateTimeField(u"加入时间", auto_now_add=True, editable=True)
    def __unicode__(self):
        return self.username