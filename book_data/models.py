from django.db import models
from django.contrib.auth.models import User


#TODO: Reviews with ratings
class Reviews(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=120)
    book_id = models.CharField(max_length=50)
    cover_id = models.CharField(max_length=50)
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reviews"

#TODO: Coments
class Comments(models.Model):
    reviews = models.ForeignKey(Reviews, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    
    class Meta:
        db_table = "comments"


#TODO: Reading List Model
class ReadingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
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

class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'avatar'

class Biography(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'biography'
