from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
# Custom Manager
from datetime import date


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()


# Our Post Model
def upload_location(instance, filename):
    return "%s/%s" %(instance.id,filename)

class Post(models.Model):
    KAT = (
        ('Ogolne','Ogolne'),
        ('Zwierzeta','Zwierzeta'),
        ('Motoryzacja','Motoryzacja'),
        ('Kulinarne','Kulinarne'),
        ('Zdrowie i uroda','Zdrowie i uroda'),
        ('Dom/Mieszkanie','Dom/Mieszkanie'),
        ('Ogrod','Ogrod'),
        ('Majsterkowanie','Majsterkowanie'),
        ('Muzyka','Muzyka'),
        ('Sztuka','Sztuka'),
        ('Sport','Sport'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=140, unique=True)
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.PROTECT)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=250, default="")
    objects = models.Manager()
    # The default manager
    image = models.FileField(null=True,blank=True,upload_to='documents/')
    category = models.CharField(max_length=50,choices=KAT,default='Z')

    # Custom made manager
    published = PublishedManager()

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def approved_edit(self):
        return self.comments.filter(edit_comment=True)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail_view',
                       args=[self.publish.year, self.publish.strftime('%m'), self.publish.strftime('%d'), self.slug])




class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.PROTECT)
    name = models.CharField(max_length=80)
    author = models.ForeignKey(User, related_name='blog_comments', on_delete=models.PROTECT,default="")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Komentarz użytkownika {}, {}'.format(self.name, self.post)
