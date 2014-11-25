# -*- coding: utf8 -*-
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
# --------------------------------------------------------------------------
# Blender 2.5 LuxRender Add-On
# --------------------------------------------------------------------------
#
# Authors:
# Doug Hammond
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# ***** END GPL LICENCE BLOCK *****
#
bl_info = {
    "name": "LuxRender",
    "author": "LuxRender Project: Doug Hammond (dougal2), Asbjørn Heid (LordCrc), Daniel Genrich (Genscher), \
    Jens Verwiebe, Jason Clarke (JtheNinja), Michael Klemm (neo2068)",
    "version": (1, 4, 'RC2'),
    "blender": (2, 67, 1),
    "api": 57908,
    "category": "Render",
    "location": "Info header, render engine menu",
    "warning": "",
    "wiki_url": "http://www.luxrender.net/wiki/LuxBlend25_Manual",
    "tracker_url": "http://www.luxrender.net/mantis",
    "description": "LuxRender integration for Blender"
}

def find_luxrender_path():
    from os import getenv
    from .extensions_framework import util as efutil

    return getenv(  # Use the env var path, if set ...
                    'LUXRENDER_ROOT',  # .. or load the last path from CFG file
                    efutil.find_config_value('luxrender', 'defaults', 'install_path', '')
    )

def import_bindings_module(name):
    """Import Lux Python bindings module (e.g. pylux)."""
    import os.path
    import sys
    import importlib
    from .outputs import LuxLog

    def _import_bindings_module(path, name, relative=False):
        LuxLog('Attempting to import {} module '
               'from "{}"'.format(name, path))
        sys.path.insert(0, path)
        if relative:
            package = os.path.split(path)[1]
            module = importlib.import_module('.' + name, package=package)
        else:
            module = importlib.import_module(name)
        LuxLog('{} module imported successfully'.format(name.title()))
        del sys.path[0]
        return module

    lux_path = find_luxrender_path() \
            or bpy.context.user_preferences.addons[__name__].preferences
    luxblend_path = os.path.dirname(os.path.abspath(__file__))
    if sys.platform == 'darwin':
        return _import_bindings_module(luxblend_path, name, True)
    else:
        try:
            module = _import_bindings_module(lux_path, name)
        except ImportError:
            LuxLog('Failed to import {} module '
                   'from "{}"'.format(name, lux_path))
            module = _import_bindings_module(luxblend_path, name)
        return module

if 'core' in locals():
    import imp

    imp.reload(core)
else:
    import bpy
    from bpy.types import AddonPreferences
    from bpy.props import StringProperty, IntProperty, BoolProperty
    from .extensions_framework import Addon
    import nodeitems_utils
    from nodeitems_utils import NodeCategory, NodeItem, NodeItemCustom

    class LuxRenderAddonPreferences(AddonPreferences):
        # this must match the addon name
        bl_idname = __name__

        install_path = StringProperty(
            name="Path to LuxRender Installation",
            description='Path to LuxRender install directory',
            subtype='DIR_PATH',
            default=find_luxrender_path(),
        )

        def draw(self, context):
            layout = self.layout
            # layout.label(text="This is a preferences view for our addon")
            layout.prop(self, "install_path")

    LuxRenderAddon = Addon(bl_info)

    def get_prefs():
        return bpy.context.user_preferences.addons[__name__].preferences

    # patch the LuxRenderAddon class to make it easier to get the addon prefs
    LuxRenderAddon.get_prefs = get_prefs

    addon_register, addon_unregister = LuxRenderAddon.init_functions()

    def register():
        bpy.utils.register_class(LuxRenderAddonPreferences)
        nodeitems_utils.register_node_categories("LUX_SHADER", ui.node_editor.luxrender_node_catagories)
        addon_register()

    def unregister():
        bpy.utils.unregister_class(LuxRenderAddonPreferences)
        nodeitems_utils.unregister_node_categories("LUX_SHADER")
        addon_unregister()


    # Importing the core package causes extensions_framework managed
    # RNA class registration via @LuxRenderAddon.addon_register_class
    from . import core
