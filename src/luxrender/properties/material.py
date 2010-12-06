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
import math

import bpy

from copy import deepcopy

from extensions_framework import declarative_property_group
from extensions_framework import util as efutil

from luxrender.properties.texture import FresnelTextureParameter, FloatTextureParameter, ColorTextureParameter
from luxrender.export import ParamSet
from luxrender.export.materials import add_texture_parameter, ExportedMaterials
from luxrender.outputs.pure_api import LUXRENDER_VERSION

def MaterialParameter(attr, name, property_group):
	return [
		{
			'attr': '%s_material' % attr,
			'type': 'string',
			'name': '%s_material' % attr,
			'description': '%s_material' % attr,
			'save_in_preset': True
		},
		{
			'type': 'prop_search',
			'attr': attr,
			'src': lambda s,c: s.object,
			'src_attr': 'material_slots',
			'trg': lambda s,c: getattr(c, property_group),
			'trg_attr': '%s_material' % attr,
			'name': name
		},
	]

def VolumeParameter(attr, name):
	return [
		{
			'attr': '%s_volume' % attr,
			'type': 'string',
			'name': '%s_volume' % attr,
			'description': '%s_volume' % attr,
			'save_in_preset': True
		},
		{
			'type': 'prop_search',
			'attr': attr,
			'src': lambda s,c: s.scene.luxrender_volumes,
			'src_attr': 'volumes',
			'trg': lambda s,c: c.luxrender_mat_glass2,
			'trg_attr': '%s_volume' % attr,
			'name': name
		},
	]

class VolumeDataColorTextureParameter(ColorTextureParameter):
	#texture_collection = 'textures'
	def texture_collection_finder(self):
		def func(s,c):
			return s #.main
		return func
	
	def texture_slot_set_attr(self):
		def func2(s,c):
			return c
		return func2

class VolumeDataFresnelTextureParameter(FresnelTextureParameter):
	#texture_collection = 'textures'
	def texture_collection_finder(self):
		def func(s,c):
			return s #.main
		return func
	
	def texture_slot_set_attr(self):
		def func2(s,c):
			return c
		return func2

# TODO: add override props to *TextureParameter instead of using these sub-types

class SubGroupFloatTextureParameter(FloatTextureParameter):
	def texture_slot_set_attr(self):
		# Looks in a different location than other FloatTextureParameters
		return lambda s,c: c.luxrender_material



# Fresnel Textures
TFR_IOR					= VolumeDataFresnelTextureParameter('fresnel', 'IOR',				add_float_value = False)

# Float Textures
TF_bumpmap				= SubGroupFloatTextureParameter('bumpmap', 'Bump Map',				add_float_value=True, precision=6, multiply_float=True, ignore_zero=True )
TF_amount				= FloatTextureParameter('amount', 'Mix Amount',						add_float_value=True, min=0.0, default=0.5, max=1.0 )
TF_cauchyb				= FloatTextureParameter('cauchyb', 'Cauchy B',						add_float_value=True, default=0.0, min=0.0, max=1.0 ) # default 0.0 for OFF
TF_d					= FloatTextureParameter('d', 'Absorption Depth',					add_float_value=True, default=0.0, min=0.0, max=15.0 ) # default 0.0 for OFF
TF_film					= FloatTextureParameter('film', 'Thin Film Thickness (nm)',			add_float_value=True, min=0.0, default=0.0, max=1500.0 ) # default 0.0 for OFF
TF_filmindex			= FloatTextureParameter('filmindex', 'Film IOR',					add_float_value=True, default=1.5, min=1.0, max=6.0 )
TF_index				= FloatTextureParameter('index', 'IOR',								add_float_value=True, min=0.0, max=25.0, default=1.0)
TF_M1					= FloatTextureParameter('M1', 'M1',									add_float_value=True, default=1.0, min=0.0, max=1.0 )
TF_M2					= FloatTextureParameter('M2', 'M2',									add_float_value=True, default=1.0, min=0.0, max=1.0 )
TF_M3					= FloatTextureParameter('M3', 'M3',									add_float_value=True, default=1.0, min=0.0, max=1.0 )
TF_R1					= FloatTextureParameter('R1', 'R1',									add_float_value=True, min=0.00001, max=1.0, default=0.0002 )
TF_R2					= FloatTextureParameter('R2', 'R2',									add_float_value=True, min=0.00001, max=1.0, default=0.0002 )
TF_R3					= FloatTextureParameter('R3', 'R3',									add_float_value=True, min=0.00001, max=1.0, default=0.0002 )
TF_sigma				= FloatTextureParameter('sigma', 'Sigma',							add_float_value=True, min=0.0, max=100.0 )
TF_uroughness			= FloatTextureParameter('uroughness', 'uroughness',					add_float_value=True, min=0.00001, max=1.0, default=0.0002 )
TF_vroughness			= FloatTextureParameter('vroughness', 'vroughness',					add_float_value=True, min=0.00001, max=1.0, default=0.0002 )
TF_backface_d			= FloatTextureParameter('bf_d', 'Backface Absorption Depth',		real_attr='backface_d', add_float_value=True, default=0.0, min=0.0, max=15.0 ) # default 0.0 for OFF
TF_backface_index		= FloatTextureParameter('bf_index', 'Backface IOR',				real_attr='backface_index', add_float_value=True, min=0.0, max=25.0, default=1.0)
TF_backface_uroughness	= FloatTextureParameter('bf_uroughness', 'Backface uroughness',	real_attr='backface_uroughness', add_float_value=True, min=0.00001, max=1.0, default=0.0002 )
TF_backface_vroughness	= FloatTextureParameter('bf_vroughness', 'Backface vroughness',	real_attr='backface_vroughness', add_float_value=True, min=0.00001, max=1.0, default=0.0002 )


# Color Textures
TC_Ka			= ColorTextureParameter('Ka', 'Absorption color',						default=(0.0,0.0,0.0) )
TC_Kd			= ColorTextureParameter('Kd', 'Diffuse color',							default=(0.64,0.64,0.64) )
TC_Kr			= ColorTextureParameter('Kr', 'Reflection color',						default=(1.0,1.0,1.0) )
TC_Ks			= ColorTextureParameter('Ks', 'Specular color',							default=(0.25,0.25,0.25) )
TC_Ks1			= ColorTextureParameter('Ks1', 'Specular color 1',						default=(1.0,1.0,1.0) )
TC_Ks2			= ColorTextureParameter('Ks2', 'Specular color 2',						default=(1.0,1.0,1.0) )
TC_Ks3			= ColorTextureParameter('Ks3', 'Specular color 3',						default=(1.0,1.0,1.0) )
TC_Kt			= ColorTextureParameter('Kt', 'Transmission color',						default=(1.0,1.0,1.0) )
TC_backface_Ka	= ColorTextureParameter('backface_Ka', 'Backface Absorption color',		default=(0.0,0.0,0.0) )
TC_backface_Kd	= ColorTextureParameter('backface_Kd', 'Backface Diffuse color',		default=(0.64,0.64,0.64) )
TC_backface_Ks	= ColorTextureParameter('backface_Ks', 'Backface Specular color',		default=(0.25,0.25,0.25) )

TC_absorption	= VolumeDataColorTextureParameter('absorption', 'Absorption',	default=(1.0,1.0,1.0))

def dict_merge(*args):
	vis = {}
	for vis_dict in args:
		vis.update(deepcopy(vis_dict))	# need a deepcopy since nested dicts return references!
	return vis

def mat_list():
	mat_list = [
		('carpaint', 'Car Paint', 'carpaint'),
		('glass', 'Glass', 'glass'),
		('glass2', 'Glass2', 'glass2'),
		('roughglass','Rough Glass','roughglass'),
		('glossy','Glossy','glossy'),
		('glossy_lossy','Glossy (Lossy)','glossy_lossy'),
		('matte','Matte','matte'),
		('mattetranslucent','Matte Translucent','mattetranslucent'),
		('metal','Metal','metal'),
		('mirror','Mirror','mirror'),
		('mix','Mix','mix'),
		('null','Null','null'),
		('shinymetal','Shiny Metal','shinymetal'),
	]
	
	if LUXRENDER_VERSION >= '0.7.1':
		mat_list += [
			('velvet', 'Velvet', 'velvet'),
			('glossytranslucent', 'Glossy Translucent', 'glossytranslucent'),
		]
	
	mat_list.sort()
	
	return mat_list

class luxrender_material(declarative_property_group):
	'''
	Storage class for LuxRender Material settings.
	This class will be instantiated within a Blender Material
	object.
	'''
	
	controls = [
		'type',
	] + \
	TF_bumpmap.controls
	
	visibility = dict_merge({}, TF_bumpmap.visibility)
	
	properties = [
		# Material Type Select
		{
			'type': 'enum',
			'attr': 'type',
			'name': 'Type',
			'description': 'LuxRender material type',
			'default': 'matte',
			'items': mat_list(),
			'save_in_preset': True
		},
	] + \
	TF_bumpmap.properties
	
	def export(self, scene, lux_context, material, mode='indirect'):
		
		if mode=='indirect' and material.name in ExportedMaterials.exported_material_names:
			return
		
		if self.type == 'mix':
			# First export the other mix mats
			m1 = bpy.data.materials[self.luxrender_mat_mix.namedmaterial1_material] 
			m1.luxrender_material.export(scene, lux_context, m1, 'indirect')
			m2 = bpy.data.materials[self.luxrender_mat_mix.namedmaterial2_material] 
			m2.luxrender_material.export(scene, lux_context, m2, 'indirect')
		
		material_params = ParamSet()
		
		sub_type = getattr(self, 'luxrender_mat_%s'%self.type)
		
		# Bump mapping
		if self.type not in ['mix', 'null']:
			material_params.update( TF_bumpmap.get_paramset(self) )
		
		material_params.update( sub_type.get_paramset(scene) )
		
		# DistributedPath compositing
		if scene.luxrender_integrator.surfaceintegrator == 'distributedpath':
			material_params.update( self.luxrender_mat_compositing.get_paramset(scene) )
		
		if mode == 'indirect':
			material_params.add_string('type', self.type)
			ExportedMaterials.makeNamedMaterial(material.name, material_params)
			ExportedMaterials.export_new_named(lux_context)
		elif mode == 'direct':
			lux_context.material(self.type, material_params)

class luxrender_mat_compositing(declarative_property_group):
	'''
	Storage class for LuxRender Material compositing settings
	for DistributedPath integrator.
	'''
	
	controls = [
		'enabled',
		['visible_material',
		'visible_emission'],
		['visible_indirect_material',
		'visible_indirect_emission'],
		'override_alpha',
		'override_alpha_value',
	]
	
	visibility = {
		'visible_material':					{ 'enabled': True },
		'visible_emission':					{ 'enabled': True },
		'visible_indirect_material':		{ 'enabled': True },
		'visible_indirect_emission':		{ 'enabled': True },
		'override_alpha':					{ 'enabled': True },
		'override_alpha_value':				{ 'enabled': True, 'override_alpha': True },
	}
	
	properties = [
		{
			'type': 'bool',
			'attr': 'enabled',
			'name': 'Use compositing settings',
			'default': False,
			'save_in_preset': True
		},
		{
			'type': 'bool',
			'attr': 'visible_material',
			'name': 'Visible Material',
			'default': True,
			'save_in_preset': True
		},
		{
			'type': 'bool',
			'attr': 'visible_emission',
			'name': 'Visible Emission',
			'default': True,
			'save_in_preset': True
		},
		{
			'type': 'bool',
			'attr': 'visible_indirect_material',
			'name': 'Visible Indirect Material',
			'default': True,
			'save_in_preset': True
		},
		{
			'type': 'bool',
			'attr': 'visible_indirect_emission',
			'name': 'Visible Indirect Emission',
			'default': True,
			'save_in_preset': True
		},
		{
			'type': 'bool',
			'attr': 'override_alpha',
			'name': 'Override Alpha',
			'default': False,
			'save_in_preset': True
		},
		{
			'type': 'float',
			'attr': 'override_alpha_value',
			'name': 'Override Alpha Value',
			'default': 0.0,
			'min': 0.0,
			'soft_min': 0.0,
			'max': 1.0,
			'soft_max': 1.0,
			'save_in_preset': True
		},
	]
	
	def get_paramset(self, scene):
		compo_params = ParamSet()
		
		if self.enabled:
			compo_params.add_bool('compo_visible_material', self.visible_material)
			compo_params.add_bool('compo_visible_emission', self.visible_emission)
			compo_params.add_bool('compo_visible_indirect_material', self.visible_indirect_material)
			compo_params.add_bool('compo_visible_indirect_emission', self.visible_indirect_emission)
			compo_params.add_bool('compo_override_alpha', self.override_alpha)
			if self.override_alpha:
				compo_params.add_float('compo_override_alpha_value', self.override_alpha_value)
		
		return compo_params

def texture_append_visibility(vis_main, textureparam_object, vis_append):
	for prop in textureparam_object.properties:
		if 'attr' in prop.keys():
			if not prop['attr'] in vis_main.keys():
				vis_main[prop['attr']] = {}
			for vk, vi in vis_append.items():
				vis_main[prop['attr']][vk] = vi
	return vis_main

def carpaint_visibility():
	cp_vis = dict_merge(
		TF_d.visibility,
		TC_Ka.visibility,
		TC_Kd.visibility,
		TC_Ks1.visibility,
		TC_Ks2.visibility,
		TC_Ks3.visibility,
		TF_M1.visibility,
		TF_M2.visibility,
		TF_M3.visibility,
		TF_R1.visibility,
		TF_R2.visibility,
		TF_R3.visibility
	)
	
	vis_append = { 'name': '-' }
	cp_vis = texture_append_visibility(cp_vis, TC_Kd, vis_append)
	cp_vis = texture_append_visibility(cp_vis, TC_Ks1, vis_append)
	cp_vis = texture_append_visibility(cp_vis, TC_Ks2, vis_append)
	cp_vis = texture_append_visibility(cp_vis, TC_Ks3, vis_append)
	
	cp_vis = texture_append_visibility(cp_vis, TF_M1, vis_append)
	cp_vis = texture_append_visibility(cp_vis, TF_M2, vis_append)
	cp_vis = texture_append_visibility(cp_vis, TF_M3, vis_append)
	cp_vis = texture_append_visibility(cp_vis, TF_R1, vis_append)
	cp_vis = texture_append_visibility(cp_vis, TF_R2, vis_append)
	cp_vis = texture_append_visibility(cp_vis, TF_R3, vis_append)
	
	return cp_vis

class luxrender_mat_carpaint(declarative_property_group):
	
	controls = [
		'name'
	] + \
		TF_d.controls + \
		TC_Ka.controls + \
		TC_Kd.controls + \
		TC_Ks1.controls + \
		TC_Ks2.controls + \
		TC_Ks3.controls + \
		TF_M1.controls + \
		TF_M2.controls + \
		TF_M3.controls + \
		TF_R1.controls + \
		TF_R2.controls + \
		TF_R3.controls
	
	visibility = carpaint_visibility()
	
	properties = [
		{
			'type': 'enum',
			'attr': 'name',
			'name': 'Preset',
			'items': [
				('-', 'Manual settings', '-'),
				('2k acrylack', '2k Acrylack', '2k acrylack'),
				('blue', 'Blue', 'blue'),
				('blue matte', 'Blue Matte', 'blue matte'),
				('bmw339', 'BMW 339', 'bmw339'),
				('ford f8', 'Ford F8', 'ford f8'),
				('opel titan', 'Opel Titan', 'opel titan'),
				('polaris silber', 'Polaris Silber', 'polaris silber'),
				('white', 'White', 'white'),
			],
			'save_in_preset': True
		},
	] + \
		TF_d.properties + \
		TC_Ka.properties + \
		TC_Kd.properties + \
		TC_Ks1.properties + \
		TC_Ks2.properties + \
		TC_Ks3.properties + \
		TF_M1.properties + \
		TF_M2.properties + \
		TF_M3.properties + \
		TF_R1.properties + \
		TF_R2.properties + \
		TF_R3.properties
	
	def get_paramset(self, scene):
		carpaint_params = ParamSet()
		
		if self.d_floatvalue > 0:
			carpaint_params.update( TF_d.get_paramset(self) )
			carpaint_params.update( TC_Ka.get_paramset(self) )
		
		if self.name == '-':	# Use manual settings
			carpaint_params.update( TC_Kd.get_paramset(self) )
			carpaint_params.update( TC_Ks1.get_paramset(self) )
			carpaint_params.update( TC_Ks2.get_paramset(self) )
			carpaint_params.update( TC_Ks3.get_paramset(self) )
			carpaint_params.update( TF_M1.get_paramset(self) )
			carpaint_params.update( TF_M2.get_paramset(self) )
			carpaint_params.update( TF_M3.get_paramset(self) )
			carpaint_params.update( TF_R1.get_paramset(self) )
			carpaint_params.update( TF_R2.get_paramset(self) )
			carpaint_params.update( TF_R3.get_paramset(self) )
		else:					# Use preset
			carpaint_params.add_string('name', self.name)
		
		return carpaint_params

class luxrender_mat_glass(declarative_property_group):
	
	controls = [
		'architectural',
	] + \
		TF_cauchyb.controls + \
		TF_film.controls + \
		TF_filmindex.controls + \
		TF_index.controls + \
		TC_Kr.controls + \
		TC_Kt.controls
	
	visibility = dict_merge(
		TF_cauchyb.visibility,
		TF_film.visibility,
		TF_filmindex.visibility,
		TF_index.visibility,
		TC_Kr.visibility,
		TC_Kt.visibility
	)
	
	properties = [
		{
			'type': 'bool',
			'attr': 'architectural',
			'name': 'Architectural',
			'default': False,
			'save_in_preset': True
		},
	] + \
		TF_cauchyb.properties + \
		TF_film.properties + \
		TF_filmindex.properties + \
		TF_index.properties + \
		TC_Kr.properties + \
		TC_Kt.properties
	
	def get_paramset(self, scene):
		glass_params = ParamSet()
		
		glass_params.add_bool('architectural', self.architectural)
		
		glass_params.update( TF_cauchyb.get_paramset(self) )
		glass_params.update( TF_film.get_paramset(self) )
		glass_params.update( TF_filmindex.get_paramset(self) )
		glass_params.update( TF_index.get_paramset(self) )
		glass_params.update( TC_Kr.get_paramset(self) )
		glass_params.update( TC_Kt.get_paramset(self) )
		
		return glass_params

class luxrender_mat_glass2(declarative_property_group):
	
	controls = [
		'architectural',
		'dispersion',
		
		# Glass 2 Volumes
		'Interior',
		'Exterior'
	]
	
	visibility = {}
	
	properties = [
		{
			'type': 'bool',
			'attr': 'architectural',
			'name': 'Architectural',
			'default': False,
			'save_in_preset': True
		},
		{
			'type': 'bool',
			'attr': 'dispersion',
			'name': 'Dispersion',
			'default': False,
			'save_in_preset': True
		},
	] + \
		VolumeParameter('Interior', 'Interior') + \
		VolumeParameter('Exterior', 'Exterior')
	
	def get_paramset(self, scene):
		glass2_params = ParamSet()
		
		glass2_params.add_bool('architectural', self.architectural)
		glass2_params.add_bool('dispersion', self.dispersion)
		
		return glass2_params

class luxrender_mat_roughglass(declarative_property_group):
	
	controls = [
	] + \
		TF_cauchyb.controls + \
		TF_index.controls + \
		TC_Kr.controls + \
		TC_Kt.controls + \
		TF_uroughness.controls + \
		TF_vroughness.controls
	
	visibility = dict_merge(
		TF_cauchyb.visibility,
		TF_index.visibility,
		TC_Kr.visibility,
		TC_Kt.visibility,
		TF_uroughness.visibility,
		TF_vroughness.visibility
	)
	
	properties = [
	] + \
		TF_cauchyb.properties + \
		TF_index.properties + \
		TC_Kr.properties + \
		TC_Kt.properties + \
		TF_uroughness.properties + \
		TF_vroughness.properties
	
	def get_paramset(self, scene):
		roughglass_params = ParamSet()
		
		roughglass_params.update( TF_cauchyb.get_paramset(self) )
		roughglass_params.update( TF_index.get_paramset(self) )
		roughglass_params.update( TC_Kr.get_paramset(self) )
		roughglass_params.update( TC_Kt.get_paramset(self) )
		roughglass_params.update( TF_uroughness.get_paramset(self) )
		roughglass_params.update( TF_vroughness.get_paramset(self) )
		
		return roughglass_params

def glossy_visibility():
	g_vis = dict_merge(
		TF_d.visibility,
		TF_index.visibility,
		TC_Ka.visibility,
		TC_Kd.visibility,
		TC_Ks.visibility,
		TF_uroughness.visibility,
		TF_vroughness.visibility
	)
	
	g_vis = texture_append_visibility(g_vis, TC_Ks, { 'useior': False })
	g_vis = texture_append_visibility(g_vis, TF_index, { 'useior': True })
	
	return g_vis
	
class luxrender_mat_glossy(declarative_property_group):
	
	controls = [
		'multibounce'
	] + \
		TC_Kd.controls + \
		TF_d.controls + \
		TC_Ka.controls + \
	[
		'useior'
	] + \
		TF_index.controls + \
		TC_Ks.controls + \
		TF_uroughness.controls + \
		TF_vroughness.controls
	
	visibility = glossy_visibility()
	
	properties = [
		{
			'type': 'bool',
			'attr': 'multibounce',
			'name': 'Multibounce',
			'description': 'Enable surface layer multi-bounce',
			'default': False,
			'save_in_preset': True
		},
		{
			'type': 'bool',
			'attr': 'useior',
			'name': 'Use IOR',
			'description': 'Use IOR/Reflective index input',
			'default': False,
			'save_in_preset': True
		}
	] + \
		TF_d.properties + \
		TF_index.properties + \
		TC_Ka.properties + \
		TC_Kd.properties + \
		TC_Ks.properties + \
		TF_uroughness.properties + \
		TF_vroughness.properties
	
	def get_paramset(self, scene):
		glossy_params = ParamSet()
		
		glossy_params.add_bool('multibounce', self.multibounce)
		
		if self.d_floatvalue > 0:
			glossy_params.update( TF_d.get_paramset(self) )
			glossy_params.update( TC_Ka.get_paramset(self) )
		
		glossy_params.update( TC_Kd.get_paramset(self) )
		
		if self.useior:
			glossy_params.update( TF_index.get_paramset(self) )
			glossy_params.add_color('Ks', (1.0, 1.0, 1.0))
		else:
			glossy_params.update( TC_Ks.get_paramset(self) )
			glossy_params.add_float('index', 0.0)
			
		glossy_params.update( TF_uroughness.get_paramset(self) )
		glossy_params.update( TF_vroughness.get_paramset(self) )
		
		return glossy_params

def glossy_lossy_visibility():
	gl_vis = dict_merge(
		TF_d.visibility,
		TF_index.visibility,
		TC_Ka.visibility,
		TC_Kd.visibility,
		TC_Ks.visibility,
		TF_uroughness.visibility,
		TF_vroughness.visibility
	)
	
	gl_vis = texture_append_visibility(gl_vis, TC_Ks, { 'useior': False })
	gl_vis = texture_append_visibility(gl_vis, TF_index, { 'useior': True })
	
	return gl_vis

class luxrender_mat_glossy_lossy(declarative_property_group):
	
	controls = [
	] + \
		TC_Kd.controls + \
		TF_d.controls + \
		TC_Ka.controls + \
	[
		'useior'
	] + \
		TF_index.controls + \
		TC_Ks.controls + \
		TF_uroughness.controls + \
		TF_vroughness.controls
	
	visibility = glossy_lossy_visibility()
	
	properties = [
		{
			'type': 'bool',
			'attr': 'useior',
			'name': 'Use IOR',
			'description': 'Use IOR/Reflective index input',
			'default': False,
			'save_in_preset': True
		}
	] + \
		TC_Kd.properties + \
		TF_d.properties + \
		TC_Ka.properties + \
		TF_index.properties + \
		TC_Ks.properties + \
		TF_uroughness.properties + \
		TF_vroughness.properties
	
	def get_paramset(self, scene):
		glossy_lossy_params = ParamSet()
		
		if self.d_floatvalue > 0:
			glossy_lossy_params.update( TF_d.get_paramset(self) )
			glossy_lossy_params.update( TC_Ka.get_paramset(self) )
		
		glossy_lossy_params.update( TC_Kd.get_paramset(self) )
		
		if self.useior:
			glossy_lossy_params.update( TF_index.get_paramset(self) )
			glossy_lossy_params.add_color('Ks', (1.0, 1.0, 1.0))
		else:
			glossy_lossy_params.update( TC_Ks.get_paramset(self) )
			glossy_lossy_params.add_float('index', 0.0)
			
		glossy_lossy_params.update( TF_uroughness.get_paramset(self) )
		glossy_lossy_params.update( TF_vroughness.get_paramset(self) )
		
		return glossy_lossy_params

class luxrender_mat_matte(declarative_property_group):
	
	controls = [
	] + \
		TC_Kd.controls + \
		TF_sigma.controls
	
	visibility = dict_merge(
		TC_Kd.visibility,
		TF_sigma.visibility
	)
	
	properties = [
	] + \
		TC_Kd.properties + \
		TF_sigma.properties
	
	def get_paramset(self, scene):
		matte_params = ParamSet()
		
		matte_params.update( TC_Kd.get_paramset(self) )
		matte_params.update( TF_sigma.get_paramset(self) )
		
		return matte_params
	
class luxrender_mat_mattetranslucent(declarative_property_group):
	
	controls = [
		'energyconserving'
	] + \
		TC_Kr.controls + \
		TC_Kt.controls + \
		TF_sigma.controls
	
	visibility = dict_merge(
		TC_Kr.visibility,
		TC_Kt.visibility,
		TF_sigma.visibility
	)
	
	properties = [
		{
			'type': 'bool',
			'attr': 'energyconserving',
			'name': 'Energy conserving',
			'description': 'Force energy conservation with regards to reflection and transmission',
			'default': False
		},
	] + \
		TC_Kr.properties + \
		TC_Kt.properties + \
		TF_sigma.properties
	
	def get_paramset(self, scene):
		mattetranslucent_params = ParamSet()
		
		mattetranslucent_params.add_bool('energyconserving', self.energyconserving)
		
		mattetranslucent_params.update( TC_Kr.get_paramset(self) )
		mattetranslucent_params.update( TC_Kt.get_paramset(self) )
		mattetranslucent_params.update( TF_sigma.get_paramset(self) )
		
		return mattetranslucent_params

def glossytranslucent_visibility():
	gt_vis = dict_merge(
		TC_Kt.visibility,
		TC_Kd.visibility,
		TF_d.visibility,
		TC_Ka.visibility,
		TF_index.visibility,
		TC_Ks.visibility,
		TF_uroughness.visibility,
		TF_vroughness.visibility,
		
		TF_backface_d.visibility,
		TC_backface_Ka.visibility,
		TC_backface_Kd.visibility,
		TF_backface_index.visibility,
		TC_backface_Ks.visibility,
		TF_backface_uroughness.visibility,
		TF_backface_vroughness.visibility,
		{
			'backface_multibounce':	{ 'two_sided': True },
			'bf_useior': 			{ 'two_sided': True }
		}
	)
	
	gt_vis = texture_append_visibility(gt_vis, TC_Ks,					{ 'useior': False })
	gt_vis = texture_append_visibility(gt_vis, TF_index,				{ 'useior': True  })
	
	gt_vis = texture_append_visibility(gt_vis, TC_backface_Ka,			{ 'two_sided': True })
	gt_vis = texture_append_visibility(gt_vis, TC_backface_Kd,			{ 'two_sided': True })
	gt_vis = texture_append_visibility(gt_vis, TF_backface_d,			{ 'two_sided': True })
	gt_vis = texture_append_visibility(gt_vis, TF_backface_uroughness,	{ 'two_sided': True })
	gt_vis = texture_append_visibility(gt_vis, TF_backface_vroughness,	{ 'two_sided': True })

	gt_vis = texture_append_visibility(gt_vis, TC_backface_Ks,			{ 'two_sided': True, 'bf_useior': False })
	gt_vis = texture_append_visibility(gt_vis, TF_backface_index,		{ 'two_sided': True, 'bf_useior': True  })
	
	return gt_vis

class luxrender_mat_glossytranslucent(declarative_property_group):
	
	controls = [
		'multibounce',
	] + \
		TC_Kt.controls + \
		TC_Kd.controls + \
		TF_d.controls + \
		TC_Ka.controls + \
	[
		'useior'
	] + \
		TF_index.controls + \
		TC_Ks.controls + \
		TF_uroughness.controls + \
		TF_vroughness.controls + \
	[
		'two_sided',
		'backface_multibounce',
	] + \
		TF_backface_d.controls + \
		TC_backface_Ka.controls + \
	[
		'bf_useior'
	] + \
		TF_backface_index.controls + \
		TC_backface_Ks.controls + \
		TF_backface_uroughness.controls + \
		TF_backface_vroughness.controls
	
	visibility = glossytranslucent_visibility()
	
	properties = [
		{
			'type': 'bool',
			'attr': 'multibounce',
			'name': 'Multibounce',
			'description': 'Enable surface layer multi-bounce',
			'default': False,
			'save_in_preset': True
		},
		{
			'type': 'bool',
			'attr': 'two_sided',
			'name': 'Two sided',
			'description': 'Different surface properties for back-face and front-face',
			'default': False,
			'save_in_preset': True
		},
		{
			'type': 'bool',
			'attr': 'backface_multibounce',
			'name': 'Backface Multibounce',
			'description': 'Enable back-surface layer multi-bounce',
			'default': False,
			'save_in_preset': True
		},
		{
			'type': 'bool',
			'attr': 'useior',
			'name': 'Use IOR',
			'description': 'Use IOR/Reflective index input',
			'default': False,
			'save_in_preset': True
		},
		{
			'type': 'bool',
			'attr': 'bf_useior',
			'name': 'Backface use IOR',
			'description': 'Use IOR/Reflective index input',
			'default': False,
			'save_in_preset': True
		}
	] + \
		TC_Kt.properties + \
		TC_Kd.properties + \
		TF_d.properties + \
		TC_Ka.properties + \
		TF_index.properties + \
		TC_Ks.properties + \
		TF_uroughness.properties + \
		TF_vroughness.properties + \
		TF_backface_d.properties + \
		TC_backface_Ka.properties + \
		TF_backface_index.properties + \
		TC_backface_Ks.properties + \
		TF_backface_uroughness.properties + \
		TF_backface_vroughness.properties
		
	def get_paramset(self, scene):
		glossytranslucent_params = ParamSet()
		
		if self.d_floatvalue > 0:
			glossytranslucent_params.update( TF_d.get_paramset(self) )
			glossytranslucent_params.update( TC_Ka.get_paramset(self) )
		
		glossytranslucent_params.add_bool('onesided', not self.two_sided)
		glossytranslucent_params.add_bool('multibounce', self.multibounce)
		
		glossytranslucent_params.update( TC_Kt.get_paramset(self) )
		glossytranslucent_params.update( TC_Kd.get_paramset(self) )
		
		if self.useior:
			glossytranslucent_params.update( TF_index.get_paramset(self) )
			glossytranslucent_params.add_color('Ks', (1.0, 1.0, 1.0))
		else:
			glossytranslucent_params.update( TC_Ks.get_paramset(self) )
			glossytranslucent_params.add_float('index', 0.0)
			
		glossytranslucent_params.update( TF_uroughness.get_paramset(self) )
		glossytranslucent_params.update( TF_vroughness.get_paramset(self) )
		
		if self.two_sided:
			glossytranslucent_params.add_bool('backface_multibounce', self.backface_multibounce)
			
			if self.bf_d_floatvalue > 0:
				glossytranslucent_params.update( TF_backface_d.get_paramset(self) )
				glossytranslucent_params.update( TC_backface_Ka.get_paramset(self) )
			
			if self.bf_useior:
				glossytranslucent_params.update( TF_backface_index.get_paramset(self) )
				glossytranslucent_params.add_color('backface_Ks', (1.0, 1.0, 1.0))
			else:
				glossytranslucent_params.update( TC_backface_Ks.get_paramset(self) )
				glossytranslucent_params.add_float('backface_index', 0.0)
			
			glossytranslucent_params.update( TF_backface_uroughness.get_paramset(self) )
			glossytranslucent_params.update( TF_backface_vroughness.get_paramset(self) )
		
		return glossytranslucent_params

class luxrender_mat_metal(declarative_property_group):
	
	controls = [
		'name',
		'filename',
	] + \
		TF_uroughness.controls + \
		TF_vroughness.controls
	
	visibility = dict_merge({
			'filename':	{ 'name': 'nk' }
		},
		TF_uroughness.visibility,
		TF_vroughness.visibility
	)
	
	properties = [
		{
			'type': 'enum',
			'attr': 'name',
			'name': 'Preset',
			'items': [
				('nk', 'Use nk File', 'nk'),
				('amorphous carbon', 'amorphous carbon', 'amorphous carbon'),
				('copper', 'copper', 'copper'),
				('gold', 'gold', 'gold'),
				('silver', 'silver', 'silver'),
				('aluminium', 'aluminium', 'aluminium')
			],
			'save_in_preset': True
		},
		{
			'type': 'string',
			'subtype': 'FILE_PATH',
			'attr': 'filename',
			'name': 'NK file',
			'save_in_preset': True
		},
	] + \
		TF_uroughness.properties + \
		TF_vroughness.properties
	
	def get_paramset(self, scene):
		metal_params = ParamSet()
		
		metal_params.update( TF_uroughness.get_paramset(self) )
		metal_params.update( TF_vroughness.get_paramset(self) )
		
		if self.name == 'nk':	# use an NK data file
			metal_params.add_string('filename', efutil.path_relative_to_export(self.filename) )
		else:					# use a preset name
			metal_params.add_string('name', self.name)
		
		return metal_params

class luxrender_mat_shinymetal(declarative_property_group):
	
	controls = [
	] + \
		TF_film.controls + \
		TF_filmindex.controls + \
		TC_Kr.controls + \
		TC_Ks.controls + \
		TF_uroughness.controls + \
		TF_vroughness.controls
	
	visibility = dict_merge(
		TF_film.visibility,
		TF_filmindex.visibility,
		TC_Kr.visibility,
		TC_Ks.visibility,
		TF_uroughness.visibility,
		TF_vroughness.visibility
	)
	
	properties = [
	] + \
		TF_film.properties + \
		TF_filmindex.properties + \
		TC_Kr.properties + \
		TC_Ks.properties + \
		TF_uroughness.properties + \
		TF_vroughness.properties
	
	def get_paramset(self, scene):
		shinymetal_params = ParamSet()
		
		shinymetal_params.update( TF_film.get_paramset(self) )
		shinymetal_params.update( TF_filmindex.get_paramset(self) )
		shinymetal_params.update( TC_Kr.get_paramset(self) )
		shinymetal_params.update( TC_Ks.get_paramset(self) )
		shinymetal_params.update( TF_uroughness.get_paramset(self) )
		shinymetal_params.update( TF_vroughness.get_paramset(self) )
		
		return shinymetal_params

class luxrender_mat_mirror(declarative_property_group):
	
	controls = [
	] + \
		TF_film.controls + \
		TF_filmindex.controls + \
		TC_Kr.controls
	
	visibility = dict_merge(
		TF_film.visibility,
		TF_filmindex.visibility,
		TC_Kr.visibility
	)
	
	properties = [
	] + \
		TF_film.properties + \
		TF_filmindex.properties + \
		TC_Kr.properties
	
	def get_paramset(self, scene):
		mirror_params = ParamSet()
		
		mirror_params.update( TF_film.get_paramset(self) )
		mirror_params.update( TF_filmindex.get_paramset(self) )
		mirror_params.update( TC_Kr.get_paramset(self) )
		
		return mirror_params

class luxrender_mat_mix(declarative_property_group):
	
	controls = [
		'namedmaterial1',
		'namedmaterial2',
	] + \
		TF_amount.controls
	
	visibility = TF_amount.visibility
	
	properties = [
	] + \
		TF_amount.properties + \
		MaterialParameter('namedmaterial1', 'Material 1', 'luxrender_mat_mix') + \
		MaterialParameter('namedmaterial2', 'Material 2', 'luxrender_mat_mix')
	
	def get_paramset(self, scene):
		mix_params = ParamSet()
		
		mix_params.add_string('namedmaterial1', self.namedmaterial1_material)
		mix_params.add_string('namedmaterial2', self.namedmaterial2_material)
		mix_params.update( TF_amount.get_paramset(self) )
		
		return mix_params

class luxrender_mat_null(declarative_property_group):
	
	controls = [
	]
	
	visibility = {
	}
	
	properties = [
	]
	
	def get_paramset(self, scene):
		return ParamSet()

class luxrender_mat_velvet(declarative_property_group):
	
	controls = TC_Kd.controls + [
		'thickness',
		'advanced',
		'p1', 'p2', 'p3',
	]
	
	visibility = dict_merge({
		'p1':	{ 'advanced': True },
		'p2':	{ 'advanced': True },
		'p3':	{ 'advanced': True },
	}, TC_Kd.visibility)
	
	properties = TC_Kd.properties + [
		{
			'type': 'bool',
			'attr': 'advanced',
			'name': 'Advanced',
			'default': False,
			'save_in_preset': True
		},
		{
			'type': 'float',
			'attr': 'thickness',
			'name': 'Thickness',
			'default': 0.1,
			'min': 0.0,
			'soft_min': 0.0,
			'max': 1.0,
			'soft_max': 1.0,
			'save_in_preset': True
		},
		{
			'type': 'float',
			'attr': 'p1',
			'name': 'p1',
			'default': -2.0,
			'min': -100.0,
			'soft_min': -100.0,
			'max': 100.0,
			'soft_max': 100.0,
			'save_in_preset': True
		},
		{
			'type': 'float',
			'attr': 'p2',
			'name': 'p2',
			'default': 10.0,
			'min': -100.0,
			'soft_min': -100.0,
			'max': 100.0,
			'soft_max': 100.0,
			'save_in_preset': True
		},
		{
			'type': 'float',
			'attr': 'p3',
			'name': 'p3',
			'default': 2.0,
			'min': -100.0,
			'soft_min': -100.0,
			'max': 100.0,
			'soft_max': 100.0,
			'save_in_preset': True
		},
	]
	
	def get_paramset(self, scene):
		velvet_params = ParamSet()
		
		velvet_params.update( TC_Kd.get_paramset(self) )
		
		velvet_params.add_float('thickness', self.thickness)
		if self.advanced:
			velvet_params.add_float('p1', self.p1)
			velvet_params.add_float('p2', self.p2)
			velvet_params.add_float('p3', self.p3)
		
		return velvet_params



class luxrender_volume_data(declarative_property_group):
	'''
	Storage class for LuxRender volume data. The
	luxrender_volumes object will store 1 or more of
	these in its CollectionProperty 'volumes'.
	'''
	
	controls = [
		'type',
	] + \
	TFR_IOR.controls + \
	TC_absorption.controls + \
	[
		'depth'
	]
	
	visibility = {
		'ior_floattexture':			{ 'ior_usefloattexture': True },
		'absorption_colortexture':	{ 'absorption_usecolortexture': True }
	}
	
	properties = [
		{
			'type': 'enum',
			'attr': 'type',
			'name': 'Type',
			'items': [
				('clear', 'clear', 'clear')
			],
			'save_in_preset': True
		},
	] + \
	TFR_IOR.properties + \
	TC_absorption.properties + \
	[
		{
			'type': 'float',
			'attr': 'depth',
			'name': 'Abs. at depth',
			'description': 'Object will match absorption color at this depth in metres',
			'default': 1.0,
			'min': 0.00001,
			'soft_min': 0.00001,
			'max': 1000.0,
			'soft_max': 1000.0,
			'precision': 6,
			'save_in_preset': True
		},
	]
	
	def api_output(self, lux_context):
		vp = ParamSet()
		
		scale = 1
		def absorption_transform(i):
			# This is copied from the old LuxBlend, I don't pretend to understand it, DH
			depthed = (-math.log(max([(float(i)),1e-30]))/(self.depth*scale)) * ((float(i))==1.0 and -1 or 1)
			#print('abs xform: %f -> %f' % (i,depthed))
			return depthed
		
		vp.update( add_texture_parameter(lux_context, 'fresnel', 'fresnel', self) )
		vp.update( add_texture_parameter(lux_context, 'absorption', 'color', self, value_transform=absorption_transform) )
		
		return self.type, vp

class luxrender_volumes(declarative_property_group):
	'''
	Storage class for LuxRender Material volumes.
	This class will be instantiated within a Blender scene
	object.
	'''
	
	controls = [
		'volumes_label',
		'volumes_select',
		['op_vol_add', 'op_vol_rem']
	]
	
	visibility = {}
	
	properties = [
		{
			'type': 'collection',
			'ptype': luxrender_volume_data,
			'name': 'volumes',
			'attr': 'volumes',
			'items': [
				
			]
		},
		{
			'type': 'text',
			'attr': 'volumes_label',
			'name': 'Volumes',
		},
		{
			'type': 'int',
			'name': 'volumes_index',
			'attr': 'volumes_index',
		},
		{
			'type': 'template_list',
			'name': 'volumes_select',
			'attr': 'volumes_select',
			'trg': lambda sc,c: c.luxrender_volumes,
			'trg_attr': 'volumes_index',
			'src': lambda sc,c: c.luxrender_volumes,
			'src_attr': 'volumes',
		},
		{
			'type': 'operator',
			'attr': 'op_vol_add',
			'operator': 'luxrender.volume_add',
			'text': 'Add',
			'icon': 'ZOOMIN',
		},
		{
			'type': 'operator',
			'attr': 'op_vol_rem',
			'operator': 'luxrender.volume_remove',
			'text': 'Remove',
			'icon': 'ZOOMOUT',
		},
	]
