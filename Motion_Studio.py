# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


#-----------------Some code is derived and or modified  from the Blender Makewalk add-on ver 0.93
#-----------------Code section will be marked: ****MakeHuman****
# ----------------Project Name:        MakeHuman
# ----------------Product Home Page:   http://www.makehuman.org/
# ----------------Code Home Page:      http://code.google.com/p/makehuman/
# ----------------Authors:             Thomas Larsson
# ----------------Script copyright (C) MakeHuman Team 2001-2014
# ----------------Coding Standards:    See http://www.makehuman.org/node/165


#------------------------------------Notes---------------------------------
#------------------Panel locations from top to buttom are alphabetical 
#
#
#
#








import bpy    
from bpy.types import Menu, Panel, UIList

bl_info = {
    "name": "Motion Studio",
    "author": "Open Studio",
    "version": (0, 100),
    "blender": (2, 7, 3),
    "location": "View3D > Tools > Motion Studio",
    "description": "Live Mocap animation to rig add-on. free to the",
    "warning": "",
    'wiki_url': "",
    "category": "MotionStudio"}





# To support reload properly, try to access a package var, if it's there, reload everything
if "bpy" in locals():
    print("Reloading MotionStudio v %d.%d" % bl_info["version"])
    #import imp


 

class View3DPanel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
#------------------------------- Add Armature Objectmode----------------------------------------     
class MoionStudioObjectModePanel(View3DPanel, Panel):
    bl_label = "Motion Studio"
    bl_context = "objectmode"
    bl_category = "Motion Studio"


    @staticmethod
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Human Metarigs:")
        layout.operator("object.snap_cursor_center_armature_human_metarig_add", text="Add Rig To center", icon='ARMATURE_DATA')
        layout.operator("object.armature_human_metarig_add", text="Add Rig", icon='OUTLINER_OB_ARMATURE')



class MotionTracksAddMetaRigToCenter(bpy.types.Operator):
    bl_idname = "object.snap_cursor_center_armature_human_metarig_add"
    bl_label = "Center"
 
    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.object.armature_human_metarig_add()
        return{'FINISHED'}             
    
class MotionTracksAddMetaRigToCenter(bpy.types.Operator):  
    bl_space_type = 'VIEW_3D'
    bl_idname = "object.motiontracksaddmetarigtocenter"  
    #bl_label = "Apply Motion Tracks"    

    bl_context = "objectmode"
    bl_category = "Motion Studio"

  

    def execute(self, context):  
        bpy.ops.view3d.snap_cursor_to_center()
        #bpy.ops.object.armature_human_metarig_add()

        return {'FINISHED'} 




















#------------------------------- Apply Poses PoseMode----------------------------------------     
class MoionStudioPanel(View3DPanel, Panel):
    bl_label = "Motion Studio"
    bl_context = "posemode"
    bl_category = "Motion Studio"


    @staticmethod
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Draw:")
        layout.operator("mcp.set_t_pose", text="Set T-pose", icon='OUTLINER_DATA_ARMATURE')
        layout.operator("object.moionstudioapplyrestpose", text="Set Rest Pose", icon='MOD_ARMATURE')

#------------------------------- Clear Pose to Rest Pose (Operator)----------------------------------------     
class MoionStudioApplyRestPose(bpy.types.Operator):
    bl_idname = "object.moionstudioapplyrestpose"
    bl_label = "Motion Studio"
    #bl_context = "posemode"
    bl_category = "Motion Studio"
        
    def execute(self, context):
        layout = self.layout
        context = bpy.context
        scene   = context.scene
        source  = context.object
        targets = bpy.data.objects["metarig"].data.bones.active
        bpy.ops.pose.rot_clear()          
        return {'FINISHED'}
#-----------------------------****MakeHuman**** Load .bvh ----------------------------------------     
class MoionStudioLoadPanel(View3DPanel, Panel):
    # subclass must set
    # bl_space_type = 'IMAGE_EDITOR'
    #bl_space_type = 'CLIP_EDITOR' #add for tracking
    bl_label = "Load Animation"
    bl_context = "objectmode"
    bl_context = "posemode"
    #bl_category = "Misc"
    bl_category = "Motion Studio"
    #bl_region_type = 'TOOLS'
    @staticmethod
    def draw(self, context):
        layout = self.layout
        ob = context.object
        scn = context.scene
        if ob and ob.type == 'ARMATURE':
            layout.operator("mcp.load_and_retarget", text="Load .BVH", icon='POSE_DATA')
            layout.separator()
            layout.prop(scn, "McpStartFrame")
            layout.prop(scn, "McpEndFrame")
            layout.separator()
            layout.prop(scn, "McpShowDetailSteps")
            if scn.McpShowDetailSteps:
                ins = inset(layout)
                ins.operator("mcp.load_bvh")
                ins.operator("mcp.rename_bvh")
                ins.operator("mcp.load_and_rename_bvh")

                ins.separator()
                ins.operator("mcp.retarget_mhx")

                ins.separator()
                ins.operator("mcp.simplify_fcurves")
                ins.operator("mcp.rescale_fcurves")

        else:
            layout.operator("mcp.load_bvh")
            layout.separator()
            layout.prop(scn, "McpStartFrame")
            layout.prop(scn, "McpEndFrame")     


#------------------------------- Remove Keyframes ----------------------------------------     
class MoionStudioClearPanel(View3DPanel, Panel):
    bl_label = "Remove Keyframes"
    bl_context = "objectmode"
    bl_context = "posemode"
    bl_category = "Motion Studio"
   

    @staticmethod
    def draw(self, context):
        layout = self.layout
        obj = bpy.context.object
        scn = context.scene
        col = layout.column(align=True)
        layout.operator("anim.keyframe_delete", text="Delete Current Keyframe", icon='KEY_DEHLT')
        layout.operator("anim.motiondeletetracks", text="Delete All Keyframes", icon='KEY_DEHLT')
     
       
#------------------------------- Delete All Key Frames Operator----------------------------------------        
class MotionDeleteTracks(bpy.types.Operator):  
    bl_idname = "anim.motiondeletetracks"  
    bl_category = "Motion Studio"
    bl_context = "posemode"
    bl_label = "MotionDeletTracks"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context): 
         obj = bpy.context.object
         scn = context.scene
         #obj.animation_data_create()
         obj.animation_data.action = bpy.data.actions.new(name="MyAction")
         fcu = obj.animation_data.action.fcurves.new(data_path="location", index=2)
         for f in range(scn.frame_start, scn.frame_end+1):
                obj.keyframe_delete(fcu.data_path, index=-1, frame=bpy.context.scene.frame_current)
                return {'FINISHED'}   

#------------------------------- Apply Live Tracks----------------------------------------        
class MoionStudioySwitchToClipEditor(View3DPanel, Panel):
    #bl_idname = "object.moionstudioapplytracks"  
    #bl_space_type = 'CLIP_EDITOR' #add for tracking
    bl_label = "Apply Motion Tracks"  
    #bl_context = "objectmode"
    bl_context = "posemode"

    bl_category = "Motion Studio"

    def draw(self, context): 
        layout = self.layout
        col = layout.column(align=True)
        layout.operator("object.motiontrackstoemptys", text="Apply Track To Emptys", icon='PLAY')
        layout.operator("object.motiontracks", text="Apply Tracks", icon='ANIM_DATA')
        #print ("Animation Tracks Removed")
        layout.operator("object.motiontracks", text="Unapply Tracks", icon='CANCEL')
        #print ("Animation Tracks Removed")
        layout.operator("object.motiontrackstoemptys", text="Apply Live Track", icon='REC')
        #layout.operator("object.livemotiontracks", text="Apply Live Track", icon='REC')
   



class MoionStudioyApplyTracks(View3DPanel, Panel):
    bl_idname = "object.moionstudioapplytracks"  
    bl_space_type = 'CLIP_EDITOR' #add for tracking
    bl_label = "Apply Motion Tracks"  
    #bl_context = "objectmode"
    bl_context = "posemode"

    bl_category = "Motion Studio"

    def draw(self, context): 
        layout = self.layout
        col = layout.column(align=True)
        layout.operator("object.motiontrackstoemptys", text="Apply Track To Emptys", icon='PLAY')
        layout.operator("object.motiontracks", text="Apply Tracks", icon='ANIM_DATA')
        #print ("Animation Tracks Removed")
        layout.operator("object.motiontracks", text="Unapply Tracks", icon='CANCEL')
        #print ("Animation Tracks Removed")
        layout.operator("object.motiontrackstoemptys", text="Apply Live Track", icon='REC')
        #layout.operator("object.livemotiontracks", text="Apply Live Track", icon='REC')
   
#------------------------------- Apply Tracks Template----------------------------------------     

class MotionTracksToEmptys(bpy.types.Operator):  
    bl_space_type = 'CLIP_EDITOR' #add for tracking
    bl_idname = "object.motiontrackstoemptys"  
    bl_label = "Apply Motion Tracks"    
    bl_context = "posemode"
    bl_context = "objectmode"
    bl_category = "Motion Studio"

  

    def execute(self, context): 
        bpy.context.area.type = 'CLIP_EDITOR'
        bpy.ops.clip.select_all(action='TOGGLE') #selet all tracks
        bpy.ops.clip.track_to_empty() # create tracked emptys 
        #***************need to call this operator ***********************
        #bpy.ops.object.motiontracks()

        
        bpy.context.area.type = 'VIEW_3D' # Returns to 3dveiw 
        bl_context = "posemode"
        obj = bpy.data.objects["metarig"]
        bpy.context.scene.objects.active = obj
        bpy.ops.object.mode_set(mode='POSE')
        return {'FINISHED'} 
#------------------------------------------------------------------------------------------       
    
#------------------------------- Template----------------------------------------     
'''
class MoionStudiozLiveTracks(View3DPanel, Panel):  
    #bl_idname = "object.motion_tools"  
    bl_label = "Tracks"     
    bl_context = "objectmode"
    bl_context = "posemode"
    bl_category = "Motion Studio"

  

    def draw(self, context): 
        layout = self.layout   
        col = layout.column(align=True)
        layout.operator("anim.motiontracks", text="Apply Live Track", icon='REC')
'''
#------------------------------------------------------------------------------------------       
   
     
     

class MotionTracks(bpy.types.Operator):  
    bl_idname = "object.motiontracks"  #called
    #bl_label = "Motion Tools"  
    #bl_category = "Tools"
    bl_category = "Motion Studio"
    bl_context = "posemode"
    bl_label = "MotionTracks"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context): 
        #print(self)
        #print(dir(self))
        #print(context)
        #print(dir(context))


        bpy.ops.object.mode_set(mode='POSE')    
        #****************************************************************************************************		
        #---------------------------------------front Camera Empty Damped Tracking-----------------------
        #****************************************************************************************************
        #----------------------------- thigh.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['thigh.L'].bone
        ActiveBone = bpy.ops.pose  
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["thigh.L"].constraints["Damped Track"].target = bpy.data.objects["Track.thigh.L"]  
        bpy.context.object.pose.bones["thigh.L"].constraints["Damped Track"].track_axis = 'TRACK_Y'
        #----------------------------- thigh.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['thigh.R'].bone  
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["thigh.R"].constraints["Damped Track"].target = bpy.data.objects["Track.thigh.R"]   
        bpy.context.object.pose.bones["thigh.R"].constraints["Damped Track"].track_axis = 'TRACK_Y'
        #----------------------------- shin.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shin.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shin.L"].constraints["Damped Track"].target = bpy.data.objects["Track.shin.L"] 
        bpy.context.object.pose.bones["shin.L"].constraints["Damped Track"].track_axis = 'TRACK_Y'		
        #----------------------------- shin.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shin.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shin.R"].constraints["Damped Track"].target = bpy.data.objects["Track.shin.R"]
        bpy.context.object.pose.bones["shin.R"].constraints["Damped Track"].track_axis = 'TRACK_Y'        
        #----------------------------- shoulder.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shoulder.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shoulder.L"].constraints["Damped Track"].target = bpy.data.objects["Track.shoulder.L"] 
        bpy.context.object.pose.bones["shoulder.L"].constraints["Damped Track"].track_axis = 'TRACK_Y'		
        #----------------------------- shoulder.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shoulder.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shoulder.R"].constraints["Damped Track"].target = bpy.data.objects["Track.shoulder.R"]
        bpy.context.object.pose.bones["shoulder.R"].constraints["Damped Track"].track_axis = 'TRACK_Y'        
        #-----------------------------head -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['head'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["head"].constraints["Damped Track"].target = bpy.data.objects["Track.head"]
        bpy.context.object.pose.bones["head"].constraints["Damped Track"].track_axis = 'TRACK_Y'        
        #----------------------------- neck -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['neck'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["neck"].constraints["Damped Track"].target = bpy.data.objects["Track.neck"]
        bpy.context.object.pose.bones["neck"].constraints["Damped Track"].track_axis = 'TRACK_Y'		
        #----------------------------- chest -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['chest'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["chest"].constraints["Damped Track"].target = bpy.data.objects["Track.chest"]
        bpy.context.object.pose.bones["chest"].constraints["Damped Track"].track_axis = 'TRACK_Y'	
        #----------------------------- spine -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['spine'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["spine"].constraints["Damped Track"].target = bpy.data.objects["Track.spine"]
        bpy.context.object.pose.bones["spine"].constraints["Damped Track"].track_axis = 'TRACK_Y'
        '''
        #*************************  Fix Me ******************************************************
        #Option 1 divide Track.hips.L x.position and Track.hips.R x.position
        #Opyion 2: Create a hips suit marking and disregard Hips.L/.R data	
        #----------------------------- hips -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['hips'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["hips"].constraints["Damped Track"].target = bpy.data.objects["Track.hips.L"]
        bpy.context.object.pose.bones["hips"].constraints["Damped Track"].track_axis = 'TRACK_Y'
        
        #******************************************************************************
        '''
        
        #----------------------------- upper_arm.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['upper_arm.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["upper_arm.L"].constraints["Damped Track"].target = bpy.data.objects["Track.upper_arm.L"]
        bpy.context.object.pose.bones["upper_arm.L"].constraints["Damped Track"].track_axis = 'TRACK_Y'        
        #----------------------------- upper_arm.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['upper_arm.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["upper_arm.R"].constraints["Damped Track"].target = bpy.data.objects["Track.upper_arm.R"]
        bpy.context.object.pose.bones["upper_arm.R"].constraints["Damped Track"].track_axis = 'TRACK_Y'		
        #----------------------------- forearm.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['forearm.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["forearm.L"].constraints["Damped Track"].target = bpy.data.objects["Track.forearm.L"]
        bpy.context.object.pose.bones["forearm.L"].constraints["Damped Track"].track_axis = 'TRACK_Y'        
        #----------------------------- forearm.R ------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['forearm.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["forearm.R"].constraints["Damped Track"].target = bpy.data.objects["Track.forearm.R"]
        bpy.context.object.pose.bones["forearm.R"].constraints["Damped Track"].track_axis = 'TRACK_Y'
        bpy.ops.object.motionhidetracks('INVOKE_DEFAULT')
        return {'FINISHED'}


'''
        #----------------------------- hand.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['hand.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["hand.L"].constraints["Damped Track"].target = bpy.data.objects["Track.forearm.L"]
        bpy.context.object.pose.bones["hand.L"].constraints["Damped Track"].track_axis = 'TRACK_Y'        
        #----------------------------- hand.R ------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['hand.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["hand.R"].constraints["Damped Track"].target = bpy.data.objects["Track.forearm.R"]
        bpy.context.object.pose.bones["hand.R"].constraints["Damped Track"].track_axis = 'TRACK_Y'
'''




       


        #****************************************************************************************************		
        #---------------------------------------Side Camera Empty Damped Tracking---------------------------
        #****************************************************************************************************
		
'''		
        #----------------------------- thigh.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['thigh.L'].bone
        ActiveBone = bpy.ops.pose  
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["thigh.L"].constraints["Damped Track"].target = bpy.data.objects["Track.thigh.L2"]  
        bpy.context.object.pose.bones["thigh.L"].constraints["Damped Track"].track_axis = 'TRACK_X'
        #----------------------------- thigh.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['thigh.R'].bone  
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["thigh.R"].constraints["Damped Track"].target = bpy.data.objects["Track.thigh.R2"]   
        bpy.context.object.pose.bones["thigh.R"].constraints["Damped Track"].track_axis = 'TRACK_X'
        #----------------------------- shin.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shin.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shin.L"].constraints["Damped Track"].target = bpy.data.objects["Track.shin.L2"] 
        bpy.context.object.pose.bones["shin.L"].constraints["Damped Track"].track_axis = 'TRACK_X'		
        #----------------------------- shin.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shin.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shin.R"].constraints["Damped Track"].target = bpy.data.objects["Track.shin.R2"]
        bpy.context.object.pose.bones["shin.R"].constraints["Damped Track"].track_axis = 'TRACK_X'        
        #----------------------------- shoulder.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shoulder.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shoulder.L"].constraints["Damped Track"].target = bpy.data.objects["Track.shoulder.L2"] 
        bpy.context.object.pose.bones["shoulder.L"].constraints["Damped Track"].track_axis = 'TRACK_X'		
        #----------------------------- shoulder.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shoulder.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shoulder.R"].constraints["Damped Track"].target = bpy.data.objects["Track.shoulder.R2"]
        bpy.context.object.pose.bones["shoulder.R"].constraints["Damped Track"].track_axis = 'TRACK_X'        
        #-----------------------------head -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['head'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["head"].constraints["Damped Track"].target = bpy.data.objects["Track.head.2"]
        bpy.context.object.pose.bones["head"].constraints["Damped Track"].track_axis = 'TRACK_X'        
        #----------------------------- neck -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['neck'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["neck"].constraints["Damped Track"].target = bpy.data.objects["Track.neck.2"]
        bpy.context.object.pose.bones["neck"].constraints["Damped Track"].track_axis = 'TRACK_X'		
        #----------------------------- chest -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['chest'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["chest"].constraints["Damped Track"].target = bpy.data.objects["Track.chest.2"]
        bpy.context.object.pose.bones["chest"].constraints["Damped Track"].track_axis = 'TRACK_X'	
        #----------------------------- spine -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['spine'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["spine"].constraints["Damped Track"].target = bpy.data.objects["Track.spine.2"]
        bpy.context.object.pose.bones["spine"].constraints["Damped Track"].track_axis = 'TRACK_X'		
        #----------------------------- hips -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['hips'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["hips"].constraints["Damped Track"].target = bpy.data.objects["Track.hips.2"]
        bpy.context.object.pose.bones["hips"].constraints["Damped Track"].track_axis = 'TRACK_X'
        #----------------------------- upper_arm.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['upper_arm.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["upper_arm.L"].constraints["Damped Track"].target = bpy.data.objects["Track.upper_arm.L2"]
        bpy.context.object.pose.bones["upper_arm.L"].constraints["Damped Track"].track_axis = 'TRACK_X'        
        #----------------------------- upper_arm.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['upper_arm.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["upper_arm.R"].constraints["Damped Track"].target = bpy.data.objects["Track.upper_arm.R2"]
        bpy.context.object.pose.bones["upper_arm.R"].constraints["Damped Track"].track_axis = 'TRACK_X'		
        #----------------------------- forearm.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['forearm.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["forearm.L"].constraints["Damped Track"].target = bpy.data.objects["Track.forearm.L2"]
        bpy.context.object.pose.bones["forearm.L"].constraints["Damped Track"].track_axis = 'TRACK_X'        
        #----------------------------- forearm.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['forearm.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["forearm.R"].constraints["Damped Track"].target = bpy.data.objects["Track.forearm.R2"]
        bpy.context.object.pose.bones["forearm.R"].constraints["Damped Track"].track_axis = 'TRACK_X'       
        return {'FINISHED'}  
'''

class MotionHideTracks(bpy.types.Operator):  
    bl_idname = "object.motionhidetracks"  #called
    bl_category = "Motion Studio"
    bl_context = "posemode"
    bl_label = "MotionTracks"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context): 
        bpy.data.objects["Track.thigh.L"].hide = True
        bpy.data.objects["Track.thigh.R"].hide = True  
        bpy.data.objects["Track.shin.L"].hide = True
        bpy.data.objects["Track.shin.R"].hide = True
        bpy.data.objects["Track.shoulder.L"].hide = True
        bpy.data.objects["Track.shoulder.R"].hide = True
        bpy.data.objects["Track.head"].hide = True
        bpy.data.objects["Track.neck"].hide = True
        bpy.data.objects["Track.chest"].hide = True
        bpy.data.objects["Track.spine"].hide = True
        bpy.data.objects["Track.hips.L"].hide = True
        #bpy.data.objects["Track.hips"].hide = True
        bpy.data.objects["Track.hips.R"].hide = True
        bpy.data.objects["Track.upper_arm.L"].hide = True
        bpy.data.objects["Track.upper_arm.R"].hide = True
        bpy.data.objects["Track.forearm.L"].hide = True
        bpy.data.objects["Track.forearm.R"].hide = True
        return {'FINISHED'}


























     
     
     
     
     
     
     
     
     
     
        
	

#register     http://www.blender.org/api/blender_python_api_2_59_0/info_overview.html   
        
if __name__ == "__main__":  # only for live edit. 
    bpy.utils.register_module(__name__)
#************************ You may need to comment these modules out***************
def register():
     #bpy.utils.register_module(__name__)
     bpy.utils.register_module(MoionStudioObjectModePanel)
     bpy.utils.register_module(MoionStudioPanel)
     bpy.utils.register_module(MotionTracksAddMetaRigToCenter) 
     bpy.utils.register_module(MoionStudioApplyRestPose)
     bpy.utils.register_module(MoionStudioLoadPanel)
     bpy.utils.register_module(MoionStudioClearPanel)
     bpy.utils.register_module(MotionDeleteTracks)
     bpy.utils.register_module(MoionStudioyApplyTracks)
     bpy.utils.register_module(MoionStudiozLiveTracks)
     bpy.utils.register_module(MoionStudioySwitchToClipEditor)
     bpy.utils.register_module(MotionTracksToEmptys)
     bpy.utils.register_class(MotionTracks)  
     bpy.utils.register_class(MotionHideTracks)
   

def unregister():
       bpy.utils.unregister_module(__name__)

#if __name__ == "__main__":
#   register()

print("MotionStudio loaded")    
    
