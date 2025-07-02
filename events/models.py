from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = [
    ('curs', 'Curs'),
    ('workshop', 'Workshop'),
]

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    website_url = models.URLField(blank=True, null=True, help_text="Link către site-uri adiacente evenimentului")
    
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='curs'
    )

    def __str__(self):
        return f"{self.title} ({self.start_date} - {self.end_date})"
    
class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} înscris la {self.event.title}"
     
    
class Comment(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentariu de la {self.user.username} la {self.event.title}"
