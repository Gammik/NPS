from django.db import models
from django.contrib.auth.models import User
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_delete
from django.dispatch import receiver
import datetime

class News(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=70)
	description = models.TextField(null=True, blank=True)
	images = models.ImageField(upload_to='newsimages/', default=None, null=True, blank=True)
	face_image = models.ImageField(upload_to='newsface/')
	created = models.DateTimeField(auto_now_add=True)
	text = models.TextField()
	id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False)
	class Meta:
		ordering = ["-created"]
class profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,)
	profile_image = models.ImageField(upload_to='profileimages/', default=None, null=True, blank=True)
	bio = models.CharField(null=True, blank=True, max_length=130)
	Date_of_birth = models.DateField(null=True, blank=True)
	phone_number = PhoneNumberField(null=True, blank=True, region="UZ")
	job = models.CharField(null=True, blank= True, max_length=50)
	id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False)
	about = models.TextField(null=True, blank=True)
	telegram = models.CharField(null=True, blank=True, max_length=100)
	instagram = models.CharField(null=True, blank=True, max_length=100)
	def __str__(self):
		return f"{self.user}"
# Create your models here.
class Skills(models.Model):
	skills = models.CharField(max_length=30)
	host = models.ForeignKey(User, on_delete=models.CASCADE)
class project(models.Model):
	host = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateField(default=datetime.date.today)
	category = models.CharField(null=True, blank=True, max_length=20)
	cost = models.CharField(null=True, blank=True, default="0.0$", max_length=10)
	profit = models.CharField(null=True, blank=True, default="Non-profit", max_length = 11)
	time = models.CharField(null=True, blank=True, max_length=10)
	Website = models.CharField(null=True, blank=True, default=None, max_length=150)
	name = models.CharField(max_length=30)
	description = models.TextField()
	mission = models.CharField(max_length=150)
	vision = models.CharField(max_length=150)
	result = models.CharField(max_length=150)
	face = models.ImageField(upload_to="projectimages/")
	id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False)
	def __str__(self):
		return f"{self.id}"
class projectfile(models.Model):
	file = models.FileField(upload_to="projectfiles/")
	project_id = models.ForeignKey(project, on_delete=models.CASCADE)
class projectimage(models.Model):
	image = models.ImageField(upload_to="projectimages/")
	project_id = models.ForeignKey(project, on_delete=models.CASCADE)
class projectmember(models.Model):
	member = models.ForeignKey(profile, on_delete=models.CASCADE)
	job = models.CharField(max_length=20)
	project_id = models.ForeignKey(project, on_delete=models.CASCADE)





@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field,models.FileField):
            instance_file_field = getattr(instance,field.name)
            delete_file_if_unused(sender,instance,field,instance_file_field)
            
""" Delete the file if something else get uploaded in its place"""

""" Only delete the file if no other instances of that model are using it"""    
def delete_file_if_unused(model,instance,field,instance_file_field):
    dynamic_field = {}
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)