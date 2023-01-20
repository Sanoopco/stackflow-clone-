from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.db.models import Count
# Create your models here.


class MyUser(AbstractUser):
    phone=models.CharField(max_length=20)
    profile_pic=models.ImageField(upload_to="profilepics",null=True)



class Questions(models.Model):
    question=models.CharField(max_length=500)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    images=models.ImageField(upload_to="qs_images",null=True,blank=True)
    qs_created_date=models.DateTimeField(auto_now_add=True)
    @property
    def fetch_answers(self):
        answers=self.answers_set.all().annotate(up_count=Count('up_vote')).order_by('-up_count')
        return answers

    def __str__(self):
        return self.question

class Answers(models.Model):
    answer=models.CharField(max_length=500)
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    up_vote=models.ManyToManyField(MyUser,related_name="upvote")
    ans_created_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.answer
        
