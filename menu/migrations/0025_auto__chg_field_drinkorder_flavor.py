# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'DrinkOrder.flavor'
        db.alter_column('menu_drinkorder', 'flavor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['menu.DrinkFlavor']))

    def backwards(self, orm):

        # Changing field 'DrinkOrder.flavor'
        db.alter_column('menu_drinkorder', 'flavor_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['menu.DrinkFlavor']))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)"},
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
            'current_order': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['menu.Order']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'menu.drink': {
            'Meta': {'object_name': 'Drink'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
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
            'ingredients': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'low_calorie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'main_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'vegetarian': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'menu.notification': {
            'Meta': {'object_name': 'Notification'},
            'drink': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['menu.Order']", 'blank': 'True'}),
            'table_number': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'help'", 'max_length': '64'})
        },
        'menu.order': {
            'Meta': {'object_name': 'Order'},
            'chef': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '64'}),
            'drinks': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['menu.DrinkOrder']", 'blank': 'True'}),
            'freebie_eligible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_items': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['menu.MenuItem']", 'blank': 'True'}),
            'modifications': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'ordering'", 'max_length': '64'}),
            'table_number': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tip': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'default': "'0.00'", 'decimal_places': '2'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        'menu.splitorder': {
            'Meta': {'object_name': 'SplitOrder'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'default': 'None', 'to': "orm['menu.SplitOrderContainer']", 'blank': 'True'}),
            'drinks': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['menu.DrinkOrder']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_items': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['menu.MenuItem']", 'blank': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent_order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Order']"}),
            'tip': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'default': "'0.00'", 'decimal_places': '2'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        'menu.splitordercontainer': {
            'Meta': {'object_name': 'SplitOrderContainer'},
            'drinks': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['menu.DrinkOrder']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_items': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['menu.MenuItem']", 'blank': 'True'}),
            'parent_order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Order']"})
        },
        'menu.survey': {
            'Comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'Meta': {'object_name': 'Survey'},
            'food': ('django.db.models.fields.CharField', [], {'default': "'good'", 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.CharField', [], {'default': "'good'", 'max_length': '64'}),
            'server': ('django.db.models.fields.CharField', [], {'default': "'good'", 'max_length': '64'})
        }
    }

    complete_apps = ['menu']