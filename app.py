from flask import Flask, request, jsonify
from goodreads_quotes import Goodreads

app = Flask(__name__)
base_url = 'https://goodreads-quotes-api.herokuapp.com'

# Main Index
@app.route('/', methods=['GET'])
def get_home():
    return jsonify({
            'author': 'Sandip Bhagat',
            'author_url': 'http://sandipbgt.github.io',
            'base_url': base_url,
            'project_name': 'goodreads-quotes-api',
            'project_url': 'https://github.com/sandipbgt/goodreads-quotes-api',
            'api': base_url + '/api'
        })

# API Index
@app.route('/api', methods=['GET'])
def get_api_home():
    return jsonify({
            'daily': base_url + '/api/quotes/daily',
            'popular': base_url + '/api/quotes/popular',
        })

# Daily Quotes
@app.route('/api/quotes/daily', methods=['GET'])
def get_daily_quote():
    quote = Goodreads.get_daily_quote()
    return jsonify(quote)

# Popular Quotes
@app.route('/api/quotes/popular', methods=['GET'])
def get_popular_quotes():
    quotes = Goodreads.get_popular_quotes()
    return jsonify({ 'quotes': quotes })

# Send daily quote via Twilio API
@app.route('/api/quotes/daily/send', methods=['POST'])
def send_daily_quote():
    data = request.get_json(force=True)

    account_sid = data.get('account_sid', None)
    if account_sid is None:
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'Twilio account sid required'}), 400

    auth_token = data.get('auth_token', None)
    if auth_token is None:
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'Twilio auth token required'}), 400

    from_phone = data.get('from_phone', None)
    if from_phone is None:
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'Twilio phone number required'}), 400

    to_phone = data.get('to_phone', None)
    if to_phone is None:
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'To phone number required'}), 400

    quote = Goodreads.get_daily_quote()
    message = "%s by - %s" % (quote['quote'], quote['author'])
    twilio_response = send_message(account_sid, auth_token, from_phone, to_phone, message)
    if not twilio_response:
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'Twilio API details required'}), 400

    return jsonify({'message': twilio_response})

# Utility function to send message via Twilio API
def send_message(account_sid, auth_token, from_phone, to_phone, message):
    from twilio import TwilioRestException
    from twilio.rest import TwilioRestClient

    if not account_sid or not auth_token or not to_phone or not from_phone:
        return False

    try:
        client = TwilioRestClient(account_sid, auth_token)
        message = client.messages.create(body=message, to=to_phone, from_=from_phone)
        return {
            'message_id': message.sid
        }
    except TwilioRestException as e:
        return {
                'error_message': str(e.msg)
            }, 400

# Fire our Flask app
if __name__ == '__main__':
    app.run()