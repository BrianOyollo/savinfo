import pytest
from ..send_sms import format_phone_number, send_order_confirmation_sms

def test_format_phone_number():
    phone_number1 = '0712345678'
    phone_number2 = '+254700000001'

    assert format_phone_number(phone_number1) == '+254712345678'
    assert format_phone_number(phone_number2) == '+254700000001'


@pytest.mark.django_db
def test_send_order_confirmation_sms(create_user):
    customer = create_user.customer
    phone_number= format_phone_number('0712345678')
    customer.phone_number = phone_number
    customer.save()

    # order
    order = '2014 Audi R8 V10 Coupe'
    quantity = 2

    response = send_order_confirmation_sms(customer, order, quantity)

    assert response['SMSMessageData']['Recipients'][0]['number'] == phone_number
    assert response['SMSMessageData']['Recipients'][0]['statusCode'] == 101
    assert response['SMSMessageData']['Recipients'][0]['messageId'] != None