from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.decorators import login_required
from django.views.generic import (ListView, 
                                  DetailView, 
                                  CreateView,
                                  UpdateView,
                                  DeleteView)

# Create your views here.

# Home view
@login_required
def home(request, LoginRequiredMixin):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

# View posts on home page as list
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# Detailed view of a post 
class PostDetailView(DetailView):
    model = Post

# Create view of post based on mixin
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    # Test that user delete post is original creator
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# Update view creates form, update fields provided
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    # Test that user updating post is original creator
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# About view
def about(request):
    return render(request, 'blog/about.html', {'title' : 'About'})