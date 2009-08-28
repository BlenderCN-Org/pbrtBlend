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
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****
#
from ef.ui import context_panel
from ef.ui import material_settings_panel
from ef.ui import described_layout

from ef.ef import ef

import bpy

class main(
	context_panel,
	material_settings_panel,
	described_layout):
	__label__ = 'LuxRender Materials'
	context_name = 'luxrender'
	
	controls = [
		# Common props
		'lux_material',
		
		# Used by many
		#'lux_mat_kd',
		#'lux_mat_kr',
		#'lux_mat_kt',
		#['lux_mat_ior_preset', 'lux_mat_ior_list'],
		
		# Car paint
		#'lux_mat_carpaint_label',
		#'lux_mat_carpaint_preset',
		
		#'lux_mat_carpaint_ks1',
		#'lux_mat_carpaint_ks2',
		#'lux_mat_carpaint_ks3',
		#['lux_mat_carpaint_r1','lux_mat_carpaint_r2','lux_mat_carpaint_r3'],
		#['lux_mat_carpaint_m1','lux_mat_carpaint_m2','lux_mat_carpaint_m3'],
		
		# Glass
		
	]
	
	selection = {
		# Used by many
		#'lux_mat_kd':					[{ 'lux_material': ['carpaint', 'glass'] }],
		#'lux_mat_kr':					[{ 'lux_material': ['glass'] }],
		#'lux_mat_kt':					[{ 'lux_material': ['glass'] }],
		#'lux_mat_ior_preset':			[{ 'lux_material': ['glass'] }],
		#'lux_mat_ior_list':				[{ 'lux_material': ['glass'] }],
	
		# Car paint
		#'lux_mat_carpaint_label':		[{ 'lux_material': 'carpaint' }],
		#'lux_mat_carpaint_preset':		[{ 'lux_material': 'carpaint' }],
		# Car paint custom
		#'lux_mat_carpaint_kd':			[{ 'lux_material': 'carpaint' }, { 'lux_mat_carpaint_preset': 'custom' }],
		#'lux_mat_carpaint_ks1':			[{ 'lux_material': 'carpaint' }, { 'lux_mat_carpaint_preset': 'custom' }],
		#'lux_mat_carpaint_ks2':			[{ 'lux_material': 'carpaint' }, { 'lux_mat_carpaint_preset': 'custom' }],
		#'lux_mat_carpaint_ks3':			[{ 'lux_material': 'carpaint' }, { 'lux_mat_carpaint_preset': 'custom' }],
		#'lux_mat_carpaint_r1':			[{ 'lux_material': 'carpaint' }, { 'lux_mat_carpaint_preset': 'custom' }],
		#'lux_mat_carpaint_r2':			[{ 'lux_material': 'carpaint' }, { 'lux_mat_carpaint_preset': 'custom' }],
		#'lux_mat_carpaint_r3':			[{ 'lux_material': 'carpaint' }, { 'lux_mat_carpaint_preset': 'custom' }],
		#'lux_mat_carpaint_m1':			[{ 'lux_material': 'carpaint' }, { 'lux_mat_carpaint_preset': 'custom' }],
		#'lux_mat_carpaint_m2':			[{ 'lux_material': 'carpaint' }, { 'lux_mat_carpaint_preset': 'custom' }],
		#'lux_mat_carpaint_m3':			[{ 'lux_material': 'carpaint' }, { 'lux_mat_carpaint_preset': 'custom' }],
		
		# Glass
		
	}
	
	material_properties = [
		# Material Type Select
		{
			'type': 'enum',
			'attr': 'lux_material',
			'name': 'Type',
			'description': 'LuxRender material type',
			'items': [
				('carpaint', 'Car Paint', 'carpaint'),
				('glass', 'Glass', 'glass'),
				('roughglass','Rough Glass','roughglass'),
				('glossy','Glossy','glossy'),
				('matte','Matte','matte'),
				('mattetranslucent','Matte Translucent','mattetranslucent'),
				('metal','Metal','metal'),
				('shinymetal','Shiny Metal','shinymetal'),
				('mirror','Mirror','mirror'),
				('mix','Mix','mix'),
				('null','Null','null'),
				('boundvolume','Bound Volume','boundvolume'),
				('light','Light','light'),
				('portal','Portal','portal'),
			]
		},
		
		# Used by many mats
		{
			'type': 'string',
			'attr': 'lux_mat_kd',
			'name': 'Diffuse Colour',
			'description': 'Diffuse Colour',
			'default': '-- TODO --',
		},
		{
			'type': 'string',
			'attr': 'lux_mat_kr',
			'name': 'Reflection Colour',
			'description': 'Reflection Colour',
			'default': '-- TODO --',
		},
		{
			'type': 'string',
			'attr': 'lux_mat_kt',
			'name': 'Transmission Colour',
			'description': 'Transmission Colour',
			'default': '-- TODO --',
		},
		{
			'type': 'bool',
			'attr': 'lux_mat_ior_preset',
			'name': 'IOR Preset',
			'description': 'IOR Preset',
			'default': True,
		},
		{
			'type': 'enum',
			'attr': 'lux_mat_ior_list',
			'name': 'IOR',
			'description': 'IOR',
			'default': '1.5',
			'items': [
				('1.5', 'Fused Silica Glass', 'Fused Silica Glass'),
				('0', '-- TODO --', '0'),
			]
		},
		
		
		# Car paint
		{
			'type': 'text',
			'attr': 'lux_mat_carpaint_label',
			'name': 'Car Paint Settings',
		},
		{
			'type': 'enum',
			'attr': 'lux_mat_carpaint_preset',
			'name': 'Preset',
			'description': 'Preset Car Paint Settings',
			'default': 'custom',
			'items': [
				('custom','Custom','custom'),
				('fordf8','Ford F8','fordf8'),
				('polaris','Polaris Silver','polaris'),
				('opel','Opel Titan','opel'),
				('bmw339','BMW 339','bmw339'),
				('2k','2K Acrylic','2k'),
				('white','White','white'),
				('blue','Blue','blue'),
				('bluematte','Blue Matte','bluematte'),
			]
		},
		{
			'type': 'string',
			'attr': 'lux_mat_carpaint_ks1',
			'name': 'Specular Layer 1',
			'description': 'Specular Layer 1 Colour',
			'default': '-- TODO --',
		},
		{
			'type': 'string',
			'attr': 'lux_mat_carpaint_ks2',
			'name': 'Specular Layer 2',
			'description': 'Specular Layer 2 Colour',
			'default': '-- TODO --',
		},
		{
			'type': 'string',
			'attr': 'lux_mat_carpaint_ks3',
			'name': 'Specular Layer 3',
			'description': 'Specular Layer 3 Colour',
			'default': '-- TODO --',
		},
		{
			'type': 'float',
			'attr': 'lux_mat_carpaint_r1',
			'name': 'R 1',
			'description': 'Specular Layer 1 Roughness',
			'default': 1,
			'min': 0,
			'soft_min': 0,
			'max': 1,
			'soft_max': 1,
		},
		{
			'type': 'float',
			'attr': 'lux_mat_carpaint_r2',
			'name': 'R 2',
			'description': 'Specular Layer 2 Roughness',
			'default': 1,
			'min': 0,
			'soft_min': 0,
			'max': 1,
			'soft_max': 1,
		},
		{
			'type': 'float',
			'attr': 'lux_mat_carpaint_r3',
			'name': 'R 3',
			'description': 'Specular Layer 3 Roughness',
			'default': 1,
			'min': 0,
			'soft_min': 0,
			'max': 1,
			'soft_max': 1,
		},
		{
			'type': 'float',
			'attr': 'lux_mat_carpaint_m1',
			'name': 'M 1',
			'description': 'Specular Layer 1 Fresnel',
			'default': 1,
			'min': 0,
			'soft_min': 0,
			'max': 1,
			'soft_max': 1,
		},
		{
			'type': 'float',
			'attr': 'lux_mat_carpaint_m2',
			'name': 'M 2',
			'description': 'Specular Layer 2 Fresnel',
			'default': 1,
			'min': 0,
			'soft_min': 0,
			'max': 1,
			'soft_max': 1,
		},
		{
			'type': 'float',
			'attr': 'lux_mat_carpaint_m3',
			'name': 'M 3',
			'description': 'Specular Layer 3 Fresnel',
			'default': 1,
			'min': 0,
			'soft_min': 0,
			'max': 1,
			'soft_max': 1,
		},
		
		# Glass
		
	]
	
	def get_properties(self):
		return self.material_properties
	
	def draw(self, context):
		if context.material is not None:
			if not hasattr(context.material, 'lux_material'):
				ef.init_properties(context.material, self.material_properties)
			
			for p in self.controls:
				self.draw_column(p, self.layout, context.material)
