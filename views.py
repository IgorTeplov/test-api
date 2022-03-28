import logging
import uuid

from flask import (Blueprint, redirect, render_template,
                   request, session, url_for)

from lib.piastrix import PiastrixApi
from lib.store import store

from settings import payway, secret_key, shop_id

logger = logging.getLogger('apiLogger')
views = Blueprint('views', __name__, '')


@views.route('/')
def index():
    """
    Displays all forms for the user, taking into account the responses from the api.

    Returns:
        return index.html with response from the api
    """
    data = None
    if 'sessionid' in session.keys():
        data = store.pop(session['sessionid'])
        if data is None:
            data = {'type': None}
    else:
        data = {'type': None}

    return render_template('index.html', data=data)


@views.route('/api/', methods=['POST'])
def api():
    """
    Create api requests.

    Returns:
        return redirects to index and sets the
               session ID with the response from api
    """
    post_form = dict(request.form)
    if {'amount', 'currency', 'description'}.issubset(set(post_form.keys())):

        post_form['amount'] = str(round(float(post_form['amount']), 2))

        if 'sessionid' not in session.keys():
            session['sessionid'] = str(uuid.uuid4())

        pi_api = PiastrixApi(secret_key, shop_id, payway)
        if post_form['currency'] == '978':
            data = pi_api.create_pay_form(post_form)
        elif post_form['currency'] == '840':
            data = pi_api.create_bill(post_form)
        else:
            data = pi_api.create_invoice(post_form)

        store.push(session['sessionid'], data)
    logger.info('Request to PiastrixApi: {0}'.format(
        '{' + ','.join(
            [f'\n\t{key}: {value}' for key, value in post_form.items() if key not in ('type', 'sign')],
        ) + '\n}',
    ))
    logger.info('Response from piastriApi: {0}'.format(
        '{' + ','.join(
            [f'\n\t{key}: {value}' for key, value in data.items() if key not in ('type', 'sign')],
        ) + '\n}',
    ))
    return redirect(url_for('.index'))
