"""
An MPD display client for py3status. Code largely copied from mpd.py of qtile. But then, I wrote most of that, too.
"""

import mpd, os, re
from time import time

HOST = "localhost"
PORT = 6600
PLAY_FORMAT = "%a - %t %s"
STOP_FORMAT = ""

class Py3status:
    def __init__(self):
        self.conn = mpd.MPDClient()
        host = os.environ.get('MPD_HOST', HOST)
        port = os.environ.get('MPD_PORT', PORT)
        self.conn.connect(host, port)
        self.host, self.port = host, port
        
    def mpdstat(self, json, config):
        self._update()
        if self.status['state'] != 'stop':
            outstr = self._do_format(PLAY_FORMAT)
        else:
            outstr = self._do_format(STOP_FORMAT)
        r = {'name': 'MPD', 'instance': "{}:{}".format(self.host, self.port), 'full_text': outstr, 'cached_until': time()}
        return 1,r

    def _to_minutes_seconds(self, stime):
        """Takes an integer time in seconds, transforms it into
        (HH:)?MM:SS. HH portion is only visible if total time is greater
        than an hour."""
        if type(stime) != int:
            stime = int(stime)
        mm = stime // 60
        ss = stime % 60
        if mm >= 60:
            hh = mm // 60
            mm = mm % 60
            rv = "{}:{:02}:{:02}".format(hh, mm, ss)
        else:
            rv = "{}:{:02}".format(mm, ss)
        return rv

    def _get_artist(self):
        return self.song['artist']

    def _get_album(self):
        return self.song['album']

    def _get_elapsed(self):
        elapsed = self.status['time'].split(':')[0]
        return self._to_minutes_seconds(elapsed)

    def _get_file(self):
        return self.song['file']

    def _get_length(self):
        return self._to_minutes_seconds(self.song['time'])

    def _get_number(self):
        return str(int(self.status['song'])+1)

    def _get_playlistlength(self):
        return self.status['playlistlength']

    def _get_status(self):
        n = self.status['state']
        if n == "play":
            return ""
        elif n == "pause":
            return "[Paused]"
        elif n == "stop":
            return ""

    def _get_longstatus(self):
        n = self.status['state']
        if n == "play":
            return "Playing"
        elif n == "pause":
            return "Paused"
        elif n == "stop":
            return "Stopped"

    def _get_title(self):
        return self.song['title']

    def _get_track(self):
        # This occasionally has leading zeros we don't want.
        return str(int(self.song['track'].split('/')[0])) 

    def _get_volume(self):
        return self.status['volume']

    def _get_single(self):
        if self.status['single'] == '1':
            return '1'
        else:
            return '_'

    def _get_repeat(self):
        if self.status['repeat'] == '1':
            return 'R'
        else:
            return '_'

    def _get_shuffle(self):
        if self.status['random'] == '1':
            return 'S'
        else:
            return '_'

    formats = {'a': _get_artist, 'A': _get_album, 'e': _get_elapsed, 
               'f': _get_file, 'l': _get_length, 'n': _get_number, 
               'p': _get_playlistlength, 's': _get_status, 'S': _get_longstatus, 
               't': _get_title, 'T': _get_track, 'v': _get_volume, '1': _get_single,
               'r': _get_repeat, 'h': _get_shuffle, '%': lambda x: '%', }

    def _match_check(self, m):
        try:
            return self.formats[m.group(1)](self)
        except KeyError: # This fires both if a nonexistent escape is given, and if the given escape is not meaningful in the current state.
            return "(nil)"

    def _do_format(self, string):
        return re.sub("%(.)", self._match_check, string)

    def _update(self):
        try:
            self.status = self.conn.status()
            self.song = self.conn.currentsong()
        except mpd.ConnectionError:
            self.conn.connect(self.host, self.port)
