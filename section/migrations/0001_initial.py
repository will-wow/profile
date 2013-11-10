# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Section'
        db.create_table(u'section_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sort_key', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, blank=True)),
            ('blurb', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('nav', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'section', ['Section'])

        # Adding model 'Slice'
        db.create_table(u'section_slice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['section.Section'])),
            ('sort_key', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=225, blank=True)),
        ))
        db.send_create_signal(u'section', ['Slice'])

        # Adding model 'Grid'
        db.create_table(u'section_grid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['section.Slice'])),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('sort_key', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('img', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'section', ['Grid'])

        # Adding model 'Link'
        db.create_table(u'section_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('grid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['section.Grid'])),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('section_link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['section.Section'], null=True, blank=True)),
            ('other_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('file_link', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'section', ['Link'])


    def backwards(self, orm):
        # Deleting model 'Section'
        db.delete_table(u'section_section')

        # Deleting model 'Slice'
        db.delete_table(u'section_slice')

        # Deleting model 'Grid'
        db.delete_table(u'section_grid')

        # Deleting model 'Link'
        db.delete_table(u'section_link')


    models = {
        u'section.grid': {
            'Meta': {'ordering': "['slice__section__title', 'slice__sort_key', 'sort_key']", 'object_name': 'Grid'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'slice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['section.Slice']"}),
            'sort_key': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'section.link': {
            'Meta': {'ordering': "['grid__slice__section__title', 'grid__slice__sort_key', 'grid__sort_key', 'display']", 'object_name': 'Link'},
            'display': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file_link': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'grid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['section.Grid']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'section_link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['section.Section']", 'null': 'True', 'blank': 'True'})
        },
        u'section.section': {
            'Meta': {'ordering': "['sort_key', 'title']", 'object_name': 'Section'},
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nav': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'sort_key': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'section.slice': {
            'Meta': {'ordering': "['sort_key']", 'object_name': 'Slice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['section.Section']"}),
            'sort_key': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '225', 'blank': 'True'})
        }
    }

    complete_apps = ['section']