from django.db import models

# Create your models here.
#Category Model
class Categories(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)

    class Meta:
        db_table="categories" 

#startup model
class Startups(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    firm_name=models.CharField(max_length=100)
    email=models.EmailField()
    start_date=models.DateTimeField()
    contact_no=models.IntegerField()
    brief_desc=models.TextField()
    description=models.TextField()
    valuation=models.IntegerField()
    expected_fund=models.IntegerField()
    category_id=models.ForeignKey(Categories, on_delete=models.CASCADE)

    

#User Model
class Users(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    password_hash=models.IntegerField()
    contact_no=models.IntegerField()
    role=models.CharField(max_length=100)
    icon=models.ImageField()

    

#Inestment Model
class Investments(models.Model):
    id=models.AutoField(primary_key=True)
    startup_id=models.ForeignKey(Startups, on_delete=models.CASCADE)
    user_id=models.ForeignKey(Users, on_delete=models.CASCADE)
    investor=models.CharField(max_length=100)
    stake=models.IntegerField()
    amount=models.IntegerField()

    

#Founder Model
class Founders(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    user_id=models.ForeignKey(Users, on_delete=models.CASCADE)

  

#Upload Model
class Uploads(models.Model):
    id=models.AutoField(primary_key=True)
    startup_id=models.ForeignKey(Startups, on_delete=models.CASCADE)
    type=models.CharField(max_length=100)
    file=models.FileField()

    
