"""
Store class.

Needed to send the result of the API to the user form on the web page.
"""


class Store:
    """Class for storing API results for sessions."""

    def __init__(self):
        """Init store."""
        self._store = {}

    def push(self, sessionid, form_data):
        """
        Add result for sessionid.

        Parameters:
            sessionid: str, format - uuid4
            form_data: dict, API result
        """
        if sessionid in self._store.keys():
            self._store[sessionid].append(form_data)
        else:
            self._store[sessionid] = [form_data]

    def pop(self, sessionid):
        """
        Get latest result for sessionid.

        Parameters:
            sessionid: str, format - uuid4

        Returns:
            return dict, API result
        """
        if sessionid in self._store.keys() and len(self._store[sessionid]) > 0:
            return self._store[sessionid].pop()


store = Store()
