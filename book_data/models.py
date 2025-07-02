from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatars/avatar.png', upload_to='avatars')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

class BasePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(max_length=32)

    class Meta:
        abstract = True

class TextPosts(BasePost):
    text = models.TextField()
    class Meta:
        db_table = 'text_posts'

class ImagePosts(BasePost):
    image = models.ImageField(upload_to='images/')
    class Meta:
        db_table = 'image_posts'

class VideoPosts(BasePost):
    video = models.FileField(upload_to='videos/')
    class Meta:
        db_table = 'video_posts'


class Following(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "following"
        unique_together = ('follower', 'following')

# Reviews with ratings
class Reviews(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=120)
    book_id = models.CharField(max_length=50)
    cover_id = models.CharField(max_length=50)
    cover_url = models.URLField()
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reviews"

# Coments
class Comments(models.Model):
    reviews = models.ForeignKey(Reviews, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    
    class Meta:
        db_table = "comments"

# Reading List Model
class ReadingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    author_name = models.CharField(max_length=256)
    book_id = models.CharField(max_length=50)
    cover_id = models.CharField(max_length=50, null=True, blank=True)
    
    
    @property
    def user_rating(self):
        review = Reviews.objects.filter(user=self.user, book_id=self.book_id).first()
        return review.rating if review else None

                
    def __str__(self):
        return f"{self.title} ({self.book_id})"
    
    class Meta:
        db_table = "reading_list"

class FavoriteBooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    book_id = models.CharField(max_length=50)
    cover_id = models.CharField(max_length=50, null=True, blank=True)
    cover_url = models.URLField()

    class Meta:
        db_table = 'favorite_books'