from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import MyLoginForm, UserRegisterForm, PostAddForm, PostEditForm
from .models import Post, Comment


# Create your views here.
# def index(request):
#     return HttpResponse("<h1>This is just a test view</h1>")

# def index(request):
#     return render(request, 'posts.html')
def post_list(request):
    print("im here")
    searchTerm = request.GET.get('searchpost')
    if searchTerm:
        post_list = (Post.objects.filter
                     (post_title__icontains=searchTerm))
    else:
    #to get all the objects
        post_list = Post.objects.all()
        print(type(post_list))
    #pagination
    #into the constructor pass the list as well as no of items/page
    paginator = Paginator(post_list,2)
    #get the GET vatiable page
    page = request.GET.get('page')
    #try Except to handle exception
    try:
        posts = paginator.page(page)
    # is raised when page is having a value that is not integer
    except PageNotAnInteger:
        posts = paginator.page(1)
    # is raised when page is having a valid value but no objects
    #exist in that page
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    #we need to pass the object to HTML page
    return render(request, 'posts.html',
    {'searchTerm':searchTerm,'post_list':posts
     , 'page':page})

#to see the post details
def post_details(request, passed_id):
    #fetching all the post
    post_details = get_object_or_404(Post, id=passed_id)
    #fetching all the comments
    comments = Comment.objects.filter(post=post_details)
    print(comments)
    return render(request,
                  'postdetails.html',
                  {'post_details':post_details,
                     'comments':comments})


#login
def user_login(request):
    if request.method == 'POST':
        #we will be getting username and paswword through Post
        login_form = MyLoginForm(request.POST)
        if login_form.is_valid():
            cleaned_data = login_form.cleaned_data
            auth_user = authenticate(request,
                            username=cleaned_data['username'],
                            password=cleaned_data['password'])
            if auth_user is not None:
                login(request, auth_user)
                return redirect('post_list')
    else:
        login_form = MyLoginForm()
    return render(request,
                  'useraccount/login_form.html',
                  {'login_form':login_form})


def register(request):
    if request.method == 'POST':
        user_reg_form = UserRegisterForm(request.POST)
        if user_reg_form.is_valid():
            new_user = user_reg_form.save(commit=False)
            new_user.set_password(user_reg_form.cleaned_data['password'])
            new_user.save()
            return render(request,
                          'registration/register_done.html',
                          {'user_reg_form':user_reg_form})
    else:
        user_reg_form = UserRegisterForm()
    return render(request,
                  'registration/register.html',
                  {'user_reg_form': user_reg_form})


#method to add post
@login_required(login_url='login')
def add_post(request):
    add_post_form = PostAddForm(request.POST, request.FILES)
    if request.method == 'POST':
        if add_post_form.is_valid():
            #create the form. do not save it yet
            new_post = add_post_form.save(commit=False)
            #assigning post_author as currently logged user
            new_post.post_author = request.user
            new_post.save()
            return redirect('post_list')
    else:
        add_post_form = PostAddForm()
    return render(request, 'useraccount/add_post.html',
                  {'add_post_form':add_post_form})

#update post

@login_required(login_url='login')
def edit_post(request, passed_id):
    post_details = get_object_or_404(Post, id=passed_id)
    edit_post_form = (PostEditForm
                      (request.POST or None,request.FILES or None,
                       instance=post_details))
    if edit_post_form.is_valid():
        edit_post_form.save()
        return redirect('post_list')
    return render(request,
                  'useraccount/edit_post.html',
                  {'edit_post_form':edit_post_form})
#delete
def delete_post(request, passed_id):
    post_details = get_object_or_404(Post, id=passed_id)
    post_details.delete()
    return redirect('post_list')
