#!/usr/bin/python
# -*- coding: utf-8 -*-

# for localized messages

from . import _
from boxbranding import getImageDistro, getImageVersion
from Components.config import config, ConfigSubsection, ConfigSelection
from enigma import getDesktop
from Plugins.Plugin import PluginDescriptor
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import SCOPE_ACTIVE_SKIN, resolveFilename

from Components.MovieList import MovieList
from Screens.MovieSelection import MovieSelection

import sys

distro = getImageDistro()
imageversion = getImageVersion()
# print("******** distro %s " % distro)
# print("******** imageversion %s " % imageversion)

screenwidth = getDesktop(0).size()

config.movielistmod = ConfigSubsection()
config.movielistmod.useextlist = ConfigSelection(default='0', choices={'0': _('No'), '3': _('Sky Planner'), '4': _('Slyk Q Planner'), '5': _('Slyk Onyx Planner'), '6': _('VSkin Planner')})
config.movielist.useextlist = ConfigSelection(default='0', choices={'0': _('No'), '3': _('Sky Planner'), '4': _('Slyk Q Planner'), '5': _('Slyk Onyx Planner'), '6': _('VSkin Planner')})

pythonVer = sys.version_info.major


def MovieList1__init__(self, root=None, sort_type=None, descr_state=None, allowCollections=False):
    try:
        myMovieList__init__(self, root, sort_type, descr_state, allowCollections)
    except Exception as e:
        print(e)
        myMovieList__init__(self, root, sort_type, descr_state)
    self.screenwidth = getDesktop(0).size().width()
    self.iconSeries = LoadPixmap(resolveFilename(SCOPE_ACTIVE_SKIN, "icons/series.png"))
    self.iconDownloaded = LoadPixmap(resolveFilename(SCOPE_ACTIVE_SKIN, "icons/downloaded.png"))


def autostart(reason, session=None, **kwargs):
    # print("*** autostart ***")
    if session is not None:

        global myMovieList__init__
        global myMovieSelection__init__

        myMovieList__init__ = MovieList.__init__

    if distro.lower() == "openvix":
        # print("******** openvix *****")

        from .openvixmovieselection import configure2

        if float(imageversion) >= 5.4:
            from .openvix6 import openvix6BuildMovieListEntry
        elif float(imageversion) <= 5.3:
            from .openvix53 import openvix53BuildMovieListEntry

        MovieList.__init__ = MovieList1__init__

        if float(imageversion) >= 5.4:
            MovieList.buildMovieListEntry = openvix6BuildMovieListEntry
        elif float(imageversion) <= 5.3:
            MovieList.buildMovieListEntry = openvix53BuildMovieListEntry

        MovieSelection.configure = configure2

    elif distro.lower() == "openatv":
        # print("******** openatv *****")

        from .openatv import openatvBuildMovieListEntry, openatvSetItemsPerPage

        MovieList.__init__ = MovieList1__init__

        try:
            MovieList.setItemsPerPage = openatvSetItemsPerPage
            MovieList.buildMovieListEntry = openatvBuildMovieListEntry
        except Exception as e:
            print(e)


def Plugins(**kwargs):
    # print("*** plugins ***")
    iconFile = 'icons/plugin-icon_sd.png'
    if screenwidth.width() > 1280:
        iconFile = 'icons/plugin-icon.png'
    description = (_('Movie Planner Layout Mod'))
    pluginname = (_('MoviePlannerMod'))
    result = [PluginDescriptor(name=pluginname, description=description, where=[PluginDescriptor.WHERE_SESSIONSTART], icon=iconFile, fnc=autostart)]
    return result
