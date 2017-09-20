#  2015 - 2017 Nicolas Priniotakis (Nikos) - nikos@easy-logging.net


# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {
	"name": "Vray HDRI-lighting-Shortcut",
	"author": "Nicolas Priniotakis (Nikos), fixed for Vray: JuhaW",
	"version": (1, 3, 2, 2),
	"blender": (2, 7, 8, 0),
	"api": 44539,
	"category": "Material",
	"location": "Properties > World",
	"description": "Easy setup for HDRI global lightings",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "", }

### IMPORTS & VARIABLES ---------------------------------------------
import bpy
import os
from bpy.types import Operator, AddonPreferences
from math import radians, degrees
global nodes, folder_path, pref, img_path, adjustments
global node_coo, node_map, node_rgb, node_add, node_sat, node_env, node_math, node_math_add
global node_bkgnd, node_out, node_light_path, node_rflx_math, node_rflx_math_add
adjustments = False
img_path = None

### FUNCTIONS ------------------------------------------------------
def img_exists(img):
	for index, i in enumerate(bpy.data.images):
		if i.name == img:
			return True
	return False


def img_index(img):
	for index, i in enumerate(bpy.data.images):
		if i.name == img:
			return index
	return None


def current_bkgnd():
	nodes = bpy.context.scene.world.node_tree.nodes
	for node in nodes:
		if node.name == "ENVIRONMENT":
			return node.image.name


def node_exists(n):
	nodes = bpy.context.scene.world.node_tree.nodes
	for node in nodes:
		if node.name == n:
			return True
	return False


# -------------------------------------------------------------
# Assign each node to a variable
# -------------------------------------------------------------
def node_attrib():
	global node_coo, node_map, node_rgb, node_add, node_sat, node_env, node_math
	global node_math_add, node_bkgnd, node_out, node_light_path, node_reflexion
	global node_rflx_math, node_rflx_math_add, node_blur_noise, node_blur_coordinate
	global node_blur_mix_1, node_blur_mix_2, node_blur_math_sub, node_blur_math_add

	nodes = bpy.context.scene.world.node_tree.nodes
	try:
		for node in nodes:
			if node.name == 'COORDINATE':
				node_coo = node
			if node.name == 'MAPPING':
				node_map = node
			if node.name == 'COMBINE':
				node_rgb = node
			if node.name == 'RGB_ADD':
				node_add = node
			if node.name == 'SATURATION':
				node_sat = node
			if node.name == 'ENVIRONMENT':
				node_env = node
			if node.name == 'HLS_MATH':
				node_math = node
			if node.name == 'HLS_MATH_ADD':
				node_math_add = node
			if node.name == 'BACKGROUND':
				node_bkgnd = node
			if node.name == 'OUTPUT':
				node_out = node
			if node.name == "LIGHT_PATH":
				node_light_path = node
			if node.name == 'REFLEXION':
				node_reflexion = node
			if node.name == "RFLX_MATH":
				node_rflx_math = node
			if node.name == "RFLX_MATH_ADD":
				node_rflx_math_add = node
			if node.name == "BLUR_NOISE":
				node_blur_noise = node
			if node.name == "BLUR_COORDINATE":
				node_blur_coordinate = node
			if node.name == "BLUR_MIX_1":
				node_blur_mix_1 = node
			if node.name == "BLUR_MIX_2":
				node_blur_mix_2 = node
			if node.name == "BLUR_MATH_ADD":
				node_blur_math_add = node
			if node.name == "BLUR_MATH_SUB":
				node_blur_math_sub = node
	except:
		pass


# -------------------------------------------------------------
# Check if the node tree has been modified by user
#
# True: if the node tree is inaltered or compliant with the UI
# False: The node tree is not compatible with the UI
# -------------------------------------------------------------
def node_tree_ok():
	try:
		current_world = bpy.context.scene.world
		if current_world.name == "HDRI Lighting Shortcut":
			if node_exists("COORDINATE"):
				if node_exists("MAPPING"):
					if node_exists("COMBINE"):
						if node_exists("RGB_ADD"):
							if node_exists("SATURATION"):
								if node_exists("ENVIRONMENT"):
									if node_exists("BACKGROUND"):
										if node_exists("LIGHT_PATH"):
											if node_exists('REFLEXION'):
												if node_exists('RFLX_MATH'):
													if node_exists('RFLX_MATH_ADD'):
														if node_exists('HLS_MATH'):
															if node_exists('HLS_MATH_ADD'):
																if node_exists('REF_MIX'):
																	if node_exists('BLUR_NOISE'):
																		if node_exists('BLUR_COORDINATE'):
																			if node_exists('BLUR_MIX_1'):
																				if node_exists('BLUR_MIX_2'):
																					if node_exists('BLUR_MATH_ADD'):
																						if node_exists('BLUR_MATH_SUB'):
																							if node_exists("OUTPUT"):
																								node_attrib()
																								return True
	except:
		pass
	return False


# -------------------------------------------------------------
# Functions that update the nodes's settings
# -------------------------------------------------------------
def update_mirror(self, context):
	global node_env
	
	image_node = hemi_lamp_imagenode_find()

	try:
		if self.mirror:
			node_env.projection = 'MIRROR_BALL'
			image_node.UVWGenEnvironment.mapping_type = 'mirror_ball'
			
		else:
			node_env.projection = 'EQUIRECTANGULAR'
			image_node.UVWGenEnvironment.mapping_type = 'spherical'
	except:
		pass


def update_orientation(self, context):
	#try:
	node_map.rotation[2] = self.orientation
	ori = degrees(self.orientation)
	
	if ori < 180:
		ori = -180 - ori
	else:
		ori = 180-ori
	
	bpy.context.scene.objects['Hemi'].rotation_euler[2] = radians(ori)
	#print (ori)
	#set sun constraint offset
	#set sun offset only if sun & Hdri are synced
	if context.scene.vray_sun_synced:
		sun_offset()
		
	"""	
	except:
		print ("pass orientation")
		pass
	"""

#############################################################################
class Vray():

	sun_orientation_x = 0
	sun_orientation_z = 0
	#sun constraint follow path
	sun_constraint = 0
	sun_synced = False
	offset = 0
	hdri_orientation = 0
	sun_button_setmode = False
	
	#value 0-1
	uvcursor_x = 0
	uvcursor_y = 0
	
	area = None
	area_image = None
	
class OBJECT_OT_sun_set_cursor(bpy.types.Operator):
	bl_label = "sun set cursor"
	bl_idname = "sun_set_cursor.execute"
	bl_description = "Sun is shining and moon is rising"
	#bl_options = {'REGISTER'}
	
	
	def modal(self, context, event):
		if event.type == 'MOUSEMOVE':
			pass
		elif event.type == 'LEFTMOUSE':
			# we could handle PRESS and RELEASE individually if necessary
			pass

		elif event.type in {'RIGHTMOUSE', 'ESC'}:
			
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		
		
		Vray.sun_button_setmode = not Vray.sun_button_setmode
		if Vray.sun_button_setmode:
			#print ("Vray.sun_button_setmode:", Vray.sun_button_setmode)
			
			#set background image from image node
			for area in bpy.context.screen.areas:
				if area.type == 'VIEW_3D':
					space_data = area.spaces.active
					Vray.area = area
					Vray.spaces = area.spaces.active
					#bpy.context.window.cursor_set("EYEDROPPER")
					
					#image node
					image_node = hemi_lamp_imagenode_find()
					if image_node:
							
						area.type= 'IMAGE_EDITOR'
						Vray.area_image = area
						area.spaces.active.image = image_node.texture.image
						area.spaces.active.mode = 'MASK'
						mask = bpy.data.masks.get("Set sun position", None)
						if not mask:
							mask = bpy.data.masks.new("Set sun position")
						area.spaces.active.mask = mask
					
					for region in area.regions:
						if region.type == 'WINDOW':
							override = {'area': area, 'region': region}
							bpy.ops.image.view_all(override, fit_view=True)
					
					
			#context.window_manager.modal_handler_add(self)
		else:
			#sun position is set, now calculate sun rotation
			#restore VIEW_3D area
			
			Vray.uvcursor_x = Vray.area_image.spaces.active.cursor_location.x / Vray.area_image.spaces.active.image.size[0]
			Vray.uvcursor_y = Vray.area_image.spaces.active.cursor_location.y / Vray.area_image.spaces.active.image.size[1]
			
			#print ("uvcursor x:", Vray.uvcursor_x)
			#print ("uvcursor y:", Vray.uvcursor_y)
			
			Vray.area.type = 'VIEW_3D'
			sun()
			context.scene.vray_sun_synced = True
			Vray.sun_synced = True
			
		return {'RUNNING_MODAL'}
		"""
		else:
			self.report({'WARNING'}, "No active object, could not finish")
			return {'CANCELLED'}
		"""
			
	def execute(self, context):
		
		
		
		
		
		return {'FINISHED'}
	
class OBJECT_OT_sun(bpy.types.Operator):
	bl_label = "sun"
	bl_idname = "sun.execute"
	bl_description = "Sun is shining and moon is rising"
	#bl_options = {'REGISTER'}

	
	def execute(self, context):
		
		#print ("context:",context.area.type)
		sun()
		#print ("Vray:", Vray.hdri_orientation)
		#Vray.hdri_orientation += 1
		
		return {'FINISHED'}


def sun():

	global img_path
	
	#x
	curx = Vray.uvcursor_x
	posx = curx-0.25
	
	#z
	curz = Vray.uvcursor_y
	posz = curz

	#print ("posx:", posx)
	#print (posz)
	
	Vray.sun_orientation_z = -posx/(1/360)#-orientation
	Vray.sun_orientation_x = posz/(1/180)
	#print ("anglez:", Vray.sun_orientation_z)
	#print ("anglex:", Vray.sun_orientation_x)
	#create circle bezier curve for sun
	curve = bpy.data.objects.get('Sun path', None)
	if not curve:
		curve_create('CURVE', 'Sun path', (0,0,0))
	
	sun = bpy.data.objects.get('Sun', None)
	if not sun:
		sun = lamp_create('SUN', 'Sun', (0,0,4))
		sun.data.vray.direct_type = 'SUN'
	
	sun.rotation_euler.x = radians(Vray.sun_orientation_x)
	sun.scale.z = -1
	
	if 'Sun path' in sun.constraints:
		c = sun.constraints['Sun path']
	else:
		c = sun.constraints.new('FOLLOW_PATH')
		c.name = "Sun path"
	#store sun constraint
	Vray.sun_constraint = c
	
	c.forward_axis = 'FORWARD_X'
	c.up_axis = 'UP_Z'
	c.use_fixed_location = True
	c.use_curve_follow = True
	c.target = bpy.data.objects["Sun path"]

	sun_offset()
	
def sun_offset():
	
	sun_z= Vray.sun_orientation_z - degrees(bpy.context.scene.orientation)
	if sun_z >180:
		Vray.offset = 2-(sun_z/360+.5)
	elif sun_z >=-180:
		Vray.offset = 1-(sun_z/360+.5)
		#<180
	else:
		#print ("degree smaller than -180:")
		Vray.offset = 0-(sun_z/360+.5)
	
	#print ("sun_z:",sun_z)
	c = Vray.sun_constraint
	c.offset_factor = Vray.offset
	#print ("offset:",Vray.offset)


def lamp_create(type, name, coordinates):
	
	od = bpy.data.lamps.new(name, type)
	o = bpy.data.objects.new(name, od)
	o.location =  coordinates
	bpy.context.scene.objects.link(o)	
	return o

def curve_create(type, name, coordinates):
	
	# sample data
	coords = [(-5,0,0), (0,5,0), (5,0,0),(0,-5,0)]

	# create the Curve Datablock
	od = bpy.data.curves.new(name, type=type)
	#curveData.dimensions = '3D'
	od.resolution_u = 32
	od.fill_mode = 'NONE'
	
	# map coords to spline
	polyline = od.splines.new('BEZIER')
	polyline.use_cyclic_u = True
	polyline.bezier_points.add(len(coords)-1)
	for i, coord in enumerate(coords):
		polyline.bezier_points[i].co = coord
		polyline.bezier_points[i].handle_right_type = 'AUTO'
		polyline.bezier_points[i].handle_left_type = 'AUTO'

	# create Object
	o = bpy.data.objects.new(name, od)
	o.hide = True
	o.hide_render = True


	o.location =  coordinates
	bpy.context.scene.objects.link(o)
	
	return o


#check if hemi lamp exist
def hemi_lamp_find():
	
	for o in bpy.context.scene.objects:
		if o.type =='LAMP' and o.data.type =='HEMI':
			return o
	#not find hemi lamp, create new
	o = lamp_create('HEMI', 'Hemi', (0,0,5))
	
	return o
	
 
def hemi_lamp_nodetree_create(o, img): 

	nt = o.data.vray.ntree
	#create if not exist
	ng = bpy.data.node_groups.new('Hemi', type = 'VRayNodeTreeLight') if not nt else nt
	o.data.vray.ntree = ng
	ng.nodes.clear()
	n_dome = ng.nodes.new("VRayNodeLightDome")
	n_image = ng.nodes.new("VRayNodeMetaImageTexture")
	n_image.location.x -= 200
	n_image.texture.image = img
	n_image.mapping_type = 'ENVIRONMENT'
	n_image.UVWGenEnvironment.mapping_type = 'spherical'
	#HDRI colorspace to Linear
	n_image.BitmapBuffer.color_space = '0'
	
	ng.links.new(n_dome.inputs['Dome Tex'], n_image.outputs['Output'])
	 
def hemi_lamp_imagenode_find():
	o = hemi_lamp_find()
	nt = o.data.vray.ntree
	for node in nt.nodes:
		if node.bl_idname == 'VRayNodeMetaImageTexture':
			return node
			
	
#############################################################################
	
	
def update_sat(self, context):
	try:
		node_sat.inputs[1].default_value = self.sat
	except:
		pass


def update_hue(self, context):
	try:
		node_sat.inputs[0].default_value = self.hue
	except:
		pass

def update_vray_sun_synced(self, context):
	pass
	
def update_hemi_light_strength(self, context):
	o = hemi_lamp_find()
	o.data.vray.LightDome.intensity = self.hemi_light_strength
	
def update_strength(self, context):
	try:
		node_math_add.inputs[1].default_value = self.light_strength
		if not bpy.context.scene.adjustments_prop:
			node_rflx_math_add.inputs[1].default_value = self.light_strength
			self.reflexion = self.light_strength
		#o = hemi_lamp_find()
		#o.data.vray.LightDome.intensity = self.light_strength
	except:
		pass


def update_main_strength(self, context):
	try:
		node_math.inputs[1].default_value = self.main_light_strength
		
	except:
		pass


def update_visible(self, context):
	
	o = hemi_lamp_find()
	
	if self.visible:
		self.world.cycles_visibility.camera = True
		o.data.vray.LightDome.invisible = False
	else:
		self.world.cycles_visibility.camera = False
		o.data.vray.LightDome.invisible = True
	try:
		self.light_strength += 0  # dirty trick to force the viewport to update
	except:
		pass


def check_visible():
	scene = bpy.context.scene
	cam = scene.world.cycles_visibility
	if scene.visible:
		cam.camera = False
		scene.visible = True
	else:
		cam.camera = True
		scene.visible = False
	try:
		scene.light_strength += 0  # stupid trick (2) to force the viewport to update
	except:
		pass


def update_reflexion(self, context):
	try:
		node_rflx_math_add.inputs[1].default_value = self.reflexion
	except:
		pass


# -------------------------------------------------------------
# Reset UI's settings to initial parameters
# -------------------------------------------------------------
def reset():
	self = bpy.context.scene
	self.visible = True
	self.adjustments_prop = False
	self.mirror = False
	self.world.cycles_visibility.camera = False
	self.light_strength = 1.0
	self.main_light_strength = 0.5
	self.orientation = 0.0
	self.adjustments_color = (0, 0, 0)
	self.sat = 1
	self.hue = 0.5
	self.reflexion = 0.5
	self.mirror = False
	
	self.hemi_light_strength = 1.0
	self.vray_sun_synced = False
	

# -------------------------------------------------------------
# Take UI's values from nodes' values
# -------------------------------------------------------------
def apply_parameters():
	scene = bpy.context.scene
	node_rgb.inputs[0].default_value = scene.adjustments_color[0]
	node_rgb.inputs[1].default_value = scene.adjustments_color[1]
	node_rgb.inputs[2].default_value = scene.adjustments_color[2]
	node_math_add.inputs[1].default_value = scene.light_strength
	node_math.inputs[1].default_value = scene.main_light_strength
	node_sat.inputs[1].default_value = scene.sat
	node_sat.inputs[0].default_value = scene.hue
	node_rflx_math_add.inputs[1].default_value = scene.reflexion
	check_visible()
	node_map.rotation[2] = scene.orientation
	scene.orientation = scene.orientation
	scene.vray_sun_synced = False
	Vray.sun_synced = False
	#world background
	[i for i in bpy.context.screen.areas if i.type == 'VIEW_3D'][0].spaces[0].show_world = True
	
	if scene.mirror:
		node_env.projection = 'MIRROR_BALL'
	else:
		node_env.projection = 'EQUIRECTANGULAR'


def clear_node_tree():
	nodes = bpy.context.scene.world.node_tree.nodes
	for node in nodes:
		try:
			nodes.remove(node)
		except:
			pass


# -------------------------------------------------------------
# True if user checks the color adjustments' box
# False: reset color adjustments to initial values
# -------------------------------------------------------------
def update_adjustments(self, context):
	global adjustments
	if self.adjustments_prop:
		adjustments = True
	else:
		adjustments = False
		self.adjustments_color = (0, 0, 0)
		self.sat = 1
		self.hue = .5
		self.reflexion = self.light_strength
		self.mirror = False


# -------------------------------------------------------------
# Returns True if 'world_name' exists
# -------------------------------------------------------------
def node_tree_exists(world_name):
	for w in bpy.data.worlds:
		if w.name == world_name:
			return True
	return False


# -------------------------------------------------------------
# Returns the ID of a specified world name
# -------------------------------------------------------------
def world_num(world_name):
	for index, w in enumerate(bpy.data.worlds):
		if w.name == world_name:
			return index


# -------------------------------------------------------------
# Setup the node tree around the HDRI image file
#
# img_path: path to the HDRI file
# -------------------------------------------------------------
def setup(img_path):
	global node_coo, node_map, node_rgb, node_add, node_sat, node_env, node_math
	global node_math_add, node_bkgnd, node_out, node_light_path, node_reflexion
	global node_rflx_math, node_rflx_math_add, node_blur_noise, node_blur_coordinate
	global node_blur_mix_1, node_blur_mix_2, node_blur_math_sub, node_blur_math_add
	#bpy.context.area.type = 'NODE_EDITOR'
	#bpy.context.scene.render.engine = 'CYCLES'
	#bpy.context.space_data.tree_type = 'ShaderNodeTree'
	#bpy.context.space_data.shader_type = 'WORLD'
	tree_name = "HDRI Lighting Shortcut"

	if node_tree_exists(tree_name):
		nw_world = bpy.data.worlds[world_num(tree_name)]
		bpy.context.scene.world = nw_world
		bpy.context.scene.world.use_nodes = True
		clear_node_tree()
	else:
		nw_world = bpy.data.worlds.new(tree_name)
		bpy.context.scene.world = nw_world
		bpy.context.scene.world.use_nodes = True

	nodes = nw_world.node_tree.nodes
	tree = nw_world.node_tree
	img = os.path.basename(img_path)

	try:
		if not img_exists(img):
			img = bpy.data.images.load(img_path)
		else:
			img = bpy.data.images[img_index(img)]
	except:
		raise NameError("Cannot load image %s" % img_path)

	for n in nodes:
		nodes.remove(n)

	### CREATE THE NODES
	#
	#Vray
	hemi_lamp = hemi_lamp_find()
	hemi_lamp_nodetree_create(hemi_lamp, img)	  
	#Vray end
	
	node_coo = nodes.new('ShaderNodeTexCoord')
	node_coo.location = -400, 0
	node_coo.name = 'COORDINATE'
	#
	node_map = nodes.new('ShaderNodeMapping')
	node_map.name = "MAPPING"
	node_map.location = -200, 0
	#
	node_rgb = nodes.new("ShaderNodeCombineRGB")
	node_rgb.name = 'COMBINE'
	node_rgb.location = 200, 200
	#
	node_add = nodes.new("ShaderNodeMixRGB")
	node_add.blend_type = 'ADD'
	node_add.inputs[0].default_value = 1
	node_add.location = 400, 400
	node_add.name = 'RGB_ADD'
	#
	node_sat = nodes.new("ShaderNodeHueSaturation")
	node_sat.location = 400, 200
	node_sat.name = 'SATURATION'
	#
	node_env = nodes.new('ShaderNodeTexEnvironment')
	node_env.name = "ENVIRONMENT"
	node_env.image = img
	node_env.location = 200, 0
	#
	node_math = nodes.new('ShaderNodeMath')
	node_math.name = "HLS_MATH"
	node_math.location = 400, -100
	node_math.operation = 'MULTIPLY'
	node_math.inputs[1].default_value = 0.1
	#
	node_math_add = nodes.new('ShaderNodeMath')
	node_math_add.name = "HLS_MATH_ADD"
	node_math_add.location = 400, -300
	node_math_add.operation = 'ADD'
	node_math_add.inputs[1].default_value = 0.5
	#
	node_rflx_math = nodes.new('ShaderNodeMath')
	node_rflx_math.name = "RFLX_MATH"
	node_rflx_math.location = 400, -500
	node_rflx_math.operation = 'MULTIPLY'
	node_rflx_math.inputs[1].default_value = 0.1
	#
	node_rflx_math_add = nodes.new('ShaderNodeMath')
	node_rflx_math_add.name = "RFLX_MATH_ADD"
	node_rflx_math_add.location = 400, -700
	node_rflx_math_add.operation = 'ADD'
	node_rflx_math_add.inputs[1].default_value = 0.5
	#
	node_bkgnd = nodes.new('ShaderNodeBackground')
	node_bkgnd.location = 600, 0
	node_bkgnd.name = 'BACKGROUND'
	#
	node_reflexion = nodes.new('ShaderNodeBackground')
	node_reflexion.location = 600, -200
	node_reflexion.name = 'REFLEXION'
	#
	node_light_path = nodes.new('ShaderNodeLightPath')
	node_light_path.location = 600, 400
	node_light_path.name = "LIGHT_PATH"
	#
	node_ref_mix = nodes.new('ShaderNodeMixShader')
	node_ref_mix.location = 800, 0
	node_ref_mix.name = 'REF_MIX'

	## BLUR NODES
	#
	node_blur_coordinate = nodes.new('ShaderNodeTexCoord')
	node_blur_coordinate.location = -200, 800
	node_blur_coordinate.name = "BLUR_COORDINATE"
	#
	node_blur_noise = nodes.new('ShaderNodeTexNoise')
	node_blur_noise.location = 0, 800
	node_blur_noise.name = "BLUR_NOISE"
	node_blur_noise.inputs[1].default_value = 10000
	#
	node_blur_mix_1 = nodes.new('ShaderNodeMixRGB')
	node_blur_mix_1.location = 200, 800
	node_blur_mix_1.name = "BLUR_MIX_1"
	node_blur_mix_1.inputs[1].default_value = (0, 0, 0, 1)
	node_blur_mix_1.inputs[0].default_value = 0.0
	#
	node_blur_mix_2 = nodes.new('ShaderNodeMixRGB')
	node_blur_mix_2.location = 200, 1000
	node_blur_mix_2.name = "BLUR_MIX_2"
	node_blur_mix_2.inputs[1].default_value = (0, 0, 0, 1)
	node_blur_mix_2.inputs[0].default_value = 0.0
	#
	node_blur_math_add = nodes.new('ShaderNodeVectorMath')
	node_blur_math_add.location = 400, 800
	node_blur_math_add.name = "BLUR_MATH_ADD"
	#
	node_blur_math_sub = nodes.new('ShaderNodeVectorMath')
	node_blur_math_sub.location = 600, 800
	node_blur_math_sub.name = "BLUR_MATH_SUB"
	node_blur_math_sub.operation = 'SUBTRACT'
	#
	node_out = nodes.new('ShaderNodeOutputWorld')
	node_out.location = 1000, 0
	node_out.name = 'OUTPUT'

	# CREATE LINKS BETWEEN NODES
	links = tree.links
	link0 = links.new(node_coo.outputs[0], node_map.inputs[0])
	link1 = links.new(node_map.outputs[0], node_env.inputs[0])
	link2 = links.new(node_rgb.outputs[0], node_add.inputs[1])
	link3 = links.new(node_env.outputs[0], node_sat.inputs[4])
	link4 = links.new(node_sat.outputs[0], node_add.inputs[2])
	link5 = links.new(node_add.outputs[0], node_reflexion.inputs[0])
	link6 = links.new(node_add.outputs[0], node_bkgnd.inputs[0])
	link7 = links.new(node_light_path.outputs[5], node_ref_mix.inputs[0])
	link8 = links.new(node_env.outputs[0], node_rflx_math.inputs[0])
	link9 = links.new(node_rflx_math.outputs[0], node_rflx_math_add.inputs[0])
	link10 = links.new(node_rflx_math_add.outputs[0], node_reflexion.inputs[1])
	link11 = links.new(node_env.outputs[0], node_math.inputs[0])
	link12 = links.new(node_math.outputs[0], node_math_add.inputs[0])
	link13 = links.new(node_math_add.outputs[0], node_bkgnd.inputs[1])
	link14 = links.new(node_bkgnd.outputs[0], node_ref_mix.inputs[1])
	link15 = links.new(node_reflexion.outputs[0], node_ref_mix.inputs[2])
	link16 = links.new(node_ref_mix.outputs[0], node_out.inputs[0])
	# blur group links
	link17 = links.new(node_blur_noise.outputs[0], node_blur_mix_1.inputs[2])
	link18 = links.new(node_blur_mix_1.outputs[0], node_blur_math_add.inputs[1])
	link19 = links.new(node_blur_math_add.outputs[0], node_blur_math_sub.inputs[0])
	link20 = links.new(node_blur_mix_2.outputs[0], node_blur_math_sub.inputs[1])
	# blur link with others
	link21 = links.new(node_blur_coordinate.outputs[0], node_blur_math_add.inputs[0])
	link22 = links.new(node_blur_math_sub.outputs[0], node_map.inputs[0])

	bpy.context.scene.world.cycles.sample_as_light = True
	bpy.context.scene.world.cycles.sample_map_resolution = img.size[0]
	bpy.context.area.type = 'PROPERTIES'


def update_color(self, context):
	node_rgb.inputs[0].default_value = self.adjustments_color[0]
	node_rgb.inputs[1].default_value = self.adjustments_color[1]
	node_rgb.inputs[2].default_value = self.adjustments_color[2]


def update_blur(self, context):
	node_blur_mix_1.inputs[0].default_value = self.blur
	node_blur_mix_2.inputs[0].default_value = self.blur


### CUSTOM PROPS ----------------------------------------------------
bpy.types.Scene.orientation = bpy.props.FloatProperty(name="Orientation", update=update_orientation, max= radians(720), min= radians(-720), default=0, unit='ROTATION', step = degrees(0.017453292519943295*100))
bpy.types.Scene.light_strength = bpy.props.FloatProperty(name="Ambient", update=update_strength, default=1.0, precision=3)
bpy.types.Scene.hemi_light_strength = bpy.props.FloatProperty(name="Hemi", update=update_hemi_light_strength, default=1.0, precision=3)
bpy.types.Scene.vray_sun_synced = bpy.props.BoolProperty(name="Sync Sun & Hdri", update=update_vray_sun_synced, default = False)
bpy.types.Scene.main_light_strength = bpy.props.FloatProperty(name="Main", update=update_main_strength, default=0.5, precision=3)
bpy.types.Scene.filepath = bpy.props.StringProperty(subtype='FILE_PATH')
bpy.types.Scene.visible = bpy.props.BoolProperty(update=update_visible, name="Visible", description="Switch on/off the visibility of the background", default=True)
bpy.types.Scene.sat = bpy.props.FloatProperty(name="Saturation", update=update_sat, max=2, min=0, default=1)
bpy.types.Scene.hue = bpy.props.FloatProperty(name="Hue", update=update_hue, max=1, min=0, default=.5)
bpy.types.Scene.reflexion = bpy.props.FloatProperty(name="Exposure", update=update_reflexion, default=1)
bpy.types.Scene.adjustments_prop = bpy.props.BoolProperty(name="Adjustments", update=update_adjustments, default=False)
bpy.types.Scene.mirror = bpy.props.BoolProperty(name="Mirror Ball", update=update_mirror, default=False)
bpy.types.Scene.adjustments_color = bpy.props.FloatVectorProperty(name="Correction", update=update_color, subtype="COLOR", min=0, max=1, default=(0, 0, 0))
bpy.types.Scene.blur = bpy.props.FloatProperty(name="Blur", update=update_blur, min=0, max=1, default=0.0)


### ADD-ON'S GUI -----------------------------------------------------
class hdri_map(bpy.types.Panel):
	bl_idname = "OBJECT_PT_sample"
	bl_label = "HDRI Lighting Shortcut"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "world"

	
	def draw(self, context):
		global adjustments, img_path
		try:
			img = current_bkgnd()
		except:
			img = ''
		layout = self.layout
		scene = bpy.context.scene

		if not node_tree_ok():
			row = layout.row()
			row.operator("nodes.img", icon="WORLD")
		if node_tree_ok():
			row = layout.row(align=True)
			row.active = True
			if not img_path == "":
				row.operator("nodes.img", icon="WORLD", text=os.path.basename(img))
			else:
				row.operator("nodes.img", icon="WORLD")
			if scene.visible:
				row.operator("visible.img", icon="RESTRICT_VIEW_OFF")
			else:
				row.operator("visible.img", icon="RESTRICT_VIEW_ON")
			row.operator("remove.setup", icon="X")

			row = layout.row(align=True)

			row.label("", icon = 'LAMP_HEMI')
			row.prop(scene, "hemi_light_strength", text = 'Hemi')
			
			row.label("", icon = 'IMAGE_COL')
			row.prop(scene, "light_strength", text = 'Image')

			#row.prop(scene, "main_light_strength")
			#row = box.row()
			
			row = layout.row(align = True)
			row.label("", icon = 'OUTLINER_DATA_META')
			row.prop(scene, "orientation")
			#row = box.row()
			#row.prop(scene, "adjustments_prop")
			#row = layout.row()
			#row.label(" ")
			row.prop(scene, "mirror")
			row = layout.row(align = True)
			row.label("", icon = 'EYEDROPPER')
			row.alert = True if Vray.sun_button_setmode else False
			row.operator("sun_set_cursor.execute", text = "Point sun position" if not Vray.sun_button_setmode else 
			"Sync sun to Hdri" )
			#print ("setmode:", Vray.sun_button_setmode)
			col = row.column()
			col.prop(scene, "vray_sun_synced")
			col.enabled = Vray.sun_synced
			#row.operator("sun.execute")
			
			if adjustments:
				row = box.row()
				row.prop(scene, "sat")
				row.prop(scene, "hue")
				row = box.row()
				row.prop(scene, 'adjustments_color')
				row = box.row()
				row.prop(scene, 'reflexion')
				row.prop(scene, 'blur')


class OBJECT_OT_load_img(bpy.types.Operator):
	bl_label = "Load Image"
	bl_idname = "nodes.img"
	bl_description = "Load Image"
	bl_options = {'REGISTER'}

	filter_glob = bpy.props.StringProperty(default="*.tif;*.png;*.jpeg;*.jpg;*.exr;*.hdr", options={'HIDDEN'})
	filepath = bpy.props.StringProperty(name="File Path", description="Filepath used for importing files", maxlen=1024, default="")
	files = bpy.props.CollectionProperty(name="File Path", type=bpy.types.OperatorFileListElement,)

	def execute(self, context):
		context.scene.vray_sun_synced = False
		
		global img_path
		img_path = self.properties.filepath
		setup(img_path)
		apply_parameters()
		return {'FINISHED'}

	def invoke(self, context, event):
		global folder_path

		# get add-on's name (for some reasons)
		for n in bpy.context.user_preferences.addons.keys():
			if 'lighting' in n and 'Shortcut' in n:
				name = n
				break
		try:
			user_preferences = bpy.context.user_preferences
			addon_prefs = user_preferences.addons[name].preferences
			folder_path = addon_prefs.folder_path
		except:
			folder_path = '//'
			pass

		print(folder_path)
		self.filepath = folder_path
		wm = context.window_manager
		wm.fileselect_add(self)
		return {'RUNNING_MODAL'}


class OBJECT_OT_Remove_setup(bpy.types.Operator):
	bl_idname = "remove.setup"
	bl_label = ""

	def execute(self, context):
		reset()
		tree_name = "HDRI Lighting Shortcut"
		if node_tree_exists(tree_name):
			nw_world = bpy.data.worlds[world_num(tree_name)]
			bpy.context.scene.world = nw_world
			clear_node_tree()
			# stupid trick (1) to force cycles to update the viewport
			bpy.context.scene.world.light_settings.use_ambient_occlusion = not bpy.context.scene.world.light_settings.use_ambient_occlusion
			bpy.context.scene.world.light_settings.use_ambient_occlusion = not bpy.context.scene.world.light_settings.use_ambient_occlusion
		return{'RUNNING_MODAL'}


class OBJECT_OT_Visible(bpy.types.Operator):
	bl_idname = "visible.img"
	bl_label = ""

	def execute(self, context):
		scene = bpy.context.scene
		cam = scene.world.cycles_visibility
		if scene.visible:
			cam.camera = True
			scene.visible = False
		else:
			cam.camera = False
			scene.visible = True
		try:
			scene.light_strength += 0  # stupid trick (2) to force the viewport to update
		except:
			pass
		return{'RUNNING_MODAL'}


class HDRI_Preferences(AddonPreferences):
	bl_idname = __name__
	folder_path = bpy.props.StringProperty(name="HDRI Folder", subtype='DIR_PATH',)

	def draw(self, context):
		layout = self.layout
		layout.prop(self, "folder_path")


class OBJECT_OT_addon_prefs(Operator):
	"""Display preferences"""
	bl_idname = "object.addon_prefs"
	bl_label = "Addon Preferences"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		user_preferences = context.user_preferences
		addon_prefs = user_preferences.addons[__name__].preferences

		info = ("Path: %s" %
				(addon_prefs.folder_path))

		self.report({'INFO'}, info)
		return {'FINISHED'}


# REGISTRATION ------------------------------------------------------
def register():
	bpy.utils.register_module(__name__)


def unregister():
	bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
	register()
