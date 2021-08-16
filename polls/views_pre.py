from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import F
from .models import Question, Choice

def index(request):
	# THERE ARE THREE WAY TO DO THIS:
	# 1. Harder and not perfect.
	'''
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	# This part reads the list of objects in questions and take the first five in order of pub_date
	output = ','.join([q.question_text for q in latest_question_list])
	# This part takes the question_text from the objects and joins them with a comma between them
	return HttpResponse(output)'''
	# 2. Longer and perfect.
	'''
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	# This part reads the list of objects in questions and take the first five in order of pub_date
	template = loader.get_template('polls/index.html')
	# return a template object form the template file
	context = {
		'latest_question_list': latest_question_list,
	}
	# This part index latest_question_list with the index 'latest_question_list'
	return HttpResponse(template.render(context, request))
	'''
	# 3. Easier and perfect.
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {'latest_question_list': latest_question_list}
	return render(request, 'polls/index.html', context)
	# render takes the request object, the template file, and a dictionary.
	# Returns a HttpResponse object with the given template rendered with the given context.
	
def detail(request, question_id):
	# Try to get the question from the database and if it doesn't exist raise a 404 error.
	
	# This version is shorter and does the same
	question = get_object_or_404(Question,pk=question_id)
	return render(request, 'polls/detail.html', {'question':question})
	# if instead of finding one item you are searching for a list of them use get_list_or_404()
'''	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	return render(request, 'polls/detail.html', {'question': question})
'''
def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
		# request.POST is a dictionary-like object that lets you access submitted 
		# data by key name, in this case, 'choice', obteining it's ID.
	except(KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form if choice is not selected.
		return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice."})
	else:
		selected_choice.votes = F('votes') + 1 # we are using the F() function to update the vote count directly to the database avoiding race conditions
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))	
		# reverse() is a way to generate URLs by specifying the view name