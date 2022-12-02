from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from ..common import defaultTitle
from ..models import course, course_event
from ..functions import dateTimeNow, dmytoymd


@login_required(login_url='/login')
def course_list(request):
    title = defaultTitle
    result = course.objects.filter(cancelled=1).order_by("-course_id")
    context = {'title': title,  'data': result}
    return render(request, 'course/course.html', context)


@login_required(login_url='/login')
def course_create(request):
    course_code = request.POST['course_code']
    course_name = request.POST['course_name']
    active = request.POST['active']
    content = course(
        course_code=course_code,
        course_name=course_name,
        active=active,
        crt_date=dateTimeNow(),
        upd_date=dateTimeNow())
    content.save()
    messages.success(request, "ทำรายการสำเร็จ !")
    return redirect("/course")


@login_required(login_url='/login')
def course_update(request):
    course_id = request.POST['course_id']
    course_code = request.POST['course_code']
    course_name = request.POST['course_name']
    active = request.POST['active']
    content = course.objects.get(pk=course_id)
    content.course_code = course_code
    content.course_name = course_name
    content.active = active
    content.upd_date = dateTimeNow()
    content.save()
    messages.success(request, "ทำรายการสำเร็จ !")
    return redirect("/course")


@login_required(login_url='/login')
def course_delete(request):
    course_id = request.POST['course_id']
    content = course.objects.get(pk=course_id)
    content.cancelled = 0
    content.save()
    messages.success(request, "ทำรายการสำเร็จ !")
    return redirect("/course")


@login_required(login_url='/login')
def course_event_list(request):
    title = defaultTitle
    month_current = request.GET.get('qmonths', date.today().month)
    year_current = request.GET.get('qyear', date.today().year)
    course_list = course.objects.filter(
        cancelled=1, active=1).order_by("-course_id")
    result = course_event.objects.select_related("course").filter(
        cancelled=1, ev_date_start__month=month_current, ev_date_start__year=year_current).order_by("-ev_id")
    context = {'title': title,  'data': result, 'course_list': course_list}
    return render(request, 'course/course_event_list.html', context)


@login_required(login_url='/login')
def course_event_create(request):
    course_id = request.POST['course_id']
    ev_date_start = dmytoymd(request.POST['ev_date_start'])
    ev_date_end = dmytoymd(request.POST['ev_date_end'])
    ev_generation = request.POST['ev_generation']
    ev_remark = request.POST['ev_remark']
    ev_price = request.POST['ev_price']
    ev_vat = request.POST['ev_vat']
    active = request.POST['active']
    content = course_event(
        ev_date_start=ev_date_start,
        ev_date_end=ev_date_end,
        ev_generation=ev_generation,
        ev_remark=ev_remark,
        ev_price=ev_price,
        ev_vat=ev_vat,
        active=active,
        crt_date=dateTimeNow(),
        upd_date=dateTimeNow(),
        course_id=course_id)
    content.save()
    messages.success(request, "ทำรายการสำเร็จ !")
    return redirect("/course/event")


@login_required(login_url='/login')
def course_event_update(request):
    ev_id = request.POST['ev_id']
    course_id = request.POST['course_id']
    ev_date_start = dmytoymd(request.POST['ev_date_start'])
    ev_date_end = dmytoymd(request.POST['ev_date_end'])
    ev_generation = request.POST['ev_generation']
    ev_remark = request.POST['ev_remark']
    ev_price = request.POST['ev_price']
    ev_vat = request.POST['ev_vat']
    active = request.POST['active']
    content = course_event.objects.get(pk=ev_id)
    content.ev_date_start = ev_date_start
    content.ev_date_end = ev_date_end
    content.ev_generation = ev_generation
    content.ev_remark = ev_remark
    content.ev_price = ev_price
    content.ev_vat = ev_vat
    content.active = active
    content.upd_date = dateTimeNow()
    content.course_id = course_id
    content.save()
    messages.success(request, "ทำรายการสำเร็จ !")
    return redirect("/course/event")


@login_required(login_url='/login')
def course_event_delete(request):
    ev_id = request.POST['ev_id']
    content = course_event.objects.get(pk=ev_id)
    content.cancelled = 0
    content.save()
    messages.success(request, "ทำรายการสำเร็จ !")
    return redirect("/course/event")


@login_required(login_url='/login')
def calendar_event(request):
    title = defaultTitle
    context = {'title': title}
    return render(request, 'course/calendar_event.html', context)


def calendar_event_api(request):
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    _date = date.today()
    if start is not None and end is not None:
        # 2022-10-31T00:00:00+07:00 to  2022-10-31
        sobj = str(start).split("T")[0]
        # 2022-10-31T00:00:00+07:00 to  2022-10-31
        eobj = str(end).split("T")[0]
    else:
        sobj = _date + timedelta(days=-30)
        eobj = _date + timedelta(days=30)
    content = course_event.objects.select_related(
        "course").filter(active=1, cancelled=1, ev_date_start__gte=sobj, ev_date_end__lte=eobj)
    # print(len(content))

    obj = []
    for r in content:
        res = {'title': str(r.course.course_name) + " (รุ่นที่" + str(r.ev_generation)+")",
               'start': r.ev_date_start, 'end': r.ev_date_end}
        obj.append(res)
    return JsonResponse(obj, safe=False)
