#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Send albums to `beet import`.
"""

import os
import subprocess
from picard import log
from picard.album import Album
from picard.ui.itemviews import BaseAction, register_album_action

PLUGIN_NAME = u'Import in Beets'
PLUGIN_AUTHOR = u'pacoqueen'
PLUGIN_DESCRIPTION = u'''Send album to `beet import` in a terminal window.'''
PLUGIN_VERSION = '0.7'
PLUGIN_API_VERSIONS = ['0.15']
PLUGIN_LICENSE = "GPL-3.0"
PLUGIN_LICENSE_URL = "https://www.gnu.org/licenses/gpl.txt"


class BeetImport(BaseAction):
    """
    Class that encapsulates the callback method that goes throught all
    selected albums and sends to Beet if they are "gold".
    """
    NAME = PLUGIN_NAME

    def callback(self, objs):
        """
        For every album selected? send it to `beet import` in a terminal and
        removes from album list.
        """
        for album in objs:
            if (isinstance(album, Album)
                    and album.is_complete()
                    and album.get_num_unmatched_files() == 0
                    and album.get_num_matched_tracks() == len(
                        list(album.iterfiles()))
                    and album.get_num_unsaved_files() == 0
                    and album.loaded):
                if self.send2beets(album):
                    self.tagger.remove_album(album)

    def send2beets(self, album):
        """
        Locates path for album and send to `beet import` command.
        """
        res = True
        log.info('beet import "{}"'.format(album))
        album_filenames = album.tagger.get_files_from_objects([album])
        albumpaths = set()
        for track in album.tracks:
            trackno = track.metadata['tracknumber']
            discno = track.metadata['discnumber']
            track_file = None
            for album_file in album_filenames:
                if (str(album_file.tracknumber) == trackno
                        and str(album_file.discnumber) == discno):
                    track_file = album_file.filename
                    break
            # log.info(u'  track "{}"'.format(track_file))
            path = os.path.dirname(track_file)
            # log.info(u'  path "{}"'.format(path))
            albumpaths.add(os.path.abspath(path))
        for path in albumpaths:
            log.info(u'album path: {}'.format(path))
            commandlist = [u'gnome-terminal', u'--', u'beet', 'import', path]
            log.info(u'Launching: {}'.format(u" ".join(commandlist)))
            try:
                res = res and (subprocess.run(commandlist) == 0)
            except AttributeError:  # Python2
                res = res and (subprocess.call(commandlist) == 0)
            log.info(u'Resultado: {}'.format(res))
        return res


register_album_action(BeetImport())
