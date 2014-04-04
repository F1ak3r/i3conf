# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
from time import time
import re

class Py3status:
    """
    Display active window title.
    """
    def _get_active_window_title(self):
        """
        This gets the window title.
        """
        root = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE)

        for line in root.stdout:
            m = re.search('^_NET_ACTIVE_WINDOW.* ([\w]+)$', line)
            if m != None:
                id_ = m.group(1)
                id_w = Popen(['xprop', '-id', id_, 'WM_NAME'], stdout=PIPE)
                break

        if id_w != None:
            for line in id_w.stdout:
                match = re.match("WM_NAME\(\w+\) = (?P<name>.+)$", line)
                if match != None:
                    return match.group('name')

        return ''

    def window_title(self, json, i3status_config):
        """
        This gets executed.
        """
        response = {
                'full_text': '',
                'name': 'window_title',
                'cached_until': 0
                }

        response['full_text'] = self._get_active_window_title().strip('"')[:70]
        return (0, response)
