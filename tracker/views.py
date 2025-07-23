# tracker/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ReadingLogForm, BookForm, UserRegisterForm
from .models import Book
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Book, ReadingLog


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        # --- 新增：我们的“调试打印”魔法 ---
        print("---------- DEBUG START ----------")
        print("表单是否验证通过:", form.is_valid())
        print("表单错误信息:", form.errors.as_json())
        print("----------- DEBUG END -----------")
        # --- 魔法结束 ---

        if form.is_valid():
            user = form.save()
            messages.success(request, f'账户 {user.username} 创建成功！欢迎加入！')
            login(request, user)
            return redirect('book_list')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'tracker/register.html', context)


@login_required
def book_list(request):
    # 我们需要根据当前登录的用户来筛选书籍
    # 首先，我们要确保每本书都和用户关联，我们将在下一步修改模型
    # 暂时我们先假设所有书都是当前用户的

    # 1. 分别查询三种状态的书籍列表
    want_to_read_books = Book.objects.filter(status='WANT_TO_READ').order_by('-added_date')
    reading_books = Book.objects.filter(status='READING').order_by('-added_date')
    finished_books = Book.objects.filter(status='FINISHED').order_by('-added_date')

    # 2. 把三个列表都传递给模板
    context = {
        'want_to_read_books': want_to_read_books,
        'reading_books': reading_books,
        'finished_books': finished_books,
    }

    return render(request, 'tracker/book_list.html', context)

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reading_logs = book.logs.all().order_by('-log_date')

    # --- 新增的表单处理逻辑 ---
    if request.method == 'POST':
        # 如果是POST请求，说明用户提交了表单
        # 用请求中的数据来创建一个表单实例
        form = ReadingLogForm(request.POST)
        if form.is_valid():
            # 如果表单数据有效
            new_log = form.save(commit=False)  # 先不直接存入数据库
            new_log.book = book  # 把这条记录和当前的书籍关联起来
            new_log.save()  # 现在才正式存入数据库
            # 成功后，重定向回当前页面，这样可以防止用户刷新时重复提交表单
            return redirect('book_detail', book_id=book.id)
    else:
        # 如果是GET请求，说明用户只是想看页面
        # 创建一个空的表单实例
        form = ReadingLogForm()
    # --- 逻辑结束 ---

    context = {
        'book': book,
        'reading_logs': reading_logs,
        'form': form,  # <-- 把表单也传递给模板
    }

    return render(request, 'tracker/book_detail.html', context)

@login_required
def add_book(request):
    if request.method == 'POST':
        # 用户提交了数据
        form = BookForm(request.POST)
        if form.is_valid():
            # 表单数据有效，保存到数据库
            new_book = form.save()
            # 成功添加后，重定向到这本书的详情页
            return redirect('book_detail', book_id=new_book.id)
    else:
        # 用户第一次访问，显示一个空的表单
        form = BookForm()

    context = {
        'form': form
    }

    return render(request, 'tracker/add_book.html', context)

@login_required # 同样需要登录才能访问
def edit_log(request, log_id):
    # 1. 根据URL传来的log_id，获取要修改的那条具体的ReadingLog对象
    log = get_object_or_404(ReadingLog, id=log_id)

    if request.method == 'POST':
        # 如果用户提交了修改后的数据
        # 关键：同时传入POST数据和要修改的实例(instance)
        form = ReadingLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save() # 调用save()时，Django知道是更新而不是创建
            messages.success(request, '阅读记录更新成功！')
            # 修改成功后，重定向回这本书的详情页
            return redirect('book_detail', book_id=log.book.id)
    else:
        # 如果是第一次访问（GET请求）
        # 关键：用要修改的实例(instance)来初始化表单，这样表单就会自动填充旧数据
        form = ReadingLogForm(instance=log)

    context = {
        'form': form
    }
    return render(request, 'tracker/edit_log.html', context)

@login_required
def delete_log(request, log_id):
    log = get_object_or_404(ReadingLog, id=log_id)
    book_id = log.book.id # 在删除前，先记下书的ID，以便跳转
    if request.method == 'POST':
        log.delete()
        messages.success(request, '阅读记录已成功删除。')
    # 不管成功与否，都跳转回书籍详情页
    return redirect('book_detail', book_id=book_id)

@login_required
def change_book_status(request, book_id):
    # 这个视图只应该通过POST方法访问，更安全
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        new_status = request.POST.get('status') # 获取表单提交的新状态

        # 检查新状态是否合法
        valid_statuses = [choice[0] for choice in Book.STATUS_CHOICES]
        if new_status in valid_statuses:
            book.status = new_status
            book.save()
            messages.success(request, f'《{book.title}》的状态已更新。')

    # 无论如何，都重定向回书架首页
    return redirect('book_list')


@login_required
def delete_book(request, book_id):
    # 只允许通过POST方法进行删除，更安全
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        # (可选，但推荐) 确保只有书的拥有者才能删除
        # if book.user != request.user:
        #     return redirect('book_list') # 如果不是拥有者，直接踢回首页

        book_title = book.title  # 在删除前记下书名，用于提示信息
        book.delete()
        messages.success(request, f'书籍《{book_title}》已成功删除。')

    # 无论请求方法是什么，最终都返回书架首页
    return redirect('book_list')