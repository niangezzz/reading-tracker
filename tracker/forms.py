# tracker/forms.py
from django import forms
from .models import ReadingLog, Book
from django.contrib.auth.forms import UserCreationForm # <-- 导入
from django.contrib.auth.models import User # <-- 导入

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User # 使用Django内置的User模型
        fields = ['username'] # 我们只让用户填写用户名，密码字段是自带的

class ReadingLogForm(forms.ModelForm):
    class Meta:
        model = ReadingLog
        # --- 修改这里的字段列表 ---
        fields = ['start_page', 'end_page', 'notes', 'log_date']
        # --------------------------
        widgets = {
            # ... widgets可以保持原样，也可以为新字段添加 ...
            'start_page': forms.NumberInput(attrs={'class': 'form-control'}),
            'end_page': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'log_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        # 我们希望用户能填写这几个字段
        fields = ['title', 'author', 'total_pages', 'status']

        # (可选) 美化一下输入框
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入书名'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入作者'}),
            'total_pages': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '这本书总共有多少页'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }