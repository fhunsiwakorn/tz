from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class location_thai(models.Model):
    location_id = models.AutoField(primary_key=True)
    district_code = models.CharField(max_length=128, blank=True, default=None)
    district_name = models.CharField(max_length=128, blank=True, default=None)
    zipcode = models.CharField(max_length=128, blank=True, default=None)
    amphur_code = models.CharField(max_length=128, blank=True, default=None)
    amphur_name = models.CharField(max_length=128, blank=True, default=None)
    province_code = models.CharField(max_length=128, blank=True, default=None)
    province_name = models.CharField(max_length=128, blank=True, default=None)


class course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=128, blank=True, default=None)
    course_name = models.CharField(max_length=128, blank=True, default=None)
    active = models.IntegerField(default=1, blank=False)
    crt_date = models.DateTimeField(blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    cancelled = models.IntegerField(default=1, blank=False)

# ev_vat  0  =ไม่รวม Vat,1 = รวม Vat


class course_event(models.Model):
    ev_id = models.AutoField(primary_key=True)
    ev_date_start = models.DateField(blank=True, null=True)
    ev_date_end = models.DateField(blank=True, null=True)
    ev_generation = models.IntegerField(default=0, blank=False)
    ev_remark = models.CharField(max_length=256, blank=True, default=None)
    ev_price = models.FloatField(default=0, blank=False)
    ev_vat = models.IntegerField(default=0, blank=False)
    active = models.IntegerField(default=1, blank=False)
    crt_date = models.DateTimeField(blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    cancelled = models.IntegerField(default=1, blank=False)
    course = models.ForeignKey(course, on_delete=models.CASCADE)

# customer_type  1  = บุคคล ,2 = บริษัท
# customer_status  0  = เป้าหมาย , 1 = ลูกค้า
# pay_type  1  = เงินสด ,2 = เครดิต
# pay_status 1 = ยังไม่ชำระเงิน  , 2 = ชำระเงินไม่ครบ , 3 = ชำระเงินครบแล้ว
# close_the_sale 1 = ปิดการขาย - ขายสำเร็จ , 2= ปิดการขาย - ขายไม่สำเร็จ


class register_main(models.Model):
    register_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    register_number = models.CharField(max_length=64, blank=True, default=None)
    customer_type = models.IntegerField(default=0, blank=False)
    customer_status = models.IntegerField(default=0, blank=False)
    pay_type = models.IntegerField(default=0, blank=False)
    pay_status = models.IntegerField(default=0, blank=False)
    close_the_sale = models.IntegerField(default=0, blank=False)
    crt_date = models.DateTimeField(blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    ev = models.ForeignKey(course_event, on_delete=models.CASCADE)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_create")
    user_update = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_update")


class register_payment(models.Model):
    rp_id = models.AutoField(primary_key=True)
    rp_doc_number = models.CharField(
        max_length=128, blank=True, default=None)
    rp_code_customer = models.CharField(
        max_length=128, blank=True, default=None)
    rp_name_customer = models.CharField(
        max_length=128, blank=True, default=None)
    rp_tax = models.CharField(max_length=128, blank=True, default=None)
    rp_name_seller = models.CharField(
        max_length=128, blank=True, default=None)
    rp_name_contact = models.CharField(
        max_length=128, blank=True, default=None)
    rp_branch = models.CharField(max_length=128, blank=True, default=None)
    rp_address = models.CharField(max_length=512, blank=True, default=None)
    rp_phone = models.CharField(max_length=64, blank=True, default=None)
    rp_email = models.CharField(max_length=64, blank=True, default=None)
    rp_confirm_date_price = models.DateField(blank=True, null=True)
    rp_date_delivery = models.DateField(blank=True, null=True)
    rp_ref1 = models.CharField(max_length=128, blank=True, default=None)
    rp_ref2 = models.CharField(max_length=128, blank=True, default=None)
    active = models.IntegerField(default=1, blank=False)
    crt_date = models.DateTimeField(blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)
    register = models.ForeignKey(register_main, on_delete=models.CASCADE)


class register_payment_items(models.Model):
    rpi_id = models.AutoField(primary_key=True)
    rpi_code = models.CharField(max_length=128, blank=True, default=None)
    rpi_name = models.CharField(max_length=128, blank=True, default=None)
    rpi_quantity = models.IntegerField(default=0, blank=False)
    rpi_unit = models.CharField(max_length=64, blank=True, default=None)
    rpi_price = models.FloatField(default=0, blank=False)
    rpi_price_discount = models.FloatField(default=0, blank=False)
    rpi_price_total = models.FloatField(default=0, blank=False)
    rpi_price_vat = models.FloatField(default=0, blank=False)
    rpi_price_result = models.FloatField(default=0, blank=False)
    rpi_pay = models.FloatField(default=0, blank=False)
    rp = models.ForeignKey(
        register_payment, on_delete=models.CASCADE)
    register = models.ForeignKey(register_main, on_delete=models.CASCADE)


class customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_code = models.CharField(max_length=128, blank=True, default=None)
    customer_name = models.CharField(max_length=128, blank=True, default=None)
    customer_tax = models.CharField(max_length=64, blank=True, default=None)
    customer_phone = models.CharField(max_length=64, blank=True, default=None)
    customer_email = models.CharField(max_length=64, blank=True, default=None)
    customer_address = models.CharField(
        max_length=64, blank=True, default=None)
    location = models.ForeignKey(
        location_thai, on_delete=models.CASCADE)
    register = models.ForeignKey(register_main, on_delete=models.CASCADE)
