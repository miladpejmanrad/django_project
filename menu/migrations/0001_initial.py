# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'menu_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'menu', ['Category'])

        # Adding model 'Allergen'
        db.create_table(u'menu_allergen', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ingredient', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'menu', ['Allergen'])

        # Adding model 'MenuItem'
        db.create_table(u'menu_menuitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('vegetarian', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('main_photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.Category'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'menu', ['MenuItem'])

        # Adding M2M table for field allergens on 'MenuItem'
        m2m_table_name = db.shorten_name(u'menu_menuitem_allergens')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('menuitem', models.ForeignKey(orm[u'menu.menuitem'], null=False)),
            ('allergen', models.ForeignKey(orm[u'menu.allergen'], null=False))
        ))
        db.create_unique(m2m_table_name, ['menuitem_id', 'allergen_id'])

        # Adding model 'Order'
        db.create_table(u'menu_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('table_number', self.gf('django.db.models.fields.IntegerField')()),
            ('modifications', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='ordering', max_length=64)),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('tip', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=8, decimal_places=2)),
            ('timestamp_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'menu', ['Order'])

        # Adding M2M table for field menu_items on 'Order'
        m2m_table_name = db.shorten_name(u'menu_order_menu_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('order', models.ForeignKey(orm[u'menu.order'], null=False)),
            ('menuitem', models.ForeignKey(orm[u'menu.menuitem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['order_id', 'menuitem_id'])

        # Adding model 'Survey'
        db.create_table(u'menu_survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'menu', ['Survey'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'menu_category')

        # Deleting model 'Allergen'
        db.delete_table(u'menu_allergen')

        # Deleting model 'MenuItem'
        db.delete_table(u'menu_menuitem')

        # Removing M2M table for field allergens on 'MenuItem'
        db.delete_table(db.shorten_name(u'menu_menuitem_allergens'))

        # Deleting model 'Order'
        db.delete_table(u'menu_order')

        # Removing M2M table for field menu_items on 'Order'
        db.delete_table(db.shorten_name(u'menu_order_menu_items'))

        # Deleting model 'Survey'
        db.delete_table(u'menu_survey')


    models = {
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