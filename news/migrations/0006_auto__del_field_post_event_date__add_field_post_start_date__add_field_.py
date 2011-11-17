# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Post.event_date'
        db.delete_column('news_post', 'event_date')

        # Adding field 'Post.start_date'
        db.add_column('news_post', 'start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Post.end_date'
        db.add_column('news_post', 'end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Post.location'
        db.add_column('news_post', 'location', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Post.event_date'
        db.add_column('news_post', 'event_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 11, 16, 12, 10, 42, 268320), blank=True), keep_default=False)

        # Deleting field 'Post.start_date'
        db.delete_column('news_post', 'start_date')

        # Deleting field 'Post.end_date'
        db.delete_column('news_post', 'end_date')

        # Deleting field 'Post.location'
        db.delete_column('news_post', 'location')


    models = {
        'medialibrary.category': {
            'Meta': {'ordering': "['parent__title', 'title']", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['medialibrary.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'medialibrary.mediafile': {
            'Meta': {'object_name': 'MediaFile'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['medialibrary.Category']", 'null': 'True', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'news.post': {
            'Meta': {'object_name': 'Post'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'media_files': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'post_mediafiles'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['medialibrary.MediaFile']"}),
            'photo': ('feincms.module.medialibrary.fields.MediaFileForeignKey', [], {'to': "orm['medialibrary.MediaFile']", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['news']
