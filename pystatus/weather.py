# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
from time import time
import re

class Py3status:
    """
    Get Rhodes weather
    """
    def _get_temp(self):
        import urllib2
        response = urllib2.urlopen('http://www.ru.ac.za/static/weather/ARCHIVE/CURRENTDATA/public-5m.dat')
        temp = (response.read().split(",")[5]).split(".")[0]+"°C"
        return temp

    def _window_title(self, json, i3status_config):
        """
        This gets executed.
        """
        response = {
                'full_text': '',
                'name': 'window_title',
                'cached_until': 600
                }

        response['full_text'] = self._get_temp().strip('"')[:70]
        return (0, response)
