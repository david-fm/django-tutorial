from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'

    # Change of the default DetailView generic view, which uses a template called: 
    # <app name>/<model name>_list.html
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Act as the context_object.
        # Return the last five published questions.
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    # Search for a question by its pk, indicated in urls.py.
    model = Question

    # The question variable will be passed automatically to the template, because the name of the model is Question.
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    # Search for a question by its pk, indicated in urls.py.
    model = Question

    # Change of the default DetailView generic view, which uses a template called: 
    # <app name>/<model name>_detail.html
    template_name = 'polls/results.html'

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