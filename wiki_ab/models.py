from django.db import models

class WikiPage(models.Model):
    header = models.CharField(max_length=256)
    pg_url = models.CharField(max_length=64, primary_key=True)
    parent_pg_url = models.CharField(max_length=64, blank=True)
    isdeleted = models.BooleanField(default=False)
    text = models.TextField(blank=True)

    def __unicode__(self):
        return self.header + '\n' + self.text

#    def get_absolute_url(self):
#        return reverse('blogclass') #, kwargs={'pk': self.pk})

    def delete(self, using=None):
        self.isdeleted = True
        self.pg_url = '|!del!|{0}|!del!|'.format(self.pg_url)
        self.save ()

#    class Meta:
#        ordering = ["-date"]

