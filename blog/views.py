from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from re import findall,match,sub,compile

# Create your views here.

Chords = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'Cm', 'Dm', 'Em', 'Fm', 'Gm', 'Am', 'Bm', 'C#', 'D#', 'E#', 'F#', 'G#',
          'A#', 'B#', 'C#m', 'D#m', 'E#m', 'F#m', 'G#m', 'A#m', 'B#m']


def post_list(request):
    query = request.GET.get("query")
    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    paginator = Paginator(posts, 10)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {"posts": posts}

    return render(request, 'blog/post_list.html', context)


def calendar(request):
    return render(request, 'blog/Calendar.html')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    text = post.text

    pattern = compile(r'([A-H]#?m?7?s?u?s?2? |[A-H]#?m?7?s?u?s?2?\r\n)')
    # text = text.replace('\n', "")
    text = sub(pattern, lambda x: '<strong>' + x.group(1) + '</strong>', text)


    context = {"title": post.title,
               "post": post,
               "text": text
               }
    return render(request, 'blog/post_detail.html', context)


def post_new(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == "POST":

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
