from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Todo(models.Model):
    TODO = 1
    DOING = 2
    DONE = 3
    CANCELLED = 4
    STATUS_CHOICES = (
        (TODO, 'Todo'),
        (DOING, 'Doing'),
        (DONE, 'Done'),
        (CANCELLED, 'Cancelled')
    )

    UNSET = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    PRIORITY_CHOICES = (
        (UNSET, 'Unset'),
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    name = models.CharField(max_length=225, editable=False)
    description = models.TextField(null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    priority = models.PositiveSmallIntegerField(choices=PRIORITY_CHOICES, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_todo = models.DateTimeField(null=True)
    date_done = models.DateTimeField(null=True)
    copy_of = models.PositiveSmallIntegerField(null=True)

    class Meta:
        db_table = 'todos'

    @classmethod
    def get_status_choices_display(cls):
        return [choice[1] for choice in cls.STATUS_CHOICES]

    def __str__(self):
        return '{} | {} | {}'.format(self.name, self.date_todo, self.date_done)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        if self.status == self.DONE:
            self.date_done = timezone.now()
