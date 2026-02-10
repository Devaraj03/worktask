from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class Work(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    assigned_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="assigned_works")
    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class WorkStatus(models.Model):

    WORK_STATES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('CLOSED', 'Closed'),
    ]
    work = models.ForeignKey(Work,on_delete=models.CASCADE,related_name='states')
    state = models.CharField(max_length=20,choices=WORK_STATES,default='OPEN')

    position = models.PositiveIntegerField(default=0)

    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.state == 'CLOSED' and self.closed_at is None:
            self.closed_at = timezone.now()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['position']
        unique_together = ('work', 'state')

    def __str__(self):
        return f"{self.work.title} - {self.state}"
