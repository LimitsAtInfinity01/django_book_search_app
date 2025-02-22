from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#TODO: Add users model


#TODO: Reviews with ratings
class Reviews(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    content = models.TextField()
    rating = models.IntegerField()
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "reviews"

#TODO: Coments
class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    data_time = models.DateTimeField()

    def __str__(self):
        return self.content
    
    class Meta:
        db_table = "comments"


#TODO: Reading List Model
class ReadingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    book_id = models.CharField(max_length=50)
    cover_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} ({self.book_id})"
    
    class Meta:
        db_table = "reading_list"