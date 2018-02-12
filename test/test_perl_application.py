import re
import time
import unittest
import unit

class TestUnitPerlApplication(unit.TestUnitApplicationPerl):

    def setUpClass():
        unit.TestUnit().check_modules('perl')

    def test_perl_application(self):
        self.load('variables')

        body = 'Test body string.'

        resp = self.post(headers={
            'Host': 'localhost',
            'Content-Type': 'text/html',
            'Custom-Header': 'blah'
        }, body=body)

        self.assertEqual(resp['status'], 200, 'status')
        headers = resp['headers']
        self.assertRegex(headers.pop('Server'), r'unit/[\d\.]+',
            'server header')
        self.assertLess(abs(time.mktime(time.gmtime()) -
            time.mktime(time.strptime(headers.pop('Date'),
            '%a, %d %b %Y %H:%M:%S GMT'))), 5, 'date header')
        self.assertDictEqual(headers, {
            'Content-Length': str(len(body)),
            'Content-Type': 'text/html',
            'Request-Method': 'POST',
            'Request-Uri': '/',
            'Http-Host': 'localhost',
            'Server-Protocol': 'HTTP/1.1',
            'Custom-Header': 'blah'
        }, 'headers')
        self.assertEqual(resp['body'], body, 'body')

    def test_perl_application_query_string(self):
        self.load('query_string')

        resp = self.get(url='/?var1=val1&var2=val2')

        self.assertEqual(resp['headers']['Query-String'], 'var1=val1&var2=val2',
            'Query-String header')

    @unittest.expectedFailure
    def test_perl_application_server_port(self):
        self.load('server_port')

        self.assertEqual(self.get()['headers']['Server-Port'], '7080',
            'Server-Port header')

    def test_perl_application_input_read_empty(self):
        self.load('input_read_empty')

        self.assertEqual(self.get()['body'], '', 'read empty')

    @unittest.expectedFailure
    def test_perl_application_input_read_offset(self):
        self.load('input_read_offset')

        self.assertEqual(self.post(body='0123456789')['body'], '4567',
            'read offset')

    def test_perl_application_input_copy(self):
        self.load('input_copy')

        body = '0123456789'
        self.assertEqual(self.post(body=body)['body'], body, 'input copy')

    def test_perl_application_errors_print(self):
        self.load('errors_print')

        self.assertEqual(self.get()['body'], '1', 'errors result')

        with open(self.testdir + '/unit.log', 'r') as f:
            m = re.search('Error in application', f.read())

        self.assertIsNotNone(m, 'errors log')

    def test_perl_application_header_pairs(self):
        self.load('header_pairs')

        self.assertEqual(self.get()['headers']['blah'], 'blah', 'header pairs')

    def test_perl_application_body_empty(self):
        self.load('body_empty')

        self.assertEqual(self.get()['body'], '0\r\n\r\n', 'body empty')

    def test_perl_application_body_array(self):
        self.load('body_array')

        self.assertEqual(self.get()['body'], '0123456789', 'body array')

    def test_perl_application_body_large(self):
        self.load('variables')

        body = '0123456789' * 1000

        resp = self.get(body=body)['body']

        self.assertEqual(resp, body, 'body large')

    def test_perl_application_body_io_empty(self):
        self.load('body_io_empty')

        self.assertEqual(self.get()['status'], 200, 'body io empty')

    def test_perl_application_body_io_file(self):
        self.load('body_io_file')

        self.assertEqual(self.get()['body'], 'body\n', 'body io file')

if __name__ == '__main__':
    unittest.main()
