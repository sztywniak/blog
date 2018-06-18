from django.contrib.sessions import serializers
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from blog.forms import CommentForm, PostForm, PostPassword
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def post_list_view(request):
    context_object_name = 'my_posts'
    list_objects = Post.published.all()
    querry = request.GET.get("q")
    if querry:
        list_objects = list_objects.filter(title__icontains=querry)
    querry2 = request.GET.get("q2")
    if querry2:
        list_objects = list_objects.filter(author__username__icontains=querry2)
    querry3 = request.GET.get("q3")
    if querry3 == "1":
        list_objects = list_objects.filter(category__icontains='Ogolne')
    elif querry3 == "2":
        list_objects = list_objects.filter(category__icontains='Zwierzeta')
    elif querry3 == "3":
        list_objects = list_objects.filter(category__icontains='Motoryzacja')
    elif querry3 == "4":
        list_objects = list_objects.filter(category__icontains='Kulinarne')
    elif querry3 == "5":
        list_objects = list_objects.filter(category__icontains='Zdrowie i uroda')
    elif querry3 == "6":
        list_objects = list_objects.filter(category__icontains='Dom/Mieszkanie')
    elif querry3 == "7":
        list_objects = list_objects.filter(category__icontains='Ogrod')
    elif querry3 == "8":
        list_objects = list_objects.filter(category__icontains='Majsterkowanie')
    elif querry3 == "9":
        list_objects = list_objects.filter(category__icontains='Muzyka')
    elif querry3 == "10":
        list_objects = list_objects.filter(category__icontains='Sztuka')
    elif querry3 == "11":
        list_objects = list_objects.filter(category__icontains='Sport')

    paginator = Paginator(list_objects, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts})


@login_required
def post_detail_view(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, publish__year=year, publish__month=month,
                             publish__day=day)
    if post.status == "":
        return render(request, 'blog/post/detail.html', {'post': post})
    else:
        form = PostPassword(request.POST)
        if form.is_valid():
            data = request.POST.get('status')
            if data == post.status:
                return render(request, 'blog/post/detail.html', {'post': post})
        return render(request, 'blog/post/post_access.html', {'post': post, 'form': form})


@login_required
def new_post(request):
    template = 'blog/new_post.html'
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        stock = form.save(commit=False)
        stock.author = request.user
        stock.save()
        return redirect('/blog')
        # messages.success(request,'Add')
    else:
        form = PostForm()

    context = {'form': form, }
    return render(request, template, context)


@login_required
def edit_post(request, pk):
    template = 'blog/new_post.html'
    post = get_object_or_404(Post, pk=pk)
    if (request.method == "POST"):
        form = PostForm(request.POST, request.FILES or None, instance=post)
        try:
            if form.is_valid():
                form.save()
                return redirect('/blog')
        except Exception as e:
            messages.warning(request, "Post was not save".format(e))
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, template, context)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    for comment in post.comments.all():
        comment.delete()
    post.delete()
    return redirect('/blog')


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return render(request, 'blog/post/detail.html', {'post': comment.post})
    else:
        form = CommentForm()
        return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return render(request, 'blog/post/detail.html', {'post': comment.post})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
