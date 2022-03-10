from django.db import models


class AccessibleNovelManager(models.Manager):
    def get_queryset(self):
        return [
            novel for novel in super().get_queryset().all() if novel.is_accessible()
        ]
