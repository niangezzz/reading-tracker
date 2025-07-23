# tracker/admin.py
from django.contrib import admin
from .models import Book, ReadingLog

# 自定义后台显示
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'total_pages', 'added_date')
    list_filter = ('status', 'author')
    search_fields = ('title', 'author')


class ReadingLogAdmin(admin.ModelAdmin):
    # 将 'pages_read' 替换为 'start_page', 'end_page' 和我们新加的计算属性 'pages_read_count'
    list_display = ('book', 'start_page', 'end_page', 'pages_read_count', 'log_date')

    # 这是一个好习惯：告诉后台'pages_read_count'是一个只读字段，因为它是由函数计算得出的
    readonly_fields = ('pages_read_count',)

# 注册模型到Admin
admin.site.register(Book, BookAdmin)
admin.site.register(ReadingLog, ReadingLogAdmin)