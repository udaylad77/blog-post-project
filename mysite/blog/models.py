from django.db import models
from django.utils import timezone
from django.urls import reverse

# SuperUserInformation
# User: Uday
# Email: udaylad77@gmail.com
# Password: Dad45mom


# Create your models here.
# After creating a post or comment where should the website take them, for that detail view is used.


class Post(models.Model):
    """
    This is Model class 'Post' for manage Post related information.
    """
    # author connected to the authorization User
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)  # Admin side
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


    def publish(self):
        """
        It take time when hit publish button.
        :return: -
        """
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        """
        It will approve comment.
        :return: -
        """
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        """
        After creating a post and hit published go to the "post_detail" page for the pk of the post you just created.
        :return: reverse
        """
        return reverse("post_detail", kwargs={'pk': self.pk})

    def __str__(self):
        """
        String representation.
        :return: title
        """
        return self.title


class Comment(models.Model):
    """
    This is Model class 'Comment' for manage Comment related information.
    """
    # 'blog.Post' means --> django app name 'blog' and Model class name 'Post'
    # Each comment connected to each Post
    post = models.ForeignKey('blog.Post', related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)


    def approve(self):
        """
        It will approve comment of particular Post
        :return:
        """
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        """
        After creating a comment and hit published go to the "post_list" page.
        Comment need to be approved by super user. for that going back to the Home page("post_list") of all post.
        :return: reverse
        """
        return reverse("post_list")

    def __str__(self):
        """
        String representation.
        :return: text
        """
        return self.text