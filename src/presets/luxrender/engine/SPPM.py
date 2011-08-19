# ***** BEGIN GPL LICENSE BLOCK *****
#
# --------------------------------------------------------------------------
# Blender 2.5 LuxRender Add-On
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
bpy.context.scene.luxrender_rendermode.rendermode = 'sppm'
bpy.context.scene.luxrender_rendermode.renderer = 'sppm'
bpy.context.scene.luxrender_engine.fixed_seed = False
bpy.context.scene.luxrender_engine.mesh_type = 'binary_ply'
bpy.context.scene.luxrender_engine.log_verbosity = 'default'
bpy.context.scene.luxrender_sampler.sampler = 'lowdiscrepancy'
bpy.context.scene.luxrender_sampler.advanced = False
bpy.context.scene.luxrender_sampler.largemutationprob = 0.4000000059604645
bpy.context.scene.luxrender_sampler.maxconsecrejects = 512
bpy.context.scene.luxrender_sampler.usevariance = False
bpy.context.scene.luxrender_sampler.basesampler = 'random'
bpy.context.scene.luxrender_sampler.chainlength = 512
bpy.context.scene.luxrender_sampler.mutationrange = 256
bpy.context.scene.luxrender_sampler.pixelsampler = 'linear'
bpy.context.scene.luxrender_sampler.pixelsamples = 2
bpy.context.scene.luxrender_integrator.surfaceintegrator = 'sppm'
bpy.context.scene.luxrender_integrator.advanced = False
bpy.context.scene.luxrender_integrator.lightstrategy = 'auto'
bpy.context.scene.luxrender_integrator.eyedepth = 32
bpy.context.scene.luxrender_integrator.lightdepth = 32
bpy.context.scene.luxrender_integrator.eyerrthreshold = 0.0
bpy.context.scene.luxrender_integrator.lightrrthreshold = 0.0
bpy.context.scene.luxrender_integrator.maxdepth = 48
bpy.context.scene.luxrender_integrator.directsampleall = True
bpy.context.scene.luxrender_integrator.directsamples = 1
bpy.context.scene.luxrender_integrator.directdiffuse = True
bpy.context.scene.luxrender_integrator.directglossy = True
bpy.context.scene.luxrender_integrator.indirectsampleall = False
bpy.context.scene.luxrender_integrator.indirectsamples = 1
bpy.context.scene.luxrender_integrator.indirectdiffuse = True
bpy.context.scene.luxrender_integrator.indirectglossy = True
bpy.context.scene.luxrender_integrator.diffusereflectdepth = 3
bpy.context.scene.luxrender_integrator.diffusereflectsamples = 1
bpy.context.scene.luxrender_integrator.diffuserefractdepth = 5
bpy.context.scene.luxrender_integrator.diffuserefractsamples = 1
bpy.context.scene.luxrender_integrator.glossyreflectdepth = 2
bpy.context.scene.luxrender_integrator.glossyreflectsamples = 1
bpy.context.scene.luxrender_integrator.glossyrefractdepth = 5
bpy.context.scene.luxrender_integrator.glossyrefractsamples = 1
bpy.context.scene.luxrender_integrator.specularreflectdepth = 3
bpy.context.scene.luxrender_integrator.specularrefractdepth = 5
bpy.context.scene.luxrender_integrator.diffusereflectreject = False
bpy.context.scene.luxrender_integrator.diffusereflectreject_threshold = 10.0
bpy.context.scene.luxrender_integrator.diffuserefractreject = False
bpy.context.scene.luxrender_integrator.diffuserefractreject_threshold = 10.0
bpy.context.scene.luxrender_integrator.glossyreflectreject = False
bpy.context.scene.luxrender_integrator.glossyreflectreject_threshold = 10.0
bpy.context.scene.luxrender_integrator.glossyrefractreject = False
bpy.context.scene.luxrender_integrator.glossyrefractreject_threshold = 10.0
bpy.context.scene.luxrender_integrator.maxphotondepth = 48
bpy.context.scene.luxrender_integrator.directphotons = 1000000
bpy.context.scene.luxrender_integrator.causticphotons = 0
bpy.context.scene.luxrender_integrator.indirectphotons = 640000
bpy.context.scene.luxrender_integrator.radiancephotons = 640000
bpy.context.scene.luxrender_integrator.nphotonsused = 50
bpy.context.scene.luxrender_integrator.maxphotondist = 0.15000000596046448
bpy.context.scene.luxrender_integrator.finalgather = True
bpy.context.scene.luxrender_integrator.finalgathersamples = 32
bpy.context.scene.luxrender_integrator.gatherangle = 5.0
bpy.context.scene.luxrender_integrator.renderingmode = 'directlighting'
bpy.context.scene.luxrender_integrator.distancethreshold = 0.75
bpy.context.scene.luxrender_integrator.photonmapsfile = ''
bpy.context.scene.luxrender_integrator.dbg_enabledirect = True
bpy.context.scene.luxrender_integrator.dbg_enableradiancemap = False
bpy.context.scene.luxrender_integrator.dbg_enableindircaustic = True
bpy.context.scene.luxrender_integrator.dbg_enableindirdiffuse = True
bpy.context.scene.luxrender_integrator.dbg_enableindirspecular = True
bpy.context.scene.luxrender_integrator.nsets = 4
bpy.context.scene.luxrender_integrator.nlights = 64
bpy.context.scene.luxrender_integrator.mindist = 0.10000000149011612
bpy.context.scene.luxrender_integrator.rrcontinueprob = 0.6499999761581421
bpy.context.scene.luxrender_integrator.rrstrategy = 'efficiency'
bpy.context.scene.luxrender_integrator.includeenvironment = True
bpy.context.scene.luxrender_integrator.maxeyedepth = 48
bpy.context.scene.luxrender_integrator.photonperpass = 1000000
bpy.context.scene.luxrender_integrator.startradius = 2.0
bpy.context.scene.luxrender_integrator.alpha = 0.699999988079071
bpy.context.scene.luxrender_integrator.lookupaccel = 'hybridhashgrid'
bpy.context.scene.luxrender_volumeintegrator.volumeintegrator = 'multi'
bpy.context.scene.luxrender_volumeintegrator.stepsize = 1.0
bpy.context.scene.luxrender_filter.filter = 'mitchell'
bpy.context.scene.luxrender_filter.advanced = False
bpy.context.scene.luxrender_filter.xwidth = 2.0
bpy.context.scene.luxrender_filter.ywidth = 2.0
bpy.context.scene.luxrender_filter.alpha = 2.0
bpy.context.scene.luxrender_filter.b = 0.3333333432674408
bpy.context.scene.luxrender_filter.c = 0.3333333432674408
bpy.context.scene.luxrender_filter.supersample = True
bpy.context.scene.luxrender_filter.tau = 3.0
bpy.context.scene.luxrender_accelerator.accelerator = 'qbvh'
bpy.context.scene.luxrender_accelerator.advanced = False
bpy.context.scene.luxrender_accelerator.intersectcost = 80
bpy.context.scene.luxrender_accelerator.traversalcost = 1
bpy.context.scene.luxrender_accelerator.emptybonus = 0.20000000298023224
bpy.context.scene.luxrender_accelerator.treetype = '2'
bpy.context.scene.luxrender_accelerator.costsample = 0
bpy.context.scene.luxrender_accelerator.maxprims = 1
bpy.context.scene.luxrender_accelerator.maxdepth = -1
bpy.context.scene.luxrender_accelerator.refineimmediately = False
bpy.context.scene.luxrender_accelerator.maxprimsperleaf = 4
bpy.context.scene.luxrender_accelerator.fullsweepthreshold = 16
bpy.context.scene.luxrender_accelerator.skipfactor = 1
