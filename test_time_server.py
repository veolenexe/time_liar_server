import unittest
import time_server
import os
import datetime


class TestTimeServer(unittest.TestCase):

    def test_get_offset_non_exist_file_correct(self):
        result = time_server.get_offset('wrong_file')
        assert result == 0

    def test_get_offset_exist_file_correct1(self):
        with open('test_configuration.txt', 'w') as f:
            f.write('100')
        try:
            result = time_server.get_offset('test_configuration.txt')
        finally:
            os.remove('test_configuration.txt')
        assert result == 100

    def test_get_offset_exist_file_correct2(self):
        with open('test_configuration.txt', 'w') as f:
            f.write('one hundred')
        try:
            result = time_server.get_offset('test_configuration.txt')
        finally:
            os.remove('test_configuration.txt')
        assert result == 0

    def test_get_wrong_time_correct1(self):
        with open('test_configuration.txt', 'w') as f:
            f.write('100')
        try:
            server = time_server.TimeServer('test_configuration.txt')
        finally:
            os.remove('test_configuration.txt')
        result = server.get_wrong_time()
        correct_time = (datetime.datetime.now() - datetime.timedelta(
            seconds=100)).strftime('%H:%M:%S')
        assert result == correct_time

    def test_get_wrong_time_correct2(self):
        server = time_server.TimeServer('wrong_file')
        result = server.get_wrong_time()
        correct_time = datetime.datetime.now().strftime('%H:%M:%S')
        assert result == correct_time
