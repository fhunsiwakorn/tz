
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import course, register, master_data, general

urlpatterns = [
    path('', register.register_home),
    path('register/', register.register_home),
    path('register/create/', register.register_create, name="CreateRegister"),
    path('register/reset', register.register_reset),
    path('register/customer/create/',
         register.customer_create, name="CreateCustomer"),
    path('register/payment/<str:register_id>', register.payment),
    path('register/payment/update/<str:register_id>',
         register.payment_form_update),
    path('register/payment/create/', register.payment_create, name="CreatePayment"),
    path('register/payment/history/<str:register_id>', register.payment_history),
    path('register/report', register.register_report),
    path('register/update/close_the_sale',
         register.update_close_the_sale, name="UpdateCloseTheSale"),
    path('register/detail/<str:register_id>', register.register_detail),
    path('register/cancle',
         register.register_cancle, name="CancleRegister"),
    path('register/export/seller', register.register_selller_report),
    path('register/export/quotation', register.register_quotation_report),

    # Course
    path('course/', course.course_list),
    path('create_course/', course.course_create, name="CreateCourse"),
    path('create_update/', course.course_update, name="UpdateCourse"),
    path('course_delete/', course.course_delete, name="DeleteCourse"),
    path('course/event', course.course_event_list),
    path('course/event/create', course.course_event_create,
         name="CreateCourseEvent"),
    path('course/event/update', course.course_event_update,
         name="UpdateCourseEvent"),
    path('course/event/delete/', course.course_event_delete,
         name="DeleteCourseEvent"),
    path('calendar_event/', course.calendar_event),
    path('calendar_event_api/', course.calendar_event_api),
    # Master Data
    path('locationthai/', master_data.get_locationThai),

    # General
    path('login/', general.login),
    path('logout/', general.logout),
    path('authen_check/', general.login_check, name="LoginCheck"),
    # print / export
    path('register/print/<slug:rp_id>', register.register_print),
    path('register/excel/seller', register.register_excel_seller),
    path('register/excel/quotation', register.register_excel_quotation),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
