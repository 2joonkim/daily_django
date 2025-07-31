from django.contrib.auth import get_user_model
from django.db import models
from PIL import Image
from io import BytesIO
from pathlib import Path
from django.core.files import File

User = get_user_model()


class Todo(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(
        upload_to='todo/thumbnails/', null=True, blank=True,
        help_text="할 일과 관련된 이미지를 업로드하세요."
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 썸네일 처리 로직
        if self.thumbnail:
            try:
                # PIL로 이미지 열기
                img = Image.open(self.thumbnail)
                
                # 이미지가 너무 크면 리사이즈
                if img.height > 800 or img.width > 800:
                    img.thumbnail((800, 800), Image.Resampling.LANCZOS)
                    
                    # 메모리에서 이미지 저장
                    temp_file = BytesIO()
                    img_format = img.format if img.format else 'JPEG'
                    img.save(temp_file, format=img_format, quality=85)
                    temp_file.seek(0)
                    
                    # 파일명 생성
                    file_name = self.thumbnail.name
                    self.thumbnail.save(file_name, File(temp_file), save=False)
                    temp_file.close()
            except Exception as e:
                # 이미지 처리 실패시 그냥 원본 저장
                pass
        
        super().save(*args, **kwargs)


class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'(self.user): (self.message)'