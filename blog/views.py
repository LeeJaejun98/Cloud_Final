from django.shortcuts import render, redirect
from .models import Post, Category, Tag
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import CommentForm
import calendar
from datetime import datetime


class MyHtmlCalendar(calendar.HTMLCalendar):
    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            # day outside month
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            return '<td class="%s"><a href="/blog/%s/">%d</a></td>' % (self.cssclasses[weekday], day, day)


def calendar_view(request):
    year = datetime.now().year
    month = datetime.now().month
    next_month = month + 1
    next_year = year
    previous_month = month - 1
    previous_year = year
    if month == 12:
        next_month = 1
        next_year = year + 1
    elif month == 1:
        previous_month = 12
        previous_year = year - 1

    calendar_html = calc_calendar(year, month)
    return render(request, 'blog/calendar.html', {
        'calendar_html': calendar_html,
        'previous_month': previous_month,
        'previous_year': previous_year,
        'next_month': next_month,
        'next_year': next_year,
        'year': year,
        'month': month,
    })


def calendar_view_other(request, year, month):
    next_month = month + 1
    next_year = year
    previous_month = month - 1
    previous_year = year
    if month == 12:
        next_month = 1
        next_year = year + 1
    elif month == 1:
        previous_month = 12
        previous_year = year - 1

    calendar_html = calc_calendar(year, month)
    return render(request, 'blog/calendar.html', {
        'calendar_html': calendar_html,
        'previous_month': previous_month,
        'previous_year': previous_year,
        'next_month': next_month,
        'next_year': next_year,
        'year': year,
        'month': month,
    })


def calc_calendar(year, month):
    cal = MyHtmlCalendar(calendar.SUNDAY)
    return cal.formatmonth(year, month)


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'file_upload', 'category', 'tag']

    template_name = 'blog/post_update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and self.get_object().author == request.user:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionError


class PostCreate(LoginRequiredMixin, CreateView):  # 사용자에게 정보를 받아오는 페이지 + 페이지에 들어있는 홈의 정보 가져오기
    model = Post
    fields = ['title', 'content', 'head_image', 'file_upload', 'category', 'tag']  # 7개만 받기

    # def test_func(self):
    #     return self.request.user.is_superuser or self.user.request.is_staff

    def get_context_data(self, **kwargs):
        context = super(PostCreate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_count'] = Post.objects.filter(category=None).count()

        return context

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')


class PostList(ListView):
    model = Post
    ordering = '-pk'  # 내림차순으로 정렬해주기 위해

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_count'] = Post.objects.filter(category=None).count()

        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context


def categories_page(request, slug):
    if slug == 'no-category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    context = {
        'category': category,
        'categories': Category.objects.all(),
        'post_list': post_list,
        'no_category_count': Post.objects.filter(category=None).count()

    }
    return render(request, 'blog/post_list.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    context = {
        'tag': tag,
        'category': Category.objects.all(),
        'post_list': post_list,
        'no_category_count': Post.objects.filter(category=None).count()

    }
    return render(request, 'blog/post_list.html', context)  # function based view


def add_comment(request, pk):
    if not request.user.is_authenticated:
        raise PermissionError

    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        comment_form = CommentForm(request.POST)
        comment_temp = comment_form.save(commit=False) #바로 DB로 가는것을 막기 위해 commit 사용
        comment_temp.post = post
        comment_temp.author = request.user
        comment_temp.save()

        return redirect(post.get_absolute_url())
    else:
        raise PermissionError
