from io import BytesIO
import weasyprint
from celery import shared_task
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from orders.models import Order

@shared_task
def payment_completed(order_id):
    """
    Задание по отправке уведомления по электронной почте
    при успешной оплате заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = f'X-Files Shop. Номер заказа {order.id}'
    message = 'Во вложении — счёт на оплату вашей недавней покупки.'
    email = EmailMessage(
        subject,
        message,
        'admin@x-files-shop.com',
        [order.email]
    )
    html = render_to_string(
        'orders/order/pdf.html',
        {'order': order}
    )
    out = BytesIO()
    stylesheets = [
        weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')
    ]
    weasyprint.HTML(string=html).write_pdf(
        out, stylesheets=stylesheets
    )
    email.attach(
        f'order_{order.id}.pdf',
        out.getvalue(),
        'application/pdf'
    )
    email.send()
