"""Util to process access token to Twitter api."""

import re

from retrying import retry

from stweet.exceptions import RefreshTokenException
from stweet.http_request import RequestDetails, RequestRunner

_retries = 5
_timeout = 20
_url = 'https://twitter.com'


class TokenRequest:
    """Class to manage Twitter token api."""

    @staticmethod
    def _request_for_response_body():
        """Method from Twint."""
        token_request_details = RequestDetails(_url, dict(), dict(), _timeout)
        token_response = RequestRunner().run_request(token_request_details)
        if token_response.is_success():
            return token_response.text
        else:
            raise RefreshTokenException('Error during request for token')

    @staticmethod
    @retry(stop_max_attempt_number=20)
    # sometimes an error occurs on CI tests
    def refresh() -> str:
        """Method to get refreshed token. In case of error raise RefreshTokenException."""
        print('Retrieving guest token')
        token_html = TokenRequest._request_for_response_body()
        match = re.search(r'\("gt=(\d+);', token_html)
        if match:
            return str(match.group(1))
        else:
            print('Could not find the Guest token in HTML')
            raise RefreshTokenException('Could not find the Guest token in HTML')