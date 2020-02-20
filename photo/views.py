from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from photo.forms import PostCreateForm, UserLoginForm, PostEditForm
from .models import Post

def post_list(request):
    orderby = 'created'
    status = 'published'
    statusGet = request.GET.get('status')
    query = request.GET.get('q')
    order = request.GET.get('orderby')
    if statusGet:
        status = statusGet
    if order == 'dsc':
        orderby = '-created'

    if query:
        if status == 'all':
            posts = Post.published.filter(
                Q(title__icontains=query) &
                Q(author__username=request.user)

            ).order_by(orderby)
        elif status == 'draft':
            posts = Post.published.filter(
                Q(title__icontains=query)&
                Q(author__username=request.user)&
                Q(status__exact=status)

            ).order_by(orderby)
        else:
            posts = Post.published.filter(
                (Q(title__icontains=query) |
                Q(author__username=query)) &
                Q(status__exact=status)

            ).order_by(orderby)
    else:
        if status == 'all':
            posts = Post.published.filter(
                Q(author__username=request.user)

            ).order_by(orderby)
        elif status == 'draft':
            posts = Post.published.filter(
                Q(author__username=request.user) &
                Q(status__exact=status)

            ).order_by(orderby)
        else:
            posts = Post.published.filter(Q(status__exact=status)).order_by(orderby)

    context = {
        'posts': posts,
    }
    return  render(request, 'photo/post_list.html', context)

# class PostListView(ListView):
#     model = Post
#     # queryset = Post.objects
#     template_name = 'post_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
#         return context


def post_detail(request, id, slug):
    post = get_object_or_404(Post,id=id, slug=slug)
    context = {
        'post': post,
    }
    return render(request, 'photo/post_detail.html', context)


class CreatePostView(CreateView): # new
    model = Post

    form_class = PostCreateForm
    template_name = 'photo/post_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        model = form.save(commit=False)
        print(model)
        model.author = self.request.user
        model.save()
        print(self.get_success_url())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('post_list')

# class EditPostView(CreateView): # new
#     model = Post
#
#     form_class = PostCreateForm
#     template_name = 'photo/post_edit.html'
#     success_url = reverse_lazy('post_list')
#
#     def form_valid(self, form):
#         model = form.save(commit=False)
#         model.author = self.request.user
#
#         model.save()
#         print(self.get_success_url())
#         return HttpResponseRedirect(self.get_success_url())
#
#     def get_success_url(self):
#         return reverse('post_list')

def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        raise Http404()
    if request.method == "POST":
        form = PostEditForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        # print(post)
        form = PostEditForm(instance=post)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'photo/post_edit.html', context)

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        raise Http404()
    post.delete()
    return redirect('post_list')

# def post_create(request):
#     # ImageFormset = modelformset_factory(Images, fields=('image',),extra=1)
#     if request.method == 'POST':
#         form = PostCreateForm(request.POST)
#         # formset = ImageFormset(request.POST, request.FILES)
#         print(form)
#         if form.is_valid(): # and formset.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return render(request, 'photo/post_list.html')
#             # for f in formset:
#             #     try:
#             #         photo = Images(post=post, image=f.cleaned_data['image'])
#             #         photo.save()
#             #         return redirect('post_list')
#             #     except Exception as e:
#             #         break
#     else:
#         form = PostCreateForm()
#         # formset = ImageFormset(queryset=Images.objects.none())
#     context = {
#         'form': form,
#         # 'formset': formset
#     }
#     return render(request, 'photo/post_create.html', context)
#
#     success_url = reverse_lazy('photo:post_create')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('post_list'))
                else:
                    return  HttpResponse("User is not active")
            else:
                return HttpResponse("User is None")
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }
    return render(request, 'photo/login.html', context)

def user_logout(request):
    logout(request)
    return redirect('user_login')
