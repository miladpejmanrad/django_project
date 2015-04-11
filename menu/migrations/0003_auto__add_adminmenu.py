# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AdminMenu'
        db.create_table(u'menu_adminmenu', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('options', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'menu', ['AdminMenu'])


    def backwards(self, orm):
        # Deleting model 'AdminMenu'
        db.delete_table(u'menu_adminmenu')


    models = {
        u'menu.adminmenu': {
            'Meta': {'object_name': 'AdminMenu'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'menu.allergen': {
            'Meta': {'object_name': 'Allergen'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'menu.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'menu.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'allergens': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['menu.Allergen']", 'symmetrical': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['menu.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'vegetarian': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'menu.order': {
            'Meta': {'object_name': 'Order'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['menu.MenuItem']", 'symmetrical': 'False'}),
            'modifications': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'ordering'", 'max_length': '64'}),
            'table_number': ('django.db.models.fields.IntegerField', [], {}),
            'tikchen': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'timestamp_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tip': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '8', 'decimal_places': '2'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        u'menu.survey': {
            'Meta': {'object_name': 'Survey'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['menu']