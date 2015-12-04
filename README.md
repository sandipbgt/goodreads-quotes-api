# goodread-quotes-api

REST api to view and send daily quote as SMS from [goodreads.com](http://goodreads.com) using [goodreads_quotes](https://pypi.python.org/pypi/goodreads_quotes/) lilbrary.

The api is live at: [http://goodreads-quotes-api.herokuapp.com](http://goodreads-quotes-api.herokuapp.com)

## Installation
```sh
$ git clone https://github.com/sandipbgt/goodreads-quotes-api.git
$ cd goodreads-quotes-api
$ pip install -r requirements.txt
$ gunicorn app:app
```

# API Usage

**GET:** `http://goodreads-quotes-api.herokuapp.com/api/quote/daily`

**Description:** Returns quote of the day

**GET:** `http://goodreads-quotes-api.herokuapp.com/api/quote/popular`

**Description:** Returns popular quotes of the day

**POST:** `http://goodreads-quotes-api.herokuapp.com/api/quote/daily/send`

**Description:** Send quote of the day as SMS using Twilio API

**Params:**
* `account_sid`: Twilio API account sid
* `auth_token`: Twilio API auth token
* `to_phone`: Phone number to send sms
* `from_phone`: Your Twilio phone number

# Contributing
Feel free to submit a pull request or an issue!