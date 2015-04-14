# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'OrderSplit'
        db.delete_table('menu_ordersplit')

        # Removing M2M table for field menu_items on 'OrderSplit'
        db.delete_table(db.shorten_name('menu_ordersplit_menu_items'))

        # Removing M2M table for field drinks on 'OrderSplit'
        db.delete_table(db.shorten_name('menu_ordersplit_drinks'))

        # Deleting model 'OrderSplitItems'
        db.delete_table('menu_ordersplititems')

        # Removing M2M table for field menu_items on 'OrderSplitItems'
        db.delete_table(db.shorten_name('menu_ordersplititems_menu_items'))

        # Removing M2M table for field drinks on 'OrderSplitItems'
        db.delete_table(db.shorten_name('menu_ordersplititems_drinks'))

        # Adding model 'SplitOrder'
        db.create_table('menu_splitorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('container', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.SplitOrderContainer'])),
            ('parent_order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.Order'])),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=8)),
            ('tip', self.gf('django.db.models.fields.DecimalField')(default='0.00', decimal_places=2, max_digits=8)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('menu', ['SplitOrder'])

        # Adding M2M table for field menu_items on 'SplitOrder'
        m2m_table_name = db.shorten_name('menu_splitorder_menu_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('splitorder', models.ForeignKey(orm['menu.splitorder'], null=False)),
            ('menuitem', models.ForeignKey(orm['menu.menuitem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['splitorder_id', 'menuitem_id'])

        # Adding M2M table for field drinks on 'SplitOrder'
        m2m_table_name = db.shorten_name('menu_splitorder_drinks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('splitorder', models.ForeignKey(orm['menu.splitorder'], null=False)),
            ('drinkorder', models.ForeignKey(orm['menu.drinkorder'], null=False))
        ))
        db.create_unique(m2m_table_name, ['splitorder_id', 'drinkorder_id'])

        # Adding model 'SplitOrderContainer'
        db.create_table('menu_splitordercontainer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.Order'])),
        ))
        db.send_create_signal('menu', ['SplitOrderContainer'])

        # Adding M2M table for field menu_items on 'SplitOrderContainer'
        m2m_table_name = db.shorten_name('menu_splitordercontainer_menu_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('splitordercontainer', models.ForeignKey(orm['menu.splitordercontainer'], null=False)),
            ('menuitem', models.ForeignKey(orm['menu.menuitem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['splitordercontainer_id', 'menuitem_id'])

        # Adding M2M table for field drinks on 'SplitOrderContainer'
        m2m_table_name = db.shorten_name('menu_splitordercontainer_drinks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('splitordercontainer', models.ForeignKey(orm['menu.splitordercontainer'], null=False)),
            ('drinkorder', models.ForeignKey(orm['menu.drinkorder'], null=False))
        ))
        db.create_unique(m2m_table_name, ['splitordercontainer_id', 'drinkorder_id'])


    def backwards(self, orm):
        # Adding model 'OrderSplit'
        db.create_table('menu_ordersplit', (
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=8)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.Order'])),
            ('items_left_to_pay', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.OrderSplitItems'], blank=True, null=True)),
            ('tip', self.gf('django.db.models.fields.DecimalField')(default='0.00', decimal_places=2, max_digits=8)),
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

        # Adding model 'OrderSplitItems'
        db.create_table('menu_ordersplititems', (
            ('parent_order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.Order'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('menu', ['OrderSplitItems'])

        # Adding M2M table for field menu_items on 'OrderSplitItems'
        m2m_table_name = db.shorten_name('menu_ordersplititems_menu_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ordersplititems', models.ForeignKey(orm['menu.ordersplititems'], null=False)),
            ('menuitem', models.ForeignKey(orm['menu.menuitem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ordersplititems_id', 'menuitem_id'])

        # Adding M2M table for field drinks on 'OrderSplitItems'
        m2m_table_name = db.shorten_name('menu_ordersplititems_drinks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ordersplititems', models.ForeignKey(orm['menu.ordersplititems'], null=False)),
            ('drinkorder', models.ForeignKey(orm['menu.drinkorder'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ordersplititems_id', 'drinkorder_id'])

        # Deleting model 'SplitOrder'
        db.delete_table('menu_splitorder')

        # Removing M2M table for field menu_items on 'SplitOrder'
        db.delete_table(db.shorten_name('menu_splitorder_menu_items'))

        # Removing M2M table for field drinks on 'SplitOrder'
        db.delete_table(db.shorten_name('menu_splitorder_drinks'))

        # Deleting model 'SplitOrderContainer'
        db.delete_table('menu_splitordercontainer')

        # Removing M2M table for field menu_items on 'SplitOrderContainer'
        db.delete_table(db.shorten_name('menu_splitordercontainer_menu_items'))

        # Removing M2M table for field drinks on 'SplitOrderContainer'
        db.delete_table(db.shorten_name('menu_splitordercontainer_drinks'))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'"},
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
            'current_order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Order']", 'blank': 'True', 'null': 'True'}),
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
            'flavor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.DrinkFlavor']", 'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'menu.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'allergens': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['menu.Allergen']", 'symmetrical': 'False'}),
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
            'drink': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Order']", 'blank': 'True', 'null': 'True'}),
            'table_number': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'help'", 'max_length': '64'})
        },
        'menu.order': {
            'Meta': {'object_name': 'Order'},
            'chef': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True', 'null': 'True'}),
            'drinks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['menu.DrinkOrder']", 'symmetrical': 'False', 'blank': 'True'}),
            'freebie_eligible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['menu.MenuItem']", 'symmetrical': 'False', 'blank': 'True'}),
            'modifications': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'ordering'", 'max_length': '64'}),
            'table_number': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tip': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'decimal_places': '2', 'max_digits': '8'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '8'})
        },
        'menu.splitorder': {
            'Meta': {'object_name': 'SplitOrder'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.SplitOrderContainer']"}),
            'drinks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['menu.DrinkOrder']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['menu.MenuItem']", 'symmetrical': 'False', 'blank': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent_order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Order']"}),
            'tip': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'decimal_places': '2', 'max_digits': '8'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '8'})
        },
        'menu.splitordercontainer': {
            'Meta': {'object_name': 'SplitOrderContainer'},
            'drinks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['menu.DrinkOrder']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['menu.MenuItem']", 'symmetrical': 'False', 'blank': 'True'}),
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