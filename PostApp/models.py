from django.db import models
from django.contrib.auth.models import User



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True, null=True)
    image_url = models.ImageField(upload_to='media/Images/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
         db_table = "Post"

    def __str__(self):
        return f"Post by {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
         db_table = "Comment"

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"



class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "Like"
        unique_together = ('post', 'user')  

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"