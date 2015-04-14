# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OrderSplit'
        db.create_table('menu_ordersplit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.Order'])),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=8)),
            ('tip', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=8, default='0.00')),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('menu', ['OrderSplit'])

        # Adding M2M table for field menu_items on 'OrderSplit'
        m2m_table_name = db.shorten_name('menu_ordersplit_menu_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ordersplit', models.ForeignKey(orm['menu.ordersplit'], null=False)),
            ('menuitem', models.ForeignKey(orm['menu.menuitem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ordersplit_id', 'menuitem_id'])

        # Adding M2M table for field drinks on 'OrderSplit'
        m2m_table_name = db.shorten_name('menu_ordersplit_drinks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ordersplit', models.ForeignKey(orm['menu.ordersplit'], null=False)),
            ('drinkorder', models.ForeignKey(orm['menu.drinkorder'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ordersplit_id', 'drinkorder_id'])


    def backwards(self, orm):
        # Deleting model 'OrderSplit'
        db.delete_table('menu_ordersplit')

        # Removing M2M table for field menu_items on 'OrderSplit'
        db.delete_table(db.shorten_name('menu_ordersplit_menu_items'))

        # Removing M2M table for field drinks on 'OrderSplit'
        db.delete_table(db.shorten_name('menu_ordersplit_drinks'))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'related_name': "'user_set'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'ordering': "('name',)", 'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        'menu.cookstatus': {
            'Meta': {'object_name': 'CookStatus'},
            'cook_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'current_order': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['menu.Order']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'flavor': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['menu.DrinkFlavor']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'menu.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'allergens': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['menu.Allergen']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'low_calorie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'order': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['menu.Order']"}),
            'table_number': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'default': "'help'"})
        },
        'menu.order': {
            'Meta': {'object_name': 'Order'},
            'chef': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '64', 'blank': 'True'}),
            'drinks': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['menu.DrinkOrder']", 'blank': 'True'}),
            'freebie_eligible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_items': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['menu.MenuItem']", 'blank': 'True'}),
            'modifications': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '64', 'default': "'ordering'"}),
            'table_number': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'tip': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '8', 'default': "'0.00'"}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '8'})
        },
        'menu.ordersplit': {
            'Meta': {'object_name': 'OrderSplit'},
            'drinks': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['menu.DrinkOrder']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_items': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['menu.MenuItem']", 'blank': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent_order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Order']"}),
            'tip': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '8', 'default': "'0.00'"}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '8'})
        },
        'menu.survey': {
            'Comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'Meta': {'object_name': 'Survey'},
            'food': ('django.db.models.fields.CharField', [], {'max_length': '64', 'default': "'good'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.CharField', [], {'max_length': '64', 'default': "'good'"}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '64', 'default': "'good'"})
        }
    }

    complete_apps = ['menu']