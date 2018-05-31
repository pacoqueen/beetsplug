#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
After a successful import, the `ok-symbolic` emblem is added to the folder in
order to notice in Nautilus what directories are currently in Beets.
"""

import os
import sys
from pathlib import Path
from gi.repository import Gio
try:
    from beets.plugins import BeetsPlugin
except ImportError:
    sys.path.append(os.path.join(os.sep, 'usr', 'share', 'beets'))
    from beets.plugins import BeetsPlugin

METADATA_EMBLEMS = 'metadata::emblems'


class NautilusEmblem(BeetsPlugin):
    """Plugin to be invoked by beets after successfully added an album."""
    def __init__(self):
        """Constructor."""
        super(NautilusEmblem, self).__init__()
        self.register_listener('pluginload', self.loaded)
        self.register_listener('import_task_files', self.files_imported)
        # Not needed after all:
        # self.register_listener('import', self.imported)
        # self.register_listener('album_imported', self.album_imported)

    def loaded(self):
        """Plugin loaded."""
        # run beet -v import to see log messages in console.
        self._log.info("NautilusEmblem loaded!")

    # pylint: disable=unused-argument
    def imported(self, lib, paths):
        """
        Item imported.
        Get metadata info via Gio, add ok-symbolic emblem and update
        modification time to force Nautilus redraw the icon.
        """
        # http://beets.readthedocs.io/en/v1.3.17/dev/plugins.html
        # import event is always called, even if aborted. So this method will
        # be called from other events and not directly by import_* event.
        for path in paths:
            self._log.info("Item imported: {}".format(path))
            gio_file = Gio.File.new_for_path(path)
            file_info = gio_file.query_info(METADATA_EMBLEMS, 0, None)
            emblem_names = file_info.get_attribute_stringv(METADATA_EMBLEMS)
            emblems = list(emblem_names)
            emblems.append("emblem-ok-symbolic.symbolic")
            emblems.append(None)
            file_info.set_attribute_stringv(METADATA_EMBLEMS, emblems)
            gio_file.set_attributes_from_info(file_info, 0, None)
            Path(path.decode("utf8")).touch()

    def files_imported(self, session, task):
        """
        After files metadata are writen, this method is invoked.
        If import task is aborted, files are not modified, so emblem is not
        added.
        If already imported tags are not updated but files are reimported. So
        this event is launched anyway and emblems are updated too (and that's
        good).
        """
        self._log.info("Files imported: {}".format(task.album.path))
        self.imported(None, (task.album.path, ))

    def album_imported(self, lib, album):
        """
        If already present album tags are valid and user ignore Beets
        recommendation («U») this callback is invoked.
        files_imported event is fired too, so this method is kinda useless.
        """
        self._log.info("Album imported: {}".format(album.path))
        self.imported(lib, (album.path, ))
