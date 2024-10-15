from django.db import models
from profiles.models import CustomUser

"""
A model for storing user posts.
"""
class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    description = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to='media/prost_pictures/', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user}({self.date}) --> {self.description}[{self.id}]'
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-date', 'user']


"""
A model for storing comments under posts from users.
"""
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=400, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username}({self.date}) --> {self.post} ({self.text})'
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-date', 'user']


"""
A model for storing users' likes on posts.
"""
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user}({self.date}) --> {self.post}'
    
    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        ordering = ['-date', 'user']



"""
A model for storing post categories.
"""
class Category(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']


"""
A model for linking posts to multiple categories.
"""
class Category_Of_Post(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.category} ---> {self.post}'
    
    class Meta:
        verbose_name = 'Category_Of_Post'
        verbose_name_plural = 'Category_Of_Posts'
