from django.db import models

class Notice(models.Model):
    title = models.CharField(max_length=200)  # 공지사항 제목
    content = models.TextField()  # 공지사항 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일

    def __str__(self):
        return self.title