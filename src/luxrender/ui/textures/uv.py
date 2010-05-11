# -*- coding: utf8 -*-
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
# --------------------------------------------------------------------------
# Blender 2.5 Exporter Framework - LuxRender Plug-in
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
import bpy

from ...export import ParamSet
from ..textures import luxrender_texture_base

class uv(bpy.types.IDPropertyGroup):
	
	def get_paramset(self):
		
		uv_params = ParamSet()
			
		return {'2DMAPPING'}, uv_params

class ui_panel_uv(luxrender_texture_base):
	bl_label = 'LuxRender UV Texture'
	
	LUX_COMPAT = {'uv'}
	
	property_group = uv
	
	controls = [
		# None
	]
	
	visibility = {} 
	
	properties = [
		{
			'type': 'string',
			'attr': 'variant',
			'default': 'color'
		},
	]
