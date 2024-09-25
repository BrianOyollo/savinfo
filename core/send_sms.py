import africastalking
import os
from dotenv import load_dotenv

load_dotenv()

africastalking.initialize(
    username='sandbox',
    api_key= os.getenv('SMS_API_KEY')
)
sms = africastalking.SMS

sender = os.getenv('SENDER_SHORTCODE')

def format_phone_number(phone_number):
    """_summary_
    Ensures the phone number is in the correct format starting with +254.

    Args:
        phone_number: The customer's phone number.
    
    Returns:
        str: The formatted phone number.
    """

    if phone_number.startswith("+254"):
        return phone_number

    elif phone_number.startswith("0"):
        return f"+254{phone_number[1:]}"
    

def send_order_confirmation_sms(customer, order, quantity):
    """
    Sends an order confirmation SMS to the customer.

    Args:
        customer: Customer instance containing phone_number and name.
        order: Order name or description.
        quantity: Number of items ordered.
    """
    customer_phone_number = format_phone_number(customer.phone_number)
    message = f"Hello {customer}, your order of {order}*{quantity} has been created successfully"

    try:
        response = sms.send(message,[customer_phone_number], sender)
        return response
    except Exception as e:
        print (f'Order confirmation message not sent: {e}')
        return None


def send_order_update_sms(customer, order, quantity):
    """
    Sends an SMS to the customer when their order is updated

    Args:
        customer: Customer instance containing phone_number and name.
        order: Updated order name or description.
        quantity: Updated number of items ordered.
    """
    customer_phone_number = format_phone_number(customer.phone_number)
    message = f"Hello {customer}, you have updated your order to {order}*{quantity}"

    try:
        response = sms.send(message,[customer_phone_number], sender)
        return response
    except Exception as e:
        print (f'Order update message not sent: {e}')
        return 