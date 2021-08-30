import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
	# Each variable represents a database field
	question_text = models.CharField(max_length=200) # CharField is a character field
	# max_length is an obligatory argument in CharFields
	pub_date = models.DateTimeField('date published')# DateTimefield is a datetime field
	# The first argument is not obligatory, but it is the fields name, if it isn't write it will be the name of the variable

	def __str__(self):
		return self.question_text
		
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now
        
class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete= models.CASCADE)
	# This creates a relationship between Choice and Question
	# Resurce to understand the relationship -> https://www.ibm.com/docs/en/mam/7.6.0?topic=structure-database-relationships
	# Resurce to undestand Django Model Relationships -> https://www.youtube.com/watch?v=2KqhBkMv7aM
	# In this case is one to many, one Question can have multiple Choice.
	# question field will indicate the ID of the Question on its own table.
	# what on_delete argument does is that if the Question related with the Choice is eliminate the choice will also be eliminated 
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	
	def __str__(self):
		return self.choice_text
	
	#It’s important to add __str__() methods to your models, not only for your own convenience when dealing with the interactive prompt, but also because objects’ representations are used throughout Django’s automatically-generated admin.
	
