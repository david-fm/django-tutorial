from django.urls import path
from . import views

app_name = 'polls' # identifier for urls on index

urlpatterns = [
	# Change to use generic views
	# path('',views.index, name = 'index'),
	# attach the view called index to the base URL '' and give it the name index
	path('',views.IndexView.as_view(), name = 'index'),

	# Change to use generic views
	# path('<int:question_id>/', views.detail, name='detail'),
	path('<int:pk>', views.DetailView.as_view(), name='detail'),

	# <int part is a converter that determines what patterns should mathc this part of the URL path
	# :question_id> part of the string defines the name that will be used to indentify the matched pattern 
	
	# Change to use generic views
	# path('<int:question_id>/results/', views.results, name='results'),
	path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
	path('<int:question_id>/vote/', views.vote, name='vote'),
]
