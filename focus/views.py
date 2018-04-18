from django.shortcuts import render,redirect,get_object_or_404
from .models import Article,Comment,Poll,NewUser
from .forms import LoginForm,CommentForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import markdown2

# Create your views here.
def index(request):
    latest_article_list = Article.objects.query_by_time()
    login_form = LoginForm()
    context = {'latest_article_list':latest_article_list,'login_form':login_form}
    return render(request,'focus/index.html',context)

def log_in(request):
    if request.method == 'GET' :
        login_form = LoginForm()
        context = {'login_form':login_form}
        return render(request,'focus/login1.html',context)
    if request.method == 'POST' :
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['uid']
            password = form.cleaned_data['pwd']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                url = request.POST.get('source_url','/focus')
                return redirect(url)
            else:
                return render(request,'focus/login2.html', {'form':form, 'error': "password or username is not ture!"})
        else:
            return render(request,'focus/login3.html',{'login_form':login_form})


@login_required
def log_out(request):
    url = request.POST.get('source_url','/focus')
    logout(request)
    return redirect(url)


def article(request,article_id):
    article = get_object_or_404(Article,id=article_id)
    login_form = LoginForm()
    comment_form = CommentForm()
    content = markdown2.markdown(article.content,extras=["code-friendly", 
		"fenced-code-blocks", "header-ids", "toc", "metadata"])
    #comments = article.comment_set.all 
    comments = Comment.objects.filter(article_id=article_id)
    context = {'article':article,'login_form':login_form,'content':content,'comment_form':comment_form,'comments':comments}
    return render(request,'focus/article_page.html',context)    

@login_required
def comment(request,article_id):
    article = get_object_or_404(Article,id=article_id)
    if request.method == 'POST' :
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            new_comment = form.cleaned_data['comment']
            c = Comment(content=new_comment,article_id=article.id)
            c.user = user
            c.save()
            article.comment_num += 1
            article.save()
    return redirect("/focus/"+str(article_id))

@login_required
def favorate(request,article_id):
    user = request.user
    article = get_object_or_404(Article,id=article_id)
    if request.method == 'GET' :
        #article.user.add(user)
        article.keep_num += 1
        article.save()
    return redirect("/focus/"+str(article_id))

@login_required
def poll(request,article_id):
    article = get_object_or_404(Article,id=article_id)
    user = request.user
    polled_users =  Poll.objects.filter(article_id=article_id)
    if user in polled_users:
        return redirect("/focus/"+str(article_id))
    else:
        #p = Poll(user=)
        article.poll_num += 1
        article.save()
        return redirect("/focus/"+str(article_id))

