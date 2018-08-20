#!/usr/bin/python3
#
# Copyright (C) 2018 Continuous Organisation.
# Author: Pierre-Louis Guhur <pierre-louis.guhur@laposte.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import argparse
import re
try:
    import cPickle as pickle
except:
    import pickle


def clean_name(name):
    return re.sub('\W+','', name.lower())


def get_config_path():
    """ Folder containing the Continuous Organisations' configuration file """
    path = os.environ.get('C_ORG_PATH', os.getcwd())
    return os.path.join(path,'configs')


def get_config_file(name = ""):
    """ File containing a Continuous Organisations' configuration """
    return os.path.join(get_config_path(), clean_name(name) + ".yaml")


def get_build_path():
    """ Folder containing the Continuous Organisations' configuration file """
    path = os.environ.get('C_ORG_PATH', os.getcwd())
    return os.path.join(path,'builds/')


def get_build_file(name = ""):
    """ File containing the build of a continuous organisation """
    return os.path.join(get_build_path(), clean_name(name) + ".build.pkl")

def get_source_path():
    """ Folder containing the Continuous Organisations' configuration file """
    path = os.environ.get('C_ORG_PATH', os.getcwd())
    return os.path.join(path,'contracts/')


def get_source_file(version):
    """ File containing the build of a continuous organisation """
    filename = "ContinuousOrganisation-v{}.sol".format(str(version))
    return os.path.join(get_source_path(), filename)



class RestrictedUnpickler(pickle.Unpickler):

    safe_builtins = {
        'range',
        'dict',
        'slice',
    }

    def find_class(self, module, name):
        # Only allow safe classes from builtins.
        if module == "builtins" and name in self.safe_builtins:
            return getattr(builtins, name)
        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                     (module, name))

def restricted_unpickle(filename):
    """Helper function analogous to pickle.load()."""
    with open(filename, 'rb') as f:
        return RestrictedUnpickler(f).load()


class ConfigurationError(Exception):
    """
    Configuration could not be parsed or has otherwise failed to apply
    """
    pass
