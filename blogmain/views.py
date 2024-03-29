from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
# Create your views here.

# def home(request):
#     context = {
#         'posts':Post.objects.all()
#     }
#     return render(request,'blogmain/home.html',context)
def about(request):
    return render(request,'blogmain/about.html',{'title':'About Page'})

class PostListView(ListView):
    model=Post
    context_object_name='posts'
    template_name='blogmain/home.html'
    ordering = ['-date_posted']
    paginate_by=5

class UserPostListView(ListView):
    model=Post
    context_object_name='posts'
    template_name='blogmain/user_posts.html'
    paginate_by =5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields= ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields= ['title','content']
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url = '/'
    fields= ['title','content']
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



 

