"""Api for working with piastrix."""
from hashlib import sha256
from time import time

from requests import post


class PiastrixApi:
    """Creates and sends all requests to work with the piastrix api."""

    def __init__(
        self,
        secret_key,
        shop_id,
        payway,
        url='https://core.piastrix.com/',
    ):
        """
        Keep base settings for all requests.

        Parameters:
            secret_key: str
            shop_id: str
            payway: str
            url: str
        """
        self.secret_key = secret_key
        self.shop_id = shop_id
        self.payway = payway
        self.url = url

    def _post(self, endpoint, data):
        response = post(f'{self.url}{endpoint}', json=data)
        return response.json()

    def _shop_order_id(self):
        return 'ORDER_{0}'.format(int(time()))

    def _sign(self, required_fields, data):
        sorted_data = [data[key] for key in sorted(required_fields)]
        signed_data = ':'.join(sorted_data) + self.secret_key
        data['sign'] = sha256(signed_data.encode('utf-8')).hexdigest()

    def create_bill(self, data):
        """
        Create bill.

        Parameters:
            data: dict, dict with bill information

        Returns:
            return answer from api
        """
        required_fields = [
            'payer_currency', 'shop_amount', 'shop_currency',
            'shop_id', 'shop_order_id',
        ]
        data.update({
            'shop_id': self.shop_id,
            'shop_order_id': self._shop_order_id(),
            'shop_amount': data['amount'],
            'shop_currency': data['currency'],
            'payer_currency': data['currency'],
        })
        self._sign(required_fields, data)
        answer = self._post('bill/create', data)
        answer.update({'type': 'bill'})
        return answer

    def create_invoice(self, data):
        """
        Create invoice.

        Parameters:
            data: dict, dict with invoice information

        Returns:
            return answer from api
        """
        required_fields = [
            'amount', 'currency', 'shop_id',
            'payway', 'shop_order_id',
        ]
        data.update({
            'shop_id': self.shop_id,
            'shop_order_id': self._shop_order_id(),
            'payway': self.payway,
        })
        self._sign(required_fields, data)
        answer = self._post('invoice/create', data)
        answer.update({'type': 'invoice'})
        return answer

    def create_pay_form(self, data):
        """
        Create invoice form.

        Parameters:
            data: dict, dict with invoice information

        Returns:
            return complete data for the invoice form
        """
        required_fields = ['amount', 'currency', 'shop_id', 'shop_order_id']
        data.update({
            'type': 'pay',
            'shop_id': self.shop_id,
            'shop_order_id': self._shop_order_id(),
        })
        self._sign(required_fields, data)
        return data
