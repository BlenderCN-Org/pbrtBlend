# -*- coding: utf8 -*-
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
# --------------------------------------------------------------------------
# Blender 2.5 LuxRender Add-On
# --------------------------------------------------------------------------
#
# Authors:
# Doug Hammond, Daniel Genrich
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
from extensions_framework import declarative_property_group
from extensions_framework.validate import Logic_Operator as LO, Logic_OR as O, Logic_AND as A

from luxrender.properties.texture import ColorTextureParameter

class LampColorTextureParameter(ColorTextureParameter):
	def texture_slot_set_attr(self):
		return lambda s,c: getattr(c, 'luxrender_lamp_%s'%s.lamp.type.lower())
	
	def texture_collection_finder(self):
		return lambda s,c: s.object.data
	
	def get_visibility(self):
		vis = {
			'%s_colortexture' % self.attr:	{ '%s_usecolortexture' % self.attr: True },
		}
		return vis

TC_L = LampColorTextureParameter('L', 'Colour')

class luxrender_lamp(declarative_property_group):
	'''
	Storage class for LuxRender Camera settings.
	This class will be instantiated within a Blender
	lamp object.
	'''
	
	controls = [
		'importance', 'lightgroup',
	]
	
	properties = [
		{
			'type': 'string',
			'attr': 'lightgroup',
			'name': 'Light Group',
			'description': 'Name of group to put this light in',
			'default': 'default'
		},
		
		{
			'type': 'float',
			'attr': 'importance',
			'name': 'Importance',
			'description': 'Light source importance',
			'default': 0.0,
			'min': 0.0,
			'soft_min': 0.0,
			'max': 1e3,
			'soft_max': 1e3,
		},
	]
	
	def get_paramset(self):
		pass

class luxrender_lamp_basic(declarative_property_group):
	controls = TC_L.controls
	visibility = TC_L.visibility
	properties = TC_L.properties

class luxrender_lamp_point(luxrender_lamp_basic):
	pass
class luxrender_lamp_spot(luxrender_lamp_basic):
	pass

class luxrender_lamp_sun(declarative_property_group):
	controls = [
		'sunsky_type',
		'turbidity',
		'sunsky_advanced',
		'horizonbrightness',
		'horizonsize',
		'sunhalobrightness',
		'sunhalosize',
		'backscattering',
	]
	
	visibility = {
		'horizonbrightness':	{ 'sunsky_advanced': True },
		'horizonsize':			{ 'sunsky_advanced': True },
		'sunhalobrightness':	{ 'sunsky_advanced': True },
		'sunhalosize':			{ 'sunsky_advanced': True },
		'backscattering':		{ 'sunsky_advanced': True },
	}
	
	properties = [
		{
			'type': 'float',
			'attr': 'turbidity',
			'name': 'turbidity',
			'default': 2.2,
			'min': 0.7,
			'soft_min': 0.7,
			'max': 50.0,
			'soft_max': 50.0,
		},
		{
			'type': 'enum',
			'attr': 'sunsky_type',
			'name': 'Sky Type',
			'default': 'sunsky',
			'items': [
				('sunsky', 'Sun & Sky', 'sunsky'),
				('sun', 'Sun Only', 'sun'),
				('sky', 'Sky Only', 'sky'),
			]
		},
		
		{
			'type': 'bool',
			'attr': 'sunsky_advanced',
			'name': 'Advanced',
			'default': False
		},
		{
			'type': 'float',
			'attr': 'horizonbrightness',
			'name': 'Horizon brightness',
			'default': 1.0,
			'min': 0.0,
			'soft_min': 0.0,
			'max': 1.32,		# anything greater than this causes sky to break
			'soft_max': 1.32
		},
		{
			'type': 'float',
			'attr': 'horizonsize',
			'name': 'Horizon size',
			'default': 1.0,
			'min': 0.0,
			'soft_min': 0.0,
			'max': 10.0,
			'soft_max': 10.0
		},
		{
			'type': 'float',
			'attr': 'sunhalobrightness',
			'name': 'Sun halo brightness',
			'default': 1.0,
			'min': 0.0,
			'soft_min': 0.0,
			'max': 10.0,
			'soft_max': 10.0
		},
		{
			'type': 'float',
			'attr': 'sunhalosize',
			'name': 'Sun halo size',
			'default': 1.0,
			'min': 0.0,
			'soft_min': 0.0,
			'max': 10.0,
			'soft_max': 10.0
		},
		{
			'type': 'float',
			'attr': 'backscattering',
			'name': 'Back scattering',
			'default': 1.0,
			'min': 0.0,
			'soft_min': 0.0,
			'max': 10.0,
			'soft_max': 10.0
		},
	]

class luxrender_lamp_area(declarative_property_group):
	controls = TC_L.controls + [
		'power',
		'efficacy',
	]
	
	visibility = TC_L.visibility
	
	properties = TC_L.properties + [
		{
			'type': 'float',
			'attr': 'power',
			'name': 'Power',
			'default': 100.0,
			'min': 0.0,
			'soft_min': 0.0,
			'max': 1e6,
			'soft_max': 1e6,
		},
		{
			'type': 'float',
			'attr': 'efficacy',
			'name': 'Efficacy',
			'default': 17.0,
			'min': 0.0,
			'soft_min': 0.0,
			'max': 1e6,
			'soft_max': 1e6,
		},
	]

class luxrender_lamp_hemi(declarative_property_group):
	controls = [
		[0.323, 'L_colorlabel', 'L_color'],
		'infinite_map',
		'mapping_type',
	]
	
	visibility = {
		'mapping_type':	{ 'infinite_map': LO({'!=': ''}) },
	}
	
	properties = TC_L.properties + [
		{
			'type': 'string',
			'subtype': 'FILE_PATH',
			'attr': 'infinite_map',
			'name': 'HDRI Map',
			'description': 'HDR image to use for lighting',
			'default': ''
		},
		{
			'type': 'enum',
			'attr': 'mapping_type',
			'name': 'Map Type',
			'default': 'latlong',
			'items': [
				('latlong', 'Lat Long', 'latlong'),
				('angular', 'Angular', 'angular'),
				('vcross', 'Vert Cross', 'vcross')
			]
		},
	]


