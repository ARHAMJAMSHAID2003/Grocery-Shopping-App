# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    quantity = models.IntegerField()
    added_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cart'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Locations(models.Model):
    location_id = models.AutoField(primary_key=True)
    city = models.TextField()
    state = models.TextField()
    zip_code = models.BigIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    region = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locations'


class OrderItems(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order_id = models.BigIntegerField()
    product_id = models.BigIntegerField()
    quantity = models.BigIntegerField()
    unit_price = models.FloatField()
    subtotal = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_items'


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField()
    store_id = models.BigIntegerField(blank=True, null=True)
    order_date = models.TextField()
    total_amount = models.FloatField()
    status = models.TextField()
    delivery_address = models.TextField(blank=True, null=True)
    payment_method = models.TextField(blank=True, null=True)
    delivery_time = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.TextField()
    description = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    price = models.FloatField()
    store_id = models.BigIntegerField(blank=True, null=True)
    stock_quantity = models.BigIntegerField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class Stores(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.TextField()
    location_id = models.BigIntegerField()
    manager_name = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    opening_hours = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stores'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.TextField()
    email = models.TextField()
    password_hash = models.CharField(max_length=255, blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    registration_date = models.TextField(blank=True, null=True)
    location_id = models.BigIntegerField(blank=True, null=True)
    age = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
