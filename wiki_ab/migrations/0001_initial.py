# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WikiPage'
        db.create_table(u'wiki_ab_wikipage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pg_url', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('parent_pg_url', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('isdeleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'wiki_ab', ['WikiPage'])


    def backwards(self, orm):
        # Deleting model 'WikiPage'
        db.delete_table(u'wiki_ab_wikipage')


    models = {
        u'wiki_ab.wikipage': {
            'Meta': {'object_name': 'WikiPage'},
            'header': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isdeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent_pg_url': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'pg_url': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['wiki_ab']