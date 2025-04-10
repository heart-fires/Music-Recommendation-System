from alipay import AliPay
from django.conf import settings

def create_alipay_order(out_trade_no, total_amount, subject):
    alipay = AliPay(
        appid=settings.ALIPAY_APPID,
        app_notify_url=settings.ALIPAY_NOTIFY_URL,
        app_private_key_string=settings.ALIPAY_PRIVATE_KEY,
        alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY,
        sign_type="RSA2",
        debug=False
    )
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=out_trade_no,
        total_amount=total_amount,
        subject=subject,
        return_url=settings.ALIPAY_RETURN_URL,
        notify_url=settings.ALIPAY_NOTIFY_URL
    )
    pay_url = 'https://openapi.alipay.com/gateway.do?' + order_string
    return pay_url