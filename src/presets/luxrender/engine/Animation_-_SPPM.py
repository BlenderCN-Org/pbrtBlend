# ***** BEGIN GPL LICENSE BLOCK *****
#
# --------------------------------------------------------------------------
# Blender 2.5 PBRTv3 Add-On
# --------------------------------------------------------------------------
#
# This preset file was generated by LuxBlend25 and modified by Jason Clarke
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
bpy.context.scene.pbrtv3_engine.export_type = 'INT'
bpy.context.scene.pbrtv3_rendermode.rendermode = 'sppm'
bpy.context.scene.pbrtv3_rendermode.renderer = 'sppm'
bpy.context.scene.pbrtv3_engine.write_files = True
bpy.context.scene.pbrtv3_engine.fixed_seed = True
bpy.context.scene.pbrtv3_halt.haltspp = 150
bpy.context.scene.pbrtv3_integrator.surfaceintegrator = 'sppm'
bpy.context.scene.pbrtv3_integrator.maxphotondepth = 24
bpy.context.scene.pbrtv3_integrator.maxeyedepth = 8
bpy.context.scene.pbrtv3_integrator.startradius = 3.0
bpy.context.scene.pbrtv3_integrator.alpha = 1.0
bpy.context.scene.pbrtv3_integrator.photonperpass = 2000000
bpy.context.scene.pbrtv3_accelerator.accelerator = 'bvh'
bpy.context.scene.pbrtv3_accelerator.advanced = False
bpy.context.scene.pbrtv3_accelerator.intersectcost = 80
bpy.context.scene.pbrtv3_accelerator.traversalcost = 1
bpy.context.scene.pbrtv3_accelerator.emptybonus = 0.20000000298023224
bpy.context.scene.pbrtv3_accelerator.treetype = '2'
bpy.context.scene.pbrtv3_accelerator.costsample = 0
bpy.context.scene.pbrtv3_accelerator.maxprims = 1
bpy.context.scene.pbrtv3_accelerator.maxdepth = -1
bpy.context.scene.pbrtv3_accelerator.refineimmediately = False
bpy.context.scene.pbrtv3_accelerator.maxprimsperleaf = 4
bpy.context.scene.pbrtv3_accelerator.fullsweepthreshold = 16
bpy.context.scene.pbrtv3_accelerator.skipfactor = 1
