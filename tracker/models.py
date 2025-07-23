# tracker/models.py
from django.db import models
from django.utils import timezone

# 书籍模型
class Book(models.Model):
    STATUS_CHOICES = (
        ('WANT_TO_READ', '想读'),
        ('READING', '在读'),
        ('FINISHED', '已读'),
    )

    title = models.CharField(max_length=200, verbose_name="书名")
    author = models.CharField(max_length=100, verbose_name="作者")
    total_pages = models.PositiveIntegerField(verbose_name="总页数")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WANT_TO_READ', verbose_name="阅读状态")
    added_date = models.DateTimeField(auto_now_add=True, verbose_name="添加日期")

    def __str__(self):
        return self.title

# 阅读记录模型
class ReadingLog(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='logs', verbose_name="书籍")

    # --- 这里的字段被修改了 ---
    start_page = models.PositiveIntegerField(verbose_name="起始页码")
    end_page = models.PositiveIntegerField(verbose_name="结束页码")
    # --------------------------

    notes = models.TextField(blank=True, null=True, verbose_name="笔记")
    log_date = models.DateField(default=timezone.now, verbose_name="记录日期")

    # (可选但推荐) 添加一个属性，方便计算阅读页数
    @property
    def pages_read_count(self):
        if self.end_page is not None and self.start_page is not None:
            return self.end_page - self.start_page + 1
        return 0

    def __str__(self):
        return f"{self.book.title} - {self.log_date}"