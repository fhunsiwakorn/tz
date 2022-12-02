from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from datetime import date, timedelta
from dateutil import rrule

from ..common import defaultTitle
from ..models import course, course_event, customers, location_thai, register_main, register_payment, register_payment_items
from ..functions import dateTimeIntNow, dateTimeNow, dmytoymd, month_fomat, ternaryZero, treeDigit


# https://docs.djangoproject.com/en/1.11/ref/models/querysets/#gt


@login_required(login_url='/login')
def register_home(request):
    title = defaultTitle

    try:
        register_id = request.session['register_id']
        content_regist = register_main.objects.get(register_id=register_id)
    except KeyError:
        content_regist = None
    # print(register_id)
    _date = date.today()
    hundredDaysLater = _date + timedelta(days=90)
    obj = []
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=_date, until=hundredDaysLater):
        _newdate = str(dt).split(" ")[0]
        yearstart = _newdate.split("-")[0]
        monthstart = _newdate.split("-")[1]
        label = month_fomat(monthstart) + " " + yearstart
        # print(label)
        result = course_event.objects.select_related("course").filter(
            cancelled=1, active=1, ev_date_start__month=int(monthstart), ev_date_start__year=int(yearstart)).order_by("ev_date_start")
        content = {"label": label, "data": result}
        obj.append(content)
    # print(obj)
    context = {'title': title,  'data': obj, 'content_regist': content_regist}
    return render(request, 'register/register.html', context)


@login_required(login_url='/login')
def register_reset(request):
    try:
        del request.session['register_id']
    except KeyError:
        pass
    return redirect("/")


@login_required(login_url='/login')
def register_create(request):
    current_user = request.user
    seller_id = current_user.id
    ev_id = request.POST['ev_id']
    customer_type = request.POST['customer_type']
    pay_type = request.POST['pay_type']
    if int(pay_type) == 1:
        close_the_sale = 1
    else:
        close_the_sale = 0
    object = register_main.objects.create(
        register_number="-",
        customer_type=customer_type,
        customer_status=0,
        pay_type=pay_type,
        pay_status=1,
        close_the_sale=close_the_sale,
        crt_date=dateTimeNow(),
        upd_date=dateTimeNow(),
        ev_id=ev_id,
        seller_id=seller_id,
        user_update_id=seller_id
    )
    object.refresh_from_db()
    register_id = object.register_id
    # print(register_id)
    request.session['register_id'] = str(register_id)
    return redirect("/")


@login_required(login_url='/login')
def customer_create(request):

    try:
        register_id = request.session['register_id']
        content_regist = register_main.objects.get(register_id=register_id)
        if not content_regist:
            return redirect("/")
    except KeyError:
        register_id = None
        content_regist = None
        return redirect("/")
    chkcustomer = customers.objects.filter(register_id=register_id).count()
    if chkcustomer > 0:
        return redirect("/register/reset")
    customer_code = dateTimeIntNow()
    customer_name = request.POST['customer_name']
    customer_tax = request.POST['customer_tax']
    customer_phone = request.POST['customer_phone']
    customer_email = request.POST['customer_email']
    customer_address = request.POST['customer_address']
    location_id = request.POST['location_id']
    customers.objects.create(
        customer_code=customer_code,
        customer_name=customer_name,
        customer_tax=customer_tax,
        customer_phone=customer_phone,
        customer_email=customer_email,
        customer_address=customer_address,
        location_id=location_id,
        register_id=register_id
    )

    # Update Regisrer
    month_current = date.today().month
    year_current = str(int(date.today().year) + 543)
    totaldata = register_main.objects.filter(
        crt_date__month=month_current).exclude(register_number="-").count()
    running_number = treeDigit(totaldata + 1)
    register_number = "R" + year_current[2:4] + "/" + \
        str(month_current) + "/" + str(running_number)
    content = register_main.objects.get(pk=register_id)
    content.register_number = register_number
    content.save()

    try:
        del request.session['register_id']
    except KeyError:
        pass
    return redirect("/register/payment/" + str(register_id))


@login_required(login_url='/login')
def register_detail(request, register_id):
    title = defaultTitle
    try:
        content_regist = register_main.objects.get(register_id=register_id)
    except:
        content_regist = None
        return redirect("/")
    content_customer = customers.objects.select_related("location").filter(
        register_id=register_id).first()
    content_course = course_event.objects.select_related(
        "course").get(ev_id=content_regist.ev_id)
    context = {'title': title,  'content_regist': content_regist,
               'content_customer': content_customer, 'content_course': content_course}
    return render(request, 'register/register_detail.html', context)


@login_required(login_url='/login')
def payment(request, register_id):
    title = defaultTitle
    try:
        content = customers.objects.select_related(
            "register", "location").get(register_id=register_id)
    except:
        content = None
        return redirect("/")
    content_regist = register_main.objects.select_related(
        "seller", "ev").get(register_id=register_id)
    content_course = course_event.objects.select_related(
        "course").get(ev_id=content_regist.ev_id)
    # print(content)
    context = {'title': title,  'data': content,
               'content_regist': content_regist, 'content_course': content_course}
    return render(request, 'register/register_payment.html', context)


@login_required(login_url='/login')
def payment_create(request):
    now = date.today()
    # Main
    register_id = request.POST['register_id']
    rp_code_customer = request.POST['rp_code_customer']
    rp_name_customer = request.POST['rp_name_customer']
    rp_tax = request.POST['rp_tax']
    rp_name_seller = request.POST['rp_name_seller']
    rp_name_contact = request.POST['rp_name_contact']
    rp_branch = request.POST['rp_branch']
    rp_address = request.POST['rp_address']
    rp_phone = request.POST['rp_phone']
    rp_email = request.POST['rp_email']
    rp_confirm_date_price = dmytoymd(
        request.POST.get("rp_confirm_date_price", now.strftime("%d/%m/%Y")))
    rp_date_delivery = dmytoymd(
        request.POST.get("rp_date_delivery", now.strftime("%d/%m/%Y")))
    rp_ref1 = request.POST['rp_ref1']
    rp_ref2 = request.POST['rp_ref2']
    check_type = register_main.objects.get(register_id=register_id)
    pay_type = check_type.pay_type
    if pay_type == 1:
        active = 1
    else:
        active = 0
    month_current = date.today().month
    year_current = str(int(date.today().year) + 543)
    totaldata = register_payment.objects.filter(
        crt_date__month=month_current).count()
    running_number = treeDigit(totaldata + 1)
    rp_doc_number = "TZ" + year_current[2:4] + "/" + \
        str(month_current) + "/" + str(running_number)
    # Item
    rpi_code = request.POST['rpi_code']
    rpi_name = request.POST['rpi_name']
    rpi_quantity = request.POST['rpi_quantity']
    rpi_unit = request.POST['rpi_unit']
    rpi_price = request.POST['rpi_price']
    rpi_price_discount = request.POST['rpi_price_discount']
    rpi_price_total = request.POST['rpi_price_total']
    rpi_price_vat = request.POST['rpi_price_vat']
    rpi_price_result = request.POST['rpi_price_result']

    # Crate Main
    object = register_payment.objects.create(
        rp_doc_number=rp_doc_number,
        rp_code_customer=rp_code_customer,
        rp_name_customer=rp_name_customer,
        rp_tax=rp_tax,
        rp_name_seller=rp_name_seller,
        rp_name_contact=rp_name_contact,
        rp_branch=rp_branch,
        rp_address=rp_address,
        rp_phone=rp_phone,
        rp_email=rp_email,
        rp_confirm_date_price=rp_confirm_date_price,
        rp_date_delivery=rp_date_delivery,
        rp_ref1=rp_ref1,
        rp_ref2=rp_ref2,
        active=active,
        crt_date=dateTimeNow(),
        upd_date=dateTimeNow(),
        register_id=register_id
    )
    object.refresh_from_db()
    rp_id = object.rp_id
    # Create Item
    content_regist = register_main.objects.select_related(
        "ev").get(register_id=register_id)
    ev_vat = content_regist.ev.ev_vat
    # print(ev_vat)

    if ev_vat == 0:
        new_total = rpi_price_total
    else:
        new_total = float(rpi_price_total) - float(rpi_price_vat)
    register_payment_items.objects.create(
        rpi_code=rpi_code,
        rpi_name=rpi_name,
        rpi_quantity=rpi_quantity,
        rpi_unit=rpi_unit,
        rpi_price=rpi_price,
        rpi_price_discount=rpi_price_discount,
        rpi_price_total=new_total,
        rpi_price_vat=rpi_price_vat,
        rpi_price_result=rpi_price_result,
        rpi_pay=rpi_price_result,
        rp_id=rp_id,
        register_id=register_id
    )

    messages.success(request, "ทำรายการสำเร็จ !")
    # return redirect("/register/report")
    return redirect("/register/payment/history/" + str(register_id))


@login_required(login_url='/login')
def payment_form_update(request, register_id):
    title = defaultTitle
    try:
        content = customers.objects.select_related(
            "register", "location").get(register_id=register_id)
    except:
        content = None
        return redirect("/register/report")
    content_regist = register_main.objects.select_related(
        "seller", "ev").get(register_id=register_id)
    if content_regist.close_the_sale > 0:
        return redirect("/register/report")
    content_course = course_event.objects.select_related(
        "course").get(ev_id=content_regist.ev_id)
    total_pay = register_payment.objects.filter(
        register_id=register_id).count()
    last_data = register_payment_items.objects.select_related(
        "rp").filter(register_id=register_id).order_by("-rp_id").first()
    # print(total_pay)
    context1 = {'title': title,  'data': content,
                'content_regist': content_regist, 'content_course': content_course}
    context2 = {'title': title,  'data': last_data, 'content_regist': content_regist,
                'content_course': content_course}
    if total_pay < 1:
        return render(request, 'register/register_payment.html', context1)
    return render(request, 'register/register_payment_update.html', context2)


@login_required(login_url='/login')
def payment_history(request, register_id):
    title = defaultTitle
    try:
        main = register_main.objects.get(register_id=register_id)
    except:
        main = None
        return redirect("/")
    content = register_payment.objects.filter(
        register_id=register_id).order_by("-rp_id")
    if len(content) < 1:
        return redirect("/register/payment/" + str(register_id))
    obj = []
    for r in content:
        items = register_payment_items.objects.filter(rp_id=r.rp_id).first()
        res = {'main': r, 'items': items}
        obj.append(res)
    context = {'title': title,  'data': obj, 'main': main}
    return render(request, 'register/register_payment_history.html', context)


@login_required(login_url='/login')
def register_report(request):
    title = defaultTitle
    # month_current = date.today().month
    # year_current = date.today().year
    month_current = request.GET.get('qmonths', date.today().month)
    year_current = request.GET.get('qyear', date.today().year)

    content = register_main.objects.filter(
        crt_date__month=month_current, crt_date__year=year_current).exclude(register_number="-").order_by("-crt_date")
    obj = []
    for r in content:
        # print(r.register_id)
        # customer_list = customers.objects.select_related('register').filter(
        #     register_id=r.register_id, register__crt_date__month=1).first()
        customer_list = customers.objects.select_related('register').filter(
            register_id=r.register_id).first()
        total_payment = register_payment.objects.filter(
            register_id=r.register_id).count()
        course_list = course_event.objects.select_related(
            'course').filter(ev_id=r.ev_id).first()
        res = {'customer_list': customer_list,
               'course_list': course_list, 'total_payment': total_payment}
        obj.append(res)
    context = {'title': title,  'data': obj}
    return render(request, 'register/register_report.html', context)


@login_required(login_url='/login')
def update_close_the_sale(request):
    current_user = request.user
    user_id_authen = current_user.id
    register_id = request.POST['register_id']
    confirm_price = float(request.POST['confirm_price'])
    close_the_sale = int(request.POST['close_the_sale'])
    if close_the_sale == 1:
        customer_status = 1
    else:
        customer_status = 0
    try:
        content = register_main.objects.get(pk=register_id)
    except:
        content = None
        return redirect("/register/report")
    # เปรียบเทียบราคาเพื่อยืนยันการปิดการขาย
    check_payment = register_payment_items.objects.filter(
        rpi_price_result=confirm_price).order_by("-rpi_id").first()
    if check_payment:
        set_active = register_payment.objects.get(rp_id=check_payment.rp_id)
        set_active.active = 1
        set_active.upd_date = dateTimeNow()
        set_active.save()
    else:
        messages.error(request, "ไม่สามารถทำรายการได้ !")
        return redirect("/register/report")
    content.close_the_sale = close_the_sale
    content.customer_status = customer_status
    content.upd_date = dateTimeNow()
    content.user_update_id = user_id_authen
    content.save()
    messages.success(request, "ทำรายการสำเร็จ !")
    return redirect("/register/report")


@login_required(login_url='/login')
def register_cancle(request):
    register_id = request.POST['register_id']
    try:
        content = register_main.objects.get(pk=register_id)
    except:
        content = None
        return redirect("/register/report")
    content.delete()
    return redirect("/register/report")


def register_print(request, rp_id):
    title = defaultTitle
    try:
        content = register_payment.objects.get(pk=rp_id)
    except register_payment.DoesNotExist:
        content = None
        return render(request, '404.html')
    items = register_payment_items.objects.filter(rp_id=content.rp_id).first()
    content_regist = register_main.objects.select_related(
        "ev").get(register_id=content.register_id)
    if content_regist.ev.ev_vat == 1:
        rpi_price_default = float(
            items.rpi_price_total) + float(items.rpi_price_vat)
    else:
        rpi_price_default = items.rpi_price_total
    context = {'title': title,  'data': content,
               'items': items, "content_regist": content_regist, 'rpi_price_default': rpi_price_default}
    if content_regist.pay_type == 1:
        return render(request, 'print/register_print_bill.html', context)
    return render(request, 'print/register_print_sale_quotation.html', context)


def register_selller_report(request):
    title = defaultTitle
    list_user = User.objects.filter(is_staff=0, is_active=1)
    course_list = course.objects.filter(
        cancelled=1, active=1).order_by("-course_id")
    try:
        province_list = location_thai.objects.all().values(
            'province_code', 'province_name').annotate(total=Count('province_code'))
    except location_thai.DoesNotExist:
        province_list = None
    context = {'title': title,  'province_list': province_list,
               'list_user': list_user, 'course_list': course_list}
    return render(request, 'register/register_selller_report.html', context)


def register_excel_seller(request):
    title = defaultTitle

    year_current = int(request.GET.get('qyear', date.today().year))
    month_current = int(request.GET.get('qmonths', date.today().month))
    province_code = int(request.GET.get('qprovince', 0))
    customer_type = int(request.GET.get('qcustomer_type', 0))
    pay_type = int(request.GET.get('qpay_type', 0))
    close_the_sale = int(request.GET.get('qclose_the_sale', -1))
    course_id = int(request.GET.get('qcourse', 0))
    generation = request.GET.get('qgeneration', 0)
    seller = int(request.GET.get('qseller', 0))
    customer_name = request.GET.get('qcustomer_name', None)
    content = customers.objects.select_related(
        'register', 'location').filter(register__crt_date__year=year_current)

    month_param = "ทุกเดือน"
    if month_current != 0:
        content = content.filter(register__crt_date__month=month_current)
        month_param = month_fomat(month_current)

    province_name = "ทุกจังหวัด"
    if province_code != 0:
        content = content.filter(location__province_code=province_code)
        p = location_thai.objects.filter(
            province_code=province_code).values_list("province_name").first()
        province_name = p[0]
    customer_type_param = "ทุกประเภท"
    if customer_type != 0:
        content = content.filter(register__customer_type=customer_type)
        if customer_type == 1:
            customer_type_param = "บุคคล"
        else:
            customer_type_param = "บริษัท"
    pay_type_param = "ทุกประเภท"
    if pay_type != 0:
        content = content.filter(register__pay_type=pay_type)
        if pay_type == 1:
            pay_type_param = "เงินสด"
        else:
            pay_type_param = "เครดิต"
    close_the_sale_param = "ทุกประเภท"
    if close_the_sale != -1:
        content = content.filter(register__close_the_sale=close_the_sale)
        if close_the_sale == 0:
            close_the_sale_param = "กำลังขาย"
        elif close_the_sale == 1:
            close_the_sale_param = "ปิดการขาย - ขายสำเร็จ"
        elif close_the_sale == 2:
            close_the_sale_param = "ปิดการขาย - ขายไม่สำเร็จ"
    course_param = "ทุกหลักสูตร"
    if course_id != 0:
        content = content.filter(register__ev__course_id=course_id)
        c = course.objects.get(course_id=course_id)
        course_param = str(c.course_code) + " " + str(c.course_name)
    generation_param = "ทุกรุ่น"
    if generation:
        content = content.filter(register__ev__ev_generation=generation)
        generation_param = generation
    seller_param = "ทุกคน"
    if seller != 0:
        content = content.filter(register__seller_id=seller)
        u = User.objects.get(id=seller)
        seller_param = str(u.first_name) + " " + str(u.last_name)
        seller_param = "ทุกคน"
    if customer_name != None:
        content = content.filter(Q(customer_name__icontains=customer_name))
    obj = []
    for r in content:
        # print(r.register_id)

        payment_list = register_payment_items.objects.select_related('rp').filter(
            register_id=r.register_id).order_by("-rp__rp_id").first()
        course_list = course_event.objects.select_related(
            'course').filter(ev_id=r.register.ev_id).first()
        res = {'customer_list': r,
               'course_list': course_list, 'payment_list': payment_list}
        obj.append(res)

    param = {'total_data': len(content), 'year_current': year_current, 'month_param': month_param, 'province_name': province_name, 'customer_type_param': customer_type_param,
             'pay_type_param': pay_type_param, 'close_the_sale_param': close_the_sale_param, 'course_param': course_param, 'generation_param': generation_param, 'seller_param': seller_param}
    context = {'title': title, 'data': obj, 'param': param}
    return render(request, 'print/register_excel_seller.html', context)


def register_quotation_report(request):
    title = defaultTitle
    list_user = User.objects.filter(is_staff=0, is_active=1)
    course_list = course.objects.filter(
        cancelled=1, active=1).order_by("-course_id")
    try:
        province_list = location_thai.objects.all().values(
            'province_code', 'province_name').annotate(total=Count('province_code'))
    except location_thai.DoesNotExist:
        province_list = None
    context = {'title': title,  'province_list': province_list,
               'list_user': list_user, 'course_list': course_list}
    return render(request, 'register/register_quotation_report.html', context)


def register_excel_quotation(request):
    title = defaultTitle
    year_current = int(request.GET.get('qyear', date.today().year))
    month_current = int(request.GET.get('qmonths', date.today().month))
    close_the_sale = int(request.GET.get('qclose_the_sale', -1))
    course_id = int(request.GET.get('qcourse', 0))
    generation = request.GET.get('qgeneration', 0)
    seller = int(request.GET.get('qseller', 0))
    customer_name = request.GET.get('qcustomer_name', None)
    content = register_payment.objects.select_related(
        'register').filter(crt_date__year=year_current)

    month_param = "ทุกเดือน"
    if month_current != 0:
        content = content.filter(crt_date__month=month_current)
        month_param = month_fomat(month_current)

    close_the_sale_param = "ทุกประเภท"
    if close_the_sale != -1:
        content = content.filter(register__close_the_sale=close_the_sale)
        if close_the_sale == 0:
            close_the_sale_param = "กำลังขาย"
        elif close_the_sale == 1:
            close_the_sale_param = "ปิดการขาย - ขายสำเร็จ"
        elif close_the_sale == 2:
            close_the_sale_param = "ปิดการขาย - ขายไม่สำเร็จ"
    course_param = "ทุกหลักสูตร"
    if course_id != 0:
        content = content.filter(register__ev__course_id=course_id)
        c = course.objects.get(course_id=course_id)
        course_param = str(c.course_code) + " " + str(c.course_name)
    generation_param = "ทุกรุ่น"
    if generation:
        content = content.filter(register__ev__ev_generation=generation)
        generation_param = generation
    seller_param = "ทุกคน"
    if seller != 0:
        content = content.filter(register__seller_id=seller)
        u = User.objects.get(id=seller)
        seller_param = str(u.first_name) + " " + str(u.last_name)
    if customer_name != None:
        content = content.filter(Q(rp_name_customer__icontains=customer_name))
    obj = []
    for r in content:
        # print(r.register_id)
        customer_list = customers.objects.filter(
            register=r.register_id).select_related('location').first()
        payment_list = register_payment_items.objects.filter(
            rp_id=r.rp_id).order_by("-rp__rp_id").first()
        course_list = course_event.objects.select_related(
            'course').filter(ev_id=r.register.ev_id).first()
        res = {'main': r, 'customer_list': customer_list,
               'course_list': course_list, 'payment_list': payment_list}
        obj.append(res)

    param = {'total_data': len(content), 'year_current': year_current, 'month_param': month_param,   'close_the_sale_param': close_the_sale_param,
             'course_param': course_param, 'generation_param': generation_param, 'seller_param': seller_param}
    context = {'title': title, 'data': obj, 'param': param}
    return render(request, 'print/register_excel_quotation.html', context)
