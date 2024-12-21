from flask import Flask, request, jsonify
import stripe
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable Cross-Origin Resource Sharing for frontend integration

# Set the secret key 
stripe.api_key = 'sk_test_your_secret_key'  # Replace with our actual secret key

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return "Welcome to the RoundSpheres Payment Gateway!"

def validate_payment_intent_data(data):
    """Validate input data for creating a PaymentIntent."""
    if 'amount' not in data or not isinstance(data['amount'], int):
        raise ValueError("Amount must be provided as an integer.")
    if 'currency' in data and not isinstance(data['currency'], str):
        raise ValueError("Currency must be a string.")

@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.json
        validate_payment_intent_data(data)
        
        amount = data['amount']
        currency = data.get('currency', 'usd')
        
        logging.info(f"Creating PaymentIntent for {amount} {currency}.")
        
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
        )
        
        return jsonify({'clientSecret': intent['client_secret']})
    except ValueError as ve:
        return jsonify(error=str(ve)), 400
    except stripe.error.StripeError as se:
        logging.error(f"Stripe error: {se}")
        return jsonify(error="Payment processing error. Please try again."), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify(error="An unexpected error occurred."), 500

def validate_subscription_data(data):
    """Validate input data for creating a subscription."""
    if 'email' not in data or not isinstance(data['email'], str):
        raise ValueError("Valid email must be provided.")
    if 'price_id' not in data or not isinstance(data['price_id'], str):
        raise ValueError("Price ID must be provided as a string.")

@app.route('/create-subscription', methods=['POST'])
def create_subscription():
    try:
        data = request.json
        validate_subscription_data(data)
        
        customer_email = data['email']
        price_id = data['price_id']
        
        logging.info(f"Creating subscription for customer {customer_email} with price ID {price_id}.")
        
        # Check if customer already exists
        existing_customers = stripe.Customer.list(email=customer_email).data
        if existing_customers:
            customer = existing_customers[0]
        else:
            customer = stripe.Customer.create(email=customer_email)
        
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[
                {"price": price_id},
            ],
            expand=["latest_invoice.payment_intent"],
        )
        
        return jsonify(subscription)
    except ValueError as ve:
        return jsonify(error=str(ve)), 400
    except stripe.error.StripeError as se:
        logging.error(f"Stripe error: {se}")
        return jsonify(error="Subscription processing error. Try again please."), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify(error="An unexpected error occurred."), 500

if __name__ == '__main__':
    app.run(debug=True)
