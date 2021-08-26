from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
# with 'decorators' in function based view
from django.contrib.auth.decorators import login_required
# with 'mixins' in class based view
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import (TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)


# Create your views here.
##############################################################################################
#######################################  Post   ##############################################
##############################################################################################

class AboutView(TemplateView):
    """
    AboutView inherit from TemplateView for about page.
    """
    template_name = 'blog/about.html'


class PostListView(ListView):
    """
    PostListView inherit from ListView for List of Posts.
    """
    model = Post

    def get_queryset(self):
        """
        It's allows us to use django's ORM when dealing with views.
        From 'Post' model with objects. filter and grab 'published_date' lte timezone and set in order.

        '__lte'           :- less than or equal to
        '-published_date' :- means we can see newest published_date at top in ListView.

        SQL Syntax        :-                               field__lookuptype = value
        SQL Query         :- SELECT * FROM PostEntry WHERE published_date <= 'current datetime';

        :return: SQL Query
        """
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    """
    PostDetailView inherit from DetailView for Detail of Posts.
    """
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    """
    CreatePostView inherit from LoginRequiredMixin and CreateView for create a new Post.
    For Creating a New Post authentication is required.
    """

    # For Redirection
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    # import from forms.py
    form_class = PostForm

    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    PostUpdateView inherit from LoginRequiredMixin and UpdateView for update a Post.
    For Update existing Post authentication is required.
    """

    # For Redirection
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    # import from forms.py
    form_class = PostForm

    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    PostDeleteView inherit from LoginRequiredMixin and DeleteView for delete a Post.
    For Delete existing Post authentication is required.
    """

    model = Post
    # After deleting post, user redirect to homepage using success_url.
    # if we didn't put 'reverse_lazy' than it will redirect again and again.
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    """
    DraftListView inherit from LoginRequiredMixin and ListView for Draft a post.
    After creating a post it will store in Draft.
    """

    # for redirection
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'

    model = Post

    def get_queryset(self):
        """
        It's allows us to use django's ORM when dealing with views.
        From 'Post' model with objects. filter and grab list with no 'published_date'.
        SQL Syntax        :-                               field__lookuptype = value
        SQL Query         :- SELECT * FROM PostEntry WHERE published_date = null;

        :return: SQL Query
        """
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


##############################################################################################
#####################################  Comment   #############################################
##############################################################################################


@login_required
def post_publish(request, pk):
    """
    For publish post.
    :param request:   post request.
    :param pk:   primary key of post.
    :return:   page name, pk of post.
    """
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):
    """
    For add comment on particular post.
    :param request:   particular post request for comment.
    :param pk:   particular post's primary key.
    :return:   particular post page, form for comment on page, dictionary for manage.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    """
    For approve comment on post.
    :param request:   request for post detail.
    :param pk:   primary key of comment model's of particular post.
    :return:   page name of post details, pk of particular post.
    """
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    """
    For remove comment.
    :param request:  request for post detail.
    :param pk:   primary key of comment model's of particular post.
    :return:   page name of post details, pk of particular post.
    """
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
