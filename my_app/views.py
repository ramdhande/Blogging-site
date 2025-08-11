from openai import OpenAI 
import os
from dotenv import load_dotenv

load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")

#print("LOADED API KEY:",openai.api_key )  # For debugging


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
"""
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import Post
from django.views.generic import  (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)    

"""
this was dummy data creted by me to create a Post
posts =[
{
	'author':'ram',
	'title':'post 1',
	'content': 'stupid',
	'date_posted': 'august 08,2024'
},
{
    'author':'rohit',
	'title':'post 2',
	'content': 'excellent',
	'date_posted': 'august 01,2024'
}
]
"""

def home(request):
	context ={
	 'posts' : Post.objects.all()
	}
	return render(request,'my_app/home.html',context)

class PostListView(ListView):
	model = Post
	template_name = 'my_app/home.html' # <app>/<model>_<viewtype>.html'
	context_object_name = 'posts'
	ordering =['-date_posted']
	paginate_by = 5

class UserPostListView(ListView):
	model = Post
	template_name = 'my_app/user_posts.html' # <app>/<model>_<viewtype>.html'
	context_object_name = 'posts'
	paginate_by = 5	

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'image', 'content']	


	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'image', 'content']	


	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)	

	def test_func(self):
		post =self.get_object()
		if self.request.user == post.author:
			return True
		return False	

class PostDeleteView( LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'	

	def test_func(self):
		post =self.get_object()
		if self.request.user == post.author:
			return True
		return False









def about(request):
	return render(request,'my_app/about.html',{'title':'About'})

# do the fucking API call 

def generate_meme_caption(request):
	if request.method == "POST":
		user_input = request.POST.get("topic", "")

		response = client.chat.completions.create(model ="gpt-3.5-turbo",
					messages=[{"role": "user", "content": f"Generate a funny meme caption about {user_input}"}])


		caption = response.choices[0].message.content

		return JsonResponse({"caption":"meme caption generate!!"})

	return render(request, "my_app/generate_meme.html")	


