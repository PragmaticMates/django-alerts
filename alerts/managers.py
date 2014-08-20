from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet


class AlertQuerySet(QuerySet):
    def for_recipient(self, recipient):
        return self.filter(recipient=recipient)

    def by_tag(self, tag):
        return self.filter(tag=tag)

    def by_tags(self, tags):
        search_q = Q()
        for tag in tags:
            search_q |= Q(**{'tag__exact': tag})
        return self.filter(search_q)

    def of_subject(self, subject):
        return self.filter(subject_type=ContentType.objects.get_for_model(subject), subject_id=subject.pk)

    def read(self):
        return self.filter(is_read=True)

    def unread(self):
        return self.filter(is_read=False)
    
    def pushed(self):
        return self.filter(is_pushed=True)
    
    def not_pushed(self):
        return self.filter(is_pushed=False)
    
    def email_sent(self):
        return self.filter(is_email_sent=True)
    
    def not_email_sent(self):
        return self.filter(is_email_sent=False)

    def mark_as_read(self, recipient):
        """
        Mark as read any unread messages in the current queryset for specified recipient.
        """
        # We want to filter out read ones, as later we will store
        # the time they were marked as read.
        qs = self.unread().for_recipient(recipient)
        qs.update(is_read=True)

    def mark_as_unread(self, recipient):
        """
        Mark as unread any read messages in the current queryset for specified recipient.
        """
        # We want to filter out read ones, as later we will store
        # the time they were marked as read.
        qs = self.read().for_recipient(recipient)
        qs.update(is_read=False)


class AlertManager(models.Manager):
    # TODO: deprecated
    def get_query_set(self):
        return self.get_queryset()

    def get_queryset(self):
        return AlertQuerySet(self.model, using=self._db)

    def for_recipient(self, user):
        return self.get_queryset().for_recipient(user)

    def by_tag(self, tag):
        return self.get_queryset().by_tag(tag)

    def of_subject(self, subject):
        return self.get_queryset().of_subject(subject)

    def read(self):
        return self.get_queryset().read()

    def unread(self):
        return self.get_queryset().unread()
    
    def pushed(self):
        return self.get_queryset().pushed()
    
    def not_pushed(self):
        return self.get_queryset().not_pushed()
    
    def email_sent(self):
        return self.get_queryset().email_sent()
    
    def not_email_sent(self):
        return self.get_queryset().not_email_sent()

    def mark_as_read(self, recipient):
        return self.get_queryset().mark_as_read(recipient)

    def mark_as_unread(self, recipient):
        return self.get_queryset().mark_as_unread(recipient)
