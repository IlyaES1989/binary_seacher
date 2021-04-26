import os

from pathlib import Path
from http.server import BaseHTTPRequestHandler
from urllib import parse

from searcher import find_recommendation, file_loader


class GetHandler(BaseHTTPRequestHandler):
    BASE_DIR = Path(__file__).resolve().parent
    DB_NAME = 'sorted_recommends.csv'

    PATH_TO_SEARCH = os.path.join(BASE_DIR, DB_NAME)
    file = file_loader(PATH_TO_SEARCH)

    def do_GET(self):
        parsed_path = parse.urlparse(self.path)
        query = parse.parse_qs(parsed_path.query)
        sku = query.get('sku')
        rank = query.get('rank')

        if rank:
            rank = rank[0]
        if sku:
            sku = sku[0]

        try:
            response = find_recommendation(self.file, sku=sku, rank=rank)
        except ValueError:
            response = 'No results have been found for this search.'
        except TypeError:
            response = 'To form a search query, specify the necessary parameter "sku" and optional "rank"\n' \
                       'For example: ?sku=Ia5f7aPUpM&rank=0.8'

        message_parts = ['CLIENT VALUES:',
                         'client_address = %s (%s)' % (self.client_address, self.address_string()),
                         'command = %s' % self.command,
                         'request_version = %s' % self.request_version,
                         'path = %s' % self.path,
                         'real path = %s' % parsed_path.path,
                         'query = %s' % query,
                         '\n',
                         'response:',
                         '%s' % response,
                         ]

        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))


if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('127.0.0.1', 8000), GetHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()

