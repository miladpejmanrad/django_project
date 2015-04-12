# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DrinkFlavor'
        db.create_table('menu_drinkflavor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flavor', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('menu', ['DrinkFlavor'])

        # Adding model 'DrinkOrder'
        db.create_table('menu_drinkorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('drink', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.Drink'])),
            ('flavor', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['menu.DrinkFlavor'], blank=True)),
        ))
        db.send_create_signal('menu', ['DrinkOrder'])

        # Adding model 'Drink'
        db.create_table('menu_drink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('price', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=8)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.Category'])),
        ))
        db.send_create_signal('menu', ['Drink'])

        # Adding M2M table for field drinks on 'Order'
        m2m_table_name = db.shorten_name('menu_order_drinks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('order', models.ForeignKey(orm['menu.order'], null=False)),
            ('drinkorder', models.ForeignKey(orm['menu.drinkorder'], null=False))
        ))
        db.create_unique(m2m_table_name, ['order_id', 'drinkorder_id'])


    def backwards(self, orm):
        # Deleting model 'DrinkFlavor'
        db.delete_table('menu_drinkflavor')

        # Deleting model 'DrinkOrder'
        db.delete_table('menu_drinkorder')

        # Deleting model 'Drink'
        db.delete_table('menu_drink')

        # Removing M2M table for field drinks on 'Order'
        db.delete_table(db.shorten_name('menu_order_drinks'))


    models = {
        'menu.adminmenu': {
            'Meta': {'object_name': 'AdminMenu'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'menu.allergen': {
            'Meta': {'object_name': 'Allergen'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'menu.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'menu.drink': {
            'Meta': {'object_name': 'Drink'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '8'})
        },
        'menu.drinkflavor': {
            'Meta': {'object_name': 'DrinkFlavor'},
            'flavor': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'menu.drinkorder': {
            'Meta': {'object_name': 'DrinkOrder'},
            'drink': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Drink']"}),
            'flavor': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['menu.DrinkFlavor']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'menu.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'allergens': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['menu.Allergen']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '8'}),
            'vegetarian': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'menu.notification': {
            'Meta': {'object_name': 'Notification'},
            'drink': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'table_number': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'default': "'help'"})
        },
        'menu.order': {
            'Meta': {'object_name': 'Order'},
            'drinks': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['menu.DrinkOrder']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_items': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['menu.MenuItem']", 'blank': 'True'}),
            'modifications': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '64', 'default': "'ordering'"}),
            'table_number': ('django.db.models.fields.IntegerField', [], {}),
            'tikchen': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '64', 'blank': 'True'}),
            'timestamp_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tip': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '8', 'default': "'0.00'"}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '8'})
        },
        'menu.survey': {
            'Meta': {'object_name': 'Survey'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['menu']