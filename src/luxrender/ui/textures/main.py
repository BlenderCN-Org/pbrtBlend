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
from ... import LuxRenderAddon
from ...ui.textures import luxrender_texture_base
from ...outputs.luxcore_api import UseLuxCore


@LuxRenderAddon.addon_register_class
class ui_texture_main(luxrender_texture_base):
    '''
    Texture Editor UI Panel
    '''

    bl_label = 'LuxRender Textures'
    bl_options = {'HIDE_HEADER'}

    display_property_groups = [
        ( ('texture',), 'luxrender_texture' )
    ]

    @classmethod
    def poll(cls, context):
        '''
        Only show LuxRender panel with 'Plugin' texture type
        '''

        tex = context.texture
        return tex and \
               (context.scene.render.engine in cls.COMPAT_ENGINES) \
               and context.texture.luxrender_texture.type is not 'BLENDER'

    def draw(self, context):
        #self.layout.separator()
        row = self.layout.row(align=True)
        row.label('LuxRender type')
        row.menu('TEXTURE_MT_luxrender_type', text=context.texture.luxrender_texture.type_label)

        if UseLuxCore():
            self.layout.separator()
            self.layout.prop(context.texture, 'use_color_ramp', text='Use Color Ramp')
            if context.texture.use_color_ramp:
                self.layout.template_color_ramp(context.texture, 'color_ramp', expand=True)

        super().draw(context)
