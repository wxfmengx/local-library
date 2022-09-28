# Django Local Library

## 概述

- 文档分为三个部分。

1. Django Local Library

- 说明 Django Local Library 的基本信息。

2. 开发：HP Windows 10

- 详细说明项目的开发过程。

3. 部署：HW ECS Ubuntu

- 详细说明项目的部署过程。

## 版本

- Django Local Library V2.0
- 部署 URL：http://49.0.244.248:8000/
- 文档编辑工具：Typora 0. 9.96
- 文档更新日期：2022年9月25日

## 设备

1. HP Windows 10
2. HW ECS Ubuntu 18.04

## 软件

- win10：Xshell 7，Sublime Text 3
- Ubuntu：nginx，uWSGI，Venv

## 参考

Django Web 框架 (python) - 学习 Web 开发 | MDN

https://developer.mozilla.org/zh-CN/docs/Learn/Server-side/Django

What is an ISBN? | International ISBN Agency

https://www.isbn-international.org/content/what-isbn

# 开发：HP Windows 10

## 第 1 部分: 搭建开发环境

### 安装 Python

- HP Windows 10 已安装 Python 3.9.7

### 新建虚拟环境

- win + R：cmd

```shell
d:
cd D:\PythonEnvironment\Virtualenv
D:\PythonSoftware\Python\Python39\python.exe -m venv work
work\Scripts\activate
pip3 install django==3.0.*
python -m django --version
pip3 list
deactivate
```

## 第 2 部分: 创建网站的框架

### 创建项目

- win + R: cmd

```shell
d:
cd D:\PythonEnvironment\Virtualenv
work\Scripts\activate
cd D:\mdn
django-admin startproject locallibrary
```

### 创建 catalog 应用

```shell
cd locallibrary
python manage.py startapp catalog
```

### 注册 catalog 应用

- 修改 `locallibrary/locallibrary/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog.apps.CatalogConfig',
]
```

### 语言和时区

```python
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
```

### 链接 URL 映射器

- 修改 `locallibrary/locallibrary/urls.py`
- 相对路径 URL
- `path('catalog/', include('catalog.urls')),`
- 根 URL 重定向
- `path('', RedirectView.as_view(url='/catalog/', permanent=True)),`
- 静态文件 URL
- `urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)`

```python
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

- 增加 `locallibrary/catalog/urls.py`
- 使用相对路径 URL `/catalog/urls.py`

```python
from django.urls import path
from catalog import views

urlpatterns = [

]
```

### 运行数据库迁移

```shell
python manage.py makemigrations
python manage.py migrate
```

### 运行 Web 服务器

```shell
python manage.py runserver

http://127.0.0.1:8000/
http://127.0.0.1:8000/admin
```

- 记录

```shell
Log in | Django site admin
http://127.0.0.1:8000/admin/login/?next=/admin/

Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.

请为员工帐户输入正确的用户名和密码。请注意，两个字段都可能区分大小写。
```

## 第 3 部分: 使用模型

### 图书类别模型：Genre model

1. 属性

- name：名称

2. 方法

- `__str__`：表示模型对象的字符串

### 语言模型：Language model

1. 属性

- name：名称

2. 方法

- `__str__`：表示模型对象的字符串

### 作者模型：Author model

1. 属性

- first_name：名字
- last_name：姓氏
- date_of_birth：出生日期
-  date_of_death：逝世日期

2. 方法

- get_absolute_url：得到绝对路径
- `__str__`：表示模型对象的字符串

3. 引用

- reverse：用于通过反转URL模式来生成URL

### 书籍模型：Book model

1. 属性

- title：书名
- author：作者
- summary：摘要
- isbn：ISBN 国际标准书号
- genre：类别
-  language：语言

2. 方法

- display_genre：表示书籍类别的字符串
- get_absolute_url：得到绝对路径
- `__str__`：表示模型对象的字符串

3. Meta

- ordering = ['title', 'author']

4. 引用

- reverse：用于通过反转URL模式来生成URL

### 书籍实例模型：BookInstance model

1. 属性

- id：ID
-  book：书籍
- imprint：出版社名
- due_back：返还日期
- status：状态
- LOAN_STATUS：Maintenance 维护中，On loan已借出，Available可获得的，Reserved已被预订的。

2. 方法

- `__str__`：表示模型对象的字符串

3. Meta

- ordering = ["due_back"]

### 添加模型

- 修改 `locallibrary/locallibrary/models.py`

```python
from django.db import models
import uuid
from django.urls import reverse

class Genre(models.Model):
	name = models.CharField(
		max_length=200,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
        )

	def __str__(self):
		return self.name

class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['title', 'author']
    
    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return '%s (%s)' % (self.id,self.book.title)
```

### 数据库迁移

```shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## 第 4 部分: Django 管理站点

### 注册模型

- 修改 `/locallibrary/catalog/admin.py`

```python
from django.contrib import admin
from .models import Genre, Language, Author, Book, BookInstance

admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookInstance)
```

### 创建超级用户

```shell
python manage.py createsuperuser

Username: admin
Email address: admin@example.com
Password:123456，隐式输入
```

### 登入站点并添加数据

```shell
http://127.0.0.1:8000/admin

CATALOG
Authors	        Add Change
Book instances	Add Change
Books	        Add Change
Genres	        Add Change
Languages       Add Change
```

## 第 5 部分: 创建我们的主页

### 索引页面

#### URL

- 修改 `/locallibrary/catalog/urls.py` 

```python
urlpatterns = [
    path('', views.index, name='index'),
]
```

#### 视图

```python
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    return render(
    	request,
    	'index.html',
        context={'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors},
    )
```

#### 模版

- 新建 `/locallibrary/catalog/templates/index.html `

```html
{% extends "base_generic.html" %}

{% block content %}
<h1>Local Library Home</h1>

  <p>Welcome to <em>LocalLibrary</em>, a very basic Django website developed as a tutorial example on the Mozilla Developer Network.</p>

<h2>Dynamic content</h2>

  <p>The library has the following record counts:</p>
  <ul>
    <li><strong>Books:</strong> {{ num_books }}</li>
    <li><strong>Copies:</strong> {{ num_instances }}</li>
    <li><strong>Copies available:</strong> {{ num_instances_available }}</li>
    <li><strong>Authors:</strong> {{ num_authors }}</li>
  </ul>

<p>You have visited this page {{ num_visits }}{% if num_visits == 1 %} time{% else %} times{% endif %}.</p>

{% endblock %}
```

### 基本页面

#### 模板

- 新建 `/locallibrary/catalog/templates/base_generic.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>

  {% block title %}<title>Local Library</title>{% endblock %}
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <!-- Add additional CSS in static file -->
  {% load static %}
  <link rel="stylesheet" href="{% static 'css/styles.css' %}">
</head>

<body>

  <div class="container-fluid">

    <div class="row">
      <div class="col-sm-2">
      {% block sidebar %}
      <ul class="sidebar-nav">
          <li><a href="{% url 'index' %}">Home</a></li>
          <li><a href="">All books</a></li>
          <li><a href="">All authors</a></li>
      </ul>
     {% endblock %}
      </div>
      <div class="col-sm-10 ">
      {% block content %}{% endblock %}
      </div>
    </div>

  </div>
</body>
</html>
```

#### CSS

- 新建 `/locallibrary/catalog/static/css/styles.css`

```css
.sidebar-nav {
    margin-top: 20px;
    padding: 0;
    list-style: none;
}
```

## 第 6 部分: 通用列表和详细视图

### 书本清单页面

#### URL

- /locallibrary/catalog/urls.py

```python
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
]
```

#### 视图

- 视图  /locallibrary/catalog/views.py

```python
from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
```

#### 模板

- 模板  /locallibrary/catalog/templates/catalog/book_list.html

```html
{% extends "base_generic.html" %}

{% block content %}
    <h1>Book List</h1>

    {% if book_list %}
    <ul>

      {% for book in book_list %}
      <li>
        <a href="{{ book.get_absolute_url }}">{{ book.title }}</a> ({{book.author}})
      </li>
      {% endfor %}

    </ul>
    {% else %}
      <p>There are no books in the library.</p>
    {% endif %}
{% endblock %}
```

- 修改 /locallibrary/catalog/templates/base_generic.html

```shell
<li><a href="{% url 'index' %}">Home</a></li>
<li><a href="{% url 'books' %}">All books</a></li>
<li><a href="">All authors</a></li>
```

### 书本详细信息页面

#### URL

- /locallibrary/catalog/urls.py

```shell
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
]
```

#### 视图

- 视图  /locallibrary/catalog/views.py

```python
class BookDetailView(generic.DetailView):
    model = Book
```

#### 模板

- /locallibrary/catalog/templates/catalog/book_detail.html

```html
{% extends "base_generic.html" %}

{% block content %}
  <h1>Title: {{ book.title }}</h1>

  <p><strong>Author:</strong> <a href="">{{ book.author }}</a></p> <!-- author detail link not yet defined -->
  <p><strong>Summary:</strong> {{ book.summary }}</p>
  <p><strong>ISBN:</strong> {{ book.isbn }}</p>
  <p><strong>Language:</strong> {{ book.language }}</p>
  <p><strong>Genre:</strong> {% for genre in book.genre.all %} {{ genre }}{% if not forloop.last %}, {% endif %}{% endfor %}</p>

  <div style="margin-left:20px;margin-top:20px">
    <h4>Copies</h4>

    {% for copy in book.bookinstance_set.all %}
    <hr>
    <p class="{% if copy.status == 'a' %}text-success{% elif copy.status == 'm' %}text-danger{% else %}text-warning{% endif %}">{{ copy.get_status_display }}</p>
    {% if copy.status != 'a' %}<p><strong>Due to be returned:</strong> {{copy.due_back}}</p>{% endif %}
    <p><strong>Imprint:</strong> {{copy.imprint}}</p>
    <p class="text-muted"><strong>Id:</strong> {{copy.id}}</p>
    {% endfor %}
  </div>
{% endblock %}
```

### 作者名单页面

#### URL

- /locallibrary/catalog/urls.py

```python
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
]
```

#### 视图

- 视图  /locallibrary/catalog/views.py

```python
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
```

#### 模板

- /locallibrary/catalog/templates/catalog/author_list.html

```html
{% extends "base_generic.html" %}

{% block content %}

<h1>Author List</h1>

{% if author_list %}
  <ul>
  {% for author in author_list %}
    <li>
      <a href="{{ author.get_absolute_url }}">
      {{ author }} ({{author.date_of_birth}} - {% if author.date_of_death %}{{author.date_of_death}}{% endif %})
      </a>
    </li>
  {% endfor %}
 </ul>
{% else %}
  <p>There are no authors available.</p>
{% endif %}
{% endblock %}
```

- 修改 /locallibrary/catalog/templates/base_generic.html

```shell
<li><a href="{% url 'index' %}">Home</a></li>
<li><a href="{% url 'books' %}">All books</a></li>
<li><a href="{% url 'authors' %}">All authors</a></li>
```

### 作者详细信息页面

#### URL

- /locallibrary/catalog/urls.py

```python
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]
```

#### 视图

- /locallibrary/catalog/views.py

```python
class AuthorDetailView(generic.DetailView):
    model = Author
```

#### 模板

- /locallibrary/catalog/templates/catalog/author_detail.html

```html
{% extends "base_generic.html" %}

{% block content %}

<h1>Author: {{ author }} </h1>
<p>{{author.date_of_birth}} - {% if author.date_of_death %}{{author.date_of_death}}{% endif %}</p>

<div style="margin-left:20px;margin-top:20px">
<h4>Books</h4>

<dl>
{% for book in author.book_set.all %}
  <dt><a href="{% url 'book-detail' book.pk %}">{{book}}</a> ({{book.bookinstance_set.all.count}})</dt>
  <dd>{{book.summary}}</dd>
{% endfor %}
</dl>

</div>
{% endblock %}
```

- 修改 /locallibrary/catalog/templates/catalog/book_detail.html

```html
<p><strong>Author:</strong> <a href="{{ book.author.get_absolute_url }}">{{ book.author }}</a></p>
```

## 第 7 部分: 用户身份验证和权限

### 启用身份验证

#### 配置文件

- 路径：locallibrary/locallibrary/settings.py

```shell
INSTALLED_APPS = [
    # Core authentication framework and its default models.
    'django.contrib.auth',
    # 核心认证框架及其默认模型。
    
    # Django content type system 
    # (allows permissions to be associated with models).
    'django.contrib.contenttypes',
    # Django内容类型系统(允许权限与模型相关联)。
]

MIDDLEWARE = [
    # Manages sessions across requests.
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 管理跨请求的会话。
    
    # Associates users with requests using sessions.
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 使用会话将用户与请求相关联。
]
```

### 用户和分组

#### 以命令行创建超级用户

-  Django 管理站点时，已经创建了。

```shell
python manage.py createsuperuser
```

#### 在管理站点创建用户

1. 启动开发服务器。
2. 本地 Web 浏览管理站点。

```shell
http://127.0.0.1:8000/admin/
```

- 创建一个分组

1. 在分组的名称 Name ，输入“Library Members”。

- 创建一个用户

```
Usernamew: zs
Password: zs123456
Personal info
First name: san
Last name: zhang
Email address: zs@example.com
```

#### 用编程方式创建用户

- 示例

```python
from django.contrib.auth.models import User

# Create user and save to the database
user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

# Update fields and then save again
user.first_name = 'John'
user.last_name = 'Citizen'
user.save()
```

### 设置身份验证

#### 主项目

##### URL

- 修改 locallibrary/locallibrary/urls.py

```python
from django.urls import include

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
```

##### 模板目录

- 新建文件夹 /locallibrary/templates/registration/
- 修改 /locallibrary/locallibrary/settings.py

```python
TEMPLATES = [
    {
        'DIRS': ['./templates',],
        'APP_DIRS': True,
    }
]
```

#### 登录页面

##### 模板

- 新建  /locallibrary/templates/registration/login.html

```html
{% extends "base_generic.html" %}

{% block content %}

{% if form.errors %}
<p>Your username and password didn't match. Please try again.</p>
{% endif %}

{% if next %}
    {% if user.is_authenticated %}
    <p>Your account doesn't have access to this page. To proceed,
    please login with an account that has access.</p>
    {% else %}
    <p>Please login to see this page.</p>
    {% endif %}
{% endif %}

<form method="post" action="{% url 'login' %}">
{% csrf_token %}

<div>
  <td>{{ form.username.label_tag }}</td>
  <td>{{ form.username }}</td>
</div>
<div>
  <td>{{ form.password.label_tag }}</td>
  <td>{{ form.password }}</td>
</div>

<div>
  <input type="submit" value="login" />
  <input type="hidden" name="next" value="{{ next }}" />
</div>
</form>

{# Assumes you setup the password_reset view in your URLconf #}
<p><a href="{% url 'password_reset' %}">Lost password?</a></p>

{% endblock %}
```

##### 网址

- 本地 Web 浏览 URL

```shell
http://127.0.0.1:8000/accounts/login/
```

##### 重定向

1. 默认情况

- 如果您尝试登录，将会成功，并且您将被重定向到另一个页面。
- （默认情况下，这将是 http://127.0.0.1:8000/accounts/profile/）

2. 自定义

- 修改 /locallibrary/locallibrary/settings.py

```python
# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'
```

#### 登出页面

##### 网址

- 登出网址

```html
http://127.0.0.1:8000/accounts/logout/
```

##### 模板

- 新建 /locallibrary/templates/registration/logged_out.html

```html
{% extends "base_generic.html" %}

{% block content %}
<p>Logged out!</p>

<a href="{% url 'login'%}">Click here to login again.</a>
{% endblock %}
```

#### 测试

##### 网址

```html
http://127.0.0.1:8000/accounts/login/
http://127.0.0.1:8000/accounts/logout/
```

### 测试验证身份

#### 模板

- 打开基本模板 /locallibrary/catalog/templates/base_generic.html
- 并将以下文本，复制到侧边栏区块 sidebar 中，紧接在 ndblock 模板标记之前。

```html
  <ul class="sidebar-nav">

    ...

   {% if user.is_authenticated %}
     <li>User: {{ user.get_username }}</li>
     <li><a href="{% url 'logout'%}?next={{request.path}}">Logout</a></li>
   {% else %}
     <li><a href="{% url 'login'%}?next={{request.path}}">Login</a></li>
   {% endif %}
  </ul>
```

#### 视图

1. 基于函数

- 限制访问函数的最简单方法，是将login_required装饰器，应用于您的视图函数。
- 如果用户已登录，则您的视图代码将正常执行。
- 如果用户未登录，则会重定向到项目设置（settings.LOGIN_URL）中定义的登录 URL，并将当前绝对路径，作为 URL 参数（"下一个"next）来传递。
- 如果用户成功登录，则会返回到此页面，但这次会进行身份验证。

```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    ...
```

2. 基于类别

- 限制对登录用户的访问的最简单方法，是从LoginRequiredMixin派生。您需要在主视图类之前的超类列表中，首先声明此 mixin。

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class MyView(LoginRequiredMixin, View):
    ...
```

- 这与login_required装饰器，具有完全相同的重定向行为。

### 示例 - 列出当前用户的书

#### 模型

- 书本实例 BookInstance：状态 status ，还书日期 due_back 。
- 将借用者字段borrower，添加到BookInstance模型.
- 添加一个属性，我们可以从模板中调用它，来判断特定的书本实例是否过期。
- 修改 /locallibrary/catalog/models.py

```python
from django.contrib.auth.models import User
from datetime import date

class BookInstance(models.Model):
    
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
```

- 数据库迁移

```shell
python manage.py makemigrations
python manage.py migrate
```

#### 管理员

- 将borrower字段，添加到BookInstanceAdmin类别中的list_display和fieldsets。
- 这将使该字段在 Admin 部分中可见，以便我们可以在需要时将User分配给BookInstance。
- 修改 /locallibrary/catalog/admin.py

```python
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )
```

#### 在借书

##### 借几本书

- 现在可以将书本借给特定用户，然后借出一些BookInstance记录。
- 将他们的借用字段borrowed，设置为您的测试用户，将状态status设置为“On loan”，并在将来和过去设置截止日期。

##### 视图

- 修改 /locallibrary/catalog/views.py

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
```

#### 借书

##### URL

- 修改  /locallibrary/catalog/urls.py

```python
urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]
```

##### 模板

- 新建 /locallibrary/catalog/templates/catalog/bookinstance_list_borrowed_user.html

```html
{% extends "base_generic.html" %}

{% block content %}
    <h1>Borrowed books</h1>

    {% if bookinstance_list %}
    <ul>

      {% for bookinst in bookinstance_list %}
      <li class="{% if bookinst.is_overdue %}text-danger{% endif %}">
        <a href="{% url 'book-detail' bookinst.book.pk %}">{{bookinst.book.title}}</a> ({{ bookinst.due_back }})
      </li>
      {% endfor %}
    </ul>

    {% else %}
      <p>There are no books borrowed.</p>
    {% endif %}
{% endblock %}
```

##### 网址

- 当开发服务器运行时，您现在应该能够在浏览器中，查看登录用户的列表。

```html
http://127.0.0.1:8000/catalog/mybooks/
```

#### 侧栏

- 将列表添加到侧栏。
- 修改基本模板 /locallibrary/catalog/templates/base_generic.html

```html
 <ul class="sidebar-nav">
   {% if user.is_authenticated %}
   <li>User: {{ user.get_username }}</li>
   <li><a href="{% url 'my-borrowed' %}">My Borrowed</a></li>
   <li><a href="{% url 'logout'%}?next={{request.path}}">Logout</a></li>
   {% else %}
   <li><a href="{% url 'login'%}?next={{request.path}}">Login</a></li>
   {% endif %}
 </ul>
```

### 权限

#### 模型

- 在模型“class Meta”部分上，使用 permissions字段，完成权限定义。
- 包含权限名称和权限显示值的嵌套元组

```python
class BookInstance(models.Model):
    ...
    class Meta:
        ...
        permissions = (("can_mark_returned", "Set book as returned"),)
```

- 然后，我们可以将权限分配给管理站点中的图书管理员“Librarian”分组。
- 打开 catalog/models.py，然后添加权限，如上所示。
- 需要重新运行迁移，适当地更新数据库。

```shell
python manage.py makemigrations
python manage.py migrate
```

#### 模板

- 如果用户具有此权限，则 {{ perms.catalog.can_mark_returned }}将为 True，否则为 False。

```html
{% if perms.catalog.can_mark_returned %}
    <!-- We can mark a BookInstance as returned. -->
    <!-- Perhaps add code to link to a "book return" view here. -->
{% endif %}
```

#### 视图

- 在功能视图中，可以使用 permission_required装饰器，或在基于类别的视图中，使用 PermissionRequiredMixin测试权限。
- 模式和行为与登录身份验证相同，但当然您可能需要添加多个权限。

1. 功能视图装饰器：

```python
from django.contrib.auth.decorators import permission_required

@permission_required('catalog.can_mark_returned')
@permission_required('catalog.can_edit')
def my_view(request):
    ...
```

2. 基于类别视图的权限要求 mixin。

```python
from django.contrib.auth.mixins import PermissionRequiredMixin

class MyView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    # Note that 'catalog.can_edit' is just an example
    # the catalog application doesn't have such permission!
```

## 第 8 部分: 使用表单

### 通用编辑-作者

#### 视图

- 打开视图文件（locallibrary/catalog/views.py），并将以下代码块，附加到其底部：

```python
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
```

#### 模板

- 创建模板文件 locallibrary/catalog/templates/catalog/author_form.html，并复制到下面的文本中。

```html
{% extends "base_generic.html" %}

{% block content %}

<form action="" method="post">
    {% csrf_token %}
    <table>
    {{ form.as_table }}
    </table>
    <input type="submit" value="Submit" />

</form>
{% endblock %}
```

- 创建模板文件 locallibrary/catalog/templates/catalog/author_confirm_delete.html ，并复制到下面的文本中。

```python
{% extends "base_generic.html" %}

{% block content %}

<h1>Delete Author</h1>

<p>Are you sure you want to delete the author: {{ author }}?</p>

<form action="" method="POST">
  {% csrf_token %}
  <input type="submit" action="" value="Yes, delete." />
</form>

{% endblock %}
```

#### URL

- 打开 URL 配置文件（locallibrary/catalog/urls.py），并将以下配置，添加到文件的底部：

```python
urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]
```

#### 测试

- 首先，使用具有访问作者编辑页面权限的帐户（由您决定），登录该站点。
- 然后导航到作者创建页面。

```html
http://127.0.0.1:8000/catalog/author/create/
```

- 修改 /locallibrary/catalog/templates/catalog/author_detail.html

```html
<div><a href="{% url 'author_update' author.pk %}">Update detail</a></div>
<div><a href="{% url 'author_delete' author.pk %}">Delete this author</a></div>
```

- 修改 /locallibrary/catalog/templates/catalog/author_list.html

```html
<div><a href="{% url 'author_create' %}">Create a author</a></div>
```

### 通用编辑-书籍

#### 视图

- 打开视图文件（locallibrary/catalog/views.py），并将以下代码块，附加到其底部：

```python
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book

class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
```

#### 模板

- 创建模板文件 locallibrary/catalog/templates/catalog/book_form.html，并复制到下面的文本中。

```html
{% extends "base_generic.html" %}

{% block content %}

<form action="" method="post">
    {% csrf_token %}
    <table>
    {{ form.as_table }}
    </table>
    <input type="submit" value="Submit">
    
</form>
{% endblock %}
```

- 创建模板文件 locallibrary/catalog/templates/catalog/book_confirm_delete.html ，并复制到下面的文本中。

```python
{% extends "base_generic.html" %}

{% block content %}

<h1>Delete Book</h1>

<p>Are you sure you want to delete the book: {{ book }}?</p>

<form action="" method="POST">
  {% csrf_token %}
  <input type="submit" action="" value="Yes, delete.">
</form>

{% endblock %}
```

#### URL

- 打开 URL 配置文件（locallibrary/catalog/urls.py），并将以下配置，添加到文件的底部：

```python
urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]
```

#### 测试

- 首先，使用具有访问作者编辑页面权限的帐户（由您决定），登录该站点。
- 然后导航到作者创建页面。

```html
http://127.0.0.1:8000/catalog/book/create/
```

- 修改 /locallibrary/catalog/templates/catalog/book_detail.html

```html
<div><a href="{% url 'book-update' book.pk %}">Update detail</a></div>
<div><a href="{% url 'book-delete' book.pk %}">Delete this book</a></div>
```

- 修改 /locallibrary/catalog/templates/catalog/book_list.html

```html
<div><a href="{% url 'book-create' %}">Create a book</a></div>
```

### 权限

#### 创建权限

1. 修改 /locallibrary/catalog/models.py

```python
class BookInstance(models.Model):
    ...
    class Meta:
        ...
        permissions = (("can_mark_returned", "Set book as returned"),)
```

2. 需要重新运行迁移，适当地更新数据库。

```shell
python manage.py makemigrations
python manage.py migrate
```

3. 启动服务器，打开站点，创建分组。、

- 将权限分配给管理站点中的图书管理员“Librarian”分组。

#### 视图：装饰权限

1. 功能视图装饰器：

```python
from django.contrib.auth.decorators import permission_required

@permission_required('catalog.can_mark_returned')
@permission_required('catalog.can_edit')
def my_view(request):
    ...
```

2. 基于类别视图的权限要求 mixin。

```python
from django.contrib.auth.mixins import PermissionRequiredMixin

class MyView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    # Note that 'catalog.can_edit' is just an example
    # the catalog application doesn't have such permission!
```

#### 模板：验证权限

- 如果用户具有此权限，则 {{ perms.catalog.can_mark_returned }}将为 True，否则为 False。

```html
{% if perms.catalog.can_mark_returned %}
    <!-- We can mark a BookInstance as returned. -->
    <!-- Perhaps add code to link to a "book return" view here. -->
{% endif %}
```

#### 实例

```html
<div>
	{% if perms.catalog.can_mark_returned %}
	<div><a href="{% url 'author_update' author.pk %}">Update detail</a></div>
	<div><a href="{% url 'author_delete' author.pk %}">Delete this author</a></div>
	{% endif %}
</div>

<div>
	{% if perms.catalog.can_mark_returned %}
	<div><a href="{% url 'author_create' %}">Create a author</a></div>
	{% endif %}
</div>

<div>
    {% if perms.catalog.can_mark_returned %}
    <div><a href="{% url 'book-update' book.pk %}">Update detail</a></div>
    <div><a href="{% url 'book-delete' book.pk %}">Delete this book</a></div>
    {% endif %}
</div>

<div>
    {% if perms.catalog.can_mark_returned %}
    <div><a href="{% url 'book-create' %}">Create a book</a></div>
    {% endif %}
</div>
```

## 第 9 部分：项目包和环境文件

### 项目包

- 名称加上版本号
- locallibrary-V10.zip

### 环境文件

- work-V10.zip
- `pip list` 列出已安装的程序包。
- `pip freeze` 以 requirements 格式，输出已安装的包。

```shell
pip freeze > requirements.txt
```

### 开发文档

- 这个 md 文件导出为 PDF。

# 部署：HW ECS Ubuntu

## 概览

- 设备：HW ECS
- 系统：Ubuntu 18.04.6 LTS
- Python 3.6.9
- uWSGI 2.0.18
- nginx/1.14.0 (Ubuntu)

## 上传项目文件

- 项目压缩包
- Xftp7 上传
- 解压缩
- locallibrary-V10.zip
- D:\mdn\Local-Lib-V10
- /home/ecsuser/mdn

## 搭建运行环境

- 新建虚拟环境

```shell
cd /home/ecsuser/mdn
python3 -m venv work
source work/bin/activate
pip3 install django==3.0.*
python3 -m django --version
pip3 list --format=columns
pip3 freeze > requirements.txt
deactivate
```

## 简单运行

- 激活环境

```shell
cd /home/ecsuser/mdn
source work/bin/activate
pip3 list --format=columns
deactivate
```

- 解压项目包

```shell
unzip locallibrary-V10.zip
cd locallibrary/
```

- 修改 settings.py

```shell
cd locallibrary/locallibrary/
i
DEBUG = False
ALLOWED_HOSTS = ['49.0.244.248']
ESC
:wq
```

- 启动并浏览

```
cd ..
python3 manage.py runserver 0.0.0.0:8000
http://49.0.244.248:8000/
http://49.0.244.248:8000/admin/
```

## 基本部署

### uWSGI

- 安装

```shell
pip3 install wheel
pip3 install uwsgi==2.0.18
pip3 list --format=columns
```

- 查看版本

```shell
pip3 freeze|grep -i 'uwsgi'
```

### 配置 UWSGI

- 新建 /locallibrary/config/uwsgi.ini

#### 模板

```ini
[uwsgi]
http=127.0.0.1:8000                  # 监听http请求，请求此地址，进入服务端
chdir=/home/ecsuser/mdn/locallibrary # 项目根目录->绝对路径
wsgi-file=locallibrary/wsgi.py  	 # 项目中wsgi.py文件目录，相对于当前工作目录
process=4  							 # 进程个数
pidfile=uwsgi.pid  					 # 服务的pid记录文件
daemonize=uwsgi.log  				 # 服务的日志文件位置
vacuum=True  						 # 进程停止后，回收pid
master=True  						 # 启动主进程管理子进程
```

#### 实例

```ini
[uwsgi]  
http=0.0.0.0:8000
chdir=/home/ecsuser/mdn/locallibrary
wsgi-file=locallibrary/wsgi.py
process=2
pidfile=uwsgi.pid
daemonize=uwsgi.log
vacuum=True
master=True
```

- http=0.0.0.0:8000 与 http=:8000 都可以

### 启动并浏览

- 查看uwsgi 进程

```shell
sudo ps -aux | grep uwsgi
sudo ps -aux | grep -i "uwsgi"
```

- 查看占用该端口的进程，杀掉该进程

```shell
sudo lsof -i:8000
sudo kill -9 <pid>
sudo killall uwsgi
```

- 启动 uWSGI

```shell
cd /home/ecsuser/mdn/locallibrary
uwsgi --ini config/uwsgi.ini

http://49.0.244.248:8000/
```

- 停止 uWSGI

```shell
cd /home/ecsuser/mdn/locallibrary
uwsgi --stop uwsgi.pid
```

### Nginx

- 安装

```
apt-get install nginx
```

- 帮助、查看版本

```
nginx -h
nginx -v
```

### Nginx 服务

- 启动、停止和重启

```shell
/etc/init.d/nginx start
/etc/init.d/nginx stop
/etc/init.d/nginx reload
```

### 测试 Nginx

- 启动Nginx后，浏览器访问

```shell
http://49.0.244.248
http://49.0.244.248:80/
```

### 配置 Nginx

- 复制 uwsgi_params，不做改动

```shell
cd /home/ecsuser/mdn
cp /etc/nginx/uwsgi_params locallibrary/config
```

- 新建 /locallibrary/config/nginx.conf

#### 模板

```shell
upstream django {
    server 0.0.0.0:8000;
}

server {
    # 端口号
    listen 80;
    # 服务器ip 或 域名
    server_name 49.0.244.248;
    # 字符集
    charset utf-8;

    # 最大上传限制
    client_max_body_size 75M;

    # 指向 django项目 的 media 目录
    location /media {
        alias /locallibrary/catalog/media;
    }

    # 指向 django项目 的 static 目录
    location /static {
        alias /locallibrary/catalog/static;
    }

    # 将所有非媒体请求转到Django服务器上
    location / {
        # 最上方已定义 upstream django
        uwsgi_pass django;
        # 将所有参数都转到 uwsgi 下
        include locallibrary/config/uwsgi_params;
    }
}
```

#### 实例

```shell
upstream django {
    server 0.0.0.0:8000;
}

server {
    listen 80;
    server_name 49.0.244.248;
    charset utf-8;
    
    client_max_body_size 75M;
    
    location /static {
        alias /home/ecsuser/mdn/locallibrary/catalog/static;
    }

    location / {
        uwsgi_pass django;
        include /home/ecsuser/mdn/locallibrary/config/uwsgi_params;
    }
}
```

#### 声明

- 在默认 nginx.conf 里声明新建的 nginx.conf

```shell
/usr/local/nginx/conf/nginx.conf
/etc/nginx/nginx.conf
/usr/local/etc/nginx/nginx.conf
```

```shell
cd /etc/nginx/
cp nginx.conf nginx.conf.bak
vi nginx.conf
```

- 在 /etc/nginx/nginx.conf 添加如下内容

```shell
http {
    include /home/ecsuser/mdn/locallibrary/config/nginx.conf;
}
```

# 底部

- 快速回到底部。

