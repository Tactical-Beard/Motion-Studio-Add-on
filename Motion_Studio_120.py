# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
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


#-------------****Some code is derived and or modified  from the Blender Makewalk add-on ver 0.93****
#-----------------Code section will be marked: ****MakeHuman****
# ----------------Project Name:        MakeHuman
# ----------------Product Home Page:   http://www.makehuman.org/
# ----------------Code Home Page:      http://code.google.com/p/makehuman/
# ----------------Authors:             Thomas Larsson
# ----------------Script copyright (C) MakeHuman Team 2001-2014
# ----------------Coding Standards:    See http://www.makehuman.org/node/165


#------------------------------------Notes---------------------------------
'''
    Panel locations from top to buttom are alphabetical 




'''



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
#***********************************************************************************************
#-----------------------------------Object Mode Panel-------------------------------------------
#***********************************************************************************************
#------------------------------- Add Armature Objectmode (UI) ----------------------------------     
class MoionStudioObjectModePanel(View3DPanel, Panel):
    bl_label = "Motion Studio"
    bl_context = "objectmode"
    bl_category = "Motion Studio"
    @staticmethod
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Human Rigs:")
        layout.operator("object.snap_cursor_center_armature_human_metarig_add", text="Add Rig To center", icon='ARMATURE_DATA')
        layout.operator("object.armature_human_metarig_add", text="Add Rig", icon='OUTLINER_OB_ARMATURE')
        layout.operator("object.motiondeletetracks", text="Delete Empties", icon='PANEL_CLOSE')
        # delete empties is near the bottom of the code
        col = layout.column(align=True)
        col = layout.column(align=True)
#------------------------------- Add Metrig And 3D Cursor To Center (Operator)---------------------------------------- 
class MotionTracksAddMetaRigToCenter(bpy.types.Operator):
    bl_idname = "object.snap_cursor_center_armature_human_metarig_add" 
    bl_label = "Center"#has to have a label   
    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.object.armature_human_metarig_add()
        return{'FINISHED'}
#------------------------------- Add Armature Objectmode----------------------------------------     
class MoionLibaryImport(View3DPanel, Panel):
    bl_label = "Motion Libary"
    bl_context = "objectmode"
    bl_category = "Motion Studio"


    @staticmethod
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Import Rigs:")
        layout.operator("import_scene.fbx", text="Import FBX Rig", icon='OUTLINER_OB_ARMATURE')
                 
#***********************************************************************************************
#-----------------------------------Pose Mode Panel-------------------------------------------
#***********************************************************************************************
#------------------------------- Apply T-Pose/Rest Pose (UI) ----------------------------------------     
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
        layout.operator("mcp.rest_current_pose", text="Reset Rest Pose", icon='MOD_ARMATURE')

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
#-----------------------------****MakeHuman**** Load .bvh (UI)----------------------------------------     
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


#------------------------------- Remove Keyframes (UI) ----------------------------------------     
class MoionStudioClearPanel(View3DPanel, Panel):
    bl_label = "Remove Keyframes"
    bl_context = "objectmode"
    bl_context = "posemode"
    bl_category = "Motion Studio"
    #bl_options = {'REGISTER', 'UNDO'}

    @staticmethod
    def draw(self, context):
        layout = self.layout
        obj = bpy.context.object
        scn = context.scene
        col = layout.column(align=True)
        layout.operator("anim.keyframe_delete", text="Delete Current Keyframe", icon='KEY_DEHLT')
        layout.operator("anim.motiondeletetracks", text="Delete All Keyframes", icon='KEY_DEHLT')

       
#------------------------------- Delete All Key Frames (Operator)----------------------------------------        
class MotionDeleteTracks(bpy.types.Operator):  
    bl_idname = "anim.motiondeletetracks"  
    bl_category = "Motion Studio"
    bl_context = "posemode"
    bl_label = "MotionDeletTracks"
    #bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context): 
         obj = bpy.context.object
         scn = context.scene
         #obj.animation_data_create()
         obj.animation_data.action = bpy.data.actions.new(name="MyAction")
         fcu = obj.animation_data.action.fcurves.new(data_path="location", index=2)
         for f in range(scn.frame_start, scn.frame_end+1):
                obj.keyframe_delete(fcu.data_path, index=-1, frame=bpy.context.scene.frame_current)
                return {'FINISHED'}   

#------------------------------- Apply Live Tracks  (UI)----------------------------------------        
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
        layout.operator("object.motiontracksy", text="Apply Y Tracks", icon='ANIM_DATA')
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        layout.operator("object.motiontrackstoemptysx", text="Apply Emptys", icon='PLAY')
        layout.operator("object.motiontracksx", text="Apply X Tracks", icon='ANIM_DATA')
        #layout.operator("object.motiontracks", text="Unapply Tracks", icon='CANCEL')
       
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        layout.operator("object.motiontrackstoemptys", text="Apply Live Track", icon='REC')
        #layout.operator("object.livemotiontracks", text="Apply Live Track", icon='REC')
        
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)   
        layout.operator("object.motionstudiosetcam", text="Toggle Camera", icon='CAMERA_DATA')#Toggle Scene Camera 
#**********************************************************************************************
#--------------------------------------Movie Editor -------------------------------------------
#**********************************************************************************************

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
        

        
        #layout.operator("object.motiontracks", text="Apply Tracks", icon='ANIM_DATA')
        #print ("Animation Tracks Removed")
        #layout.operator("object.motiontracks", text="Unapply Tracks", icon='CANCEL')
        #print ("Animation Tracks Removed")
        layout.operator("object.motiontrackstoemptys", text="Apply Live Track", icon='REC')
        #layout.operator("object.livemotiontracks", text="Apply Live Track", icon='REC')
        layout.operator("object.motionstudioapplyxytracks", text="Apply XY Tracks", icon='CAMERA_DATA')
        layout.operator("object.motionstudiosetcam", text="Toggle Camera", icon='CAMERA_DATA')
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        #layout.operator("object.testclipvideo", text="testclipvideo", icon='CAMERA_DATA')
        layout.operator("object.motionstudiosetclip", text="change clip", icon='CAMERA_DATA')
#**********************************************************************************************
#------------------------------- Create Empties And Apply Tracks Y (Operator)----------------------------------------     

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
#------------------------------- Create Empties And Apply Tracks X(Operator)----------------------------------------     
class MotionTracksToEmptysx(bpy.types.Operator):  
    bl_space_type = 'CLIP_EDITOR' #add for tracking
    bl_idname = "object.motiontrackstoemptysx"  
    bl_label = "Apply Motion Tracks"    
    bl_context = "posemode"
    bl_context = "objectmode"
    bl_category = "Motion Studio"

  

    def execute(self, context): 
        bpy.context.area.type = 'CLIP_EDITOR'
        bpy.ops.clip.select_all(action='TOGGLE') #selet all tracks
        scene = context.scene
        scene.camera = bpy.data.objects["xcamera"] #Set scene camera to "name of came"
        scene.active_clip = bpy.data.movieclips["xtracks"]
        #MovieClip.source[‘SEQUENCE’, 'xtracks']
        #MovieClip.source[‘SEQUENCE’, ‘MOVIE’]
        bpy.ops.clip.track_to_empty() #Create empty x-tracks
        bpy.context.area.type = 'VIEW_3D' # Returns to 3dveiw 
        bl_context = "posemode"
        obj = bpy.data.objects["metarig"]
        bpy.context.scene.objects.active = obj 
        #bpy.ops.object.motiontracksx() #Apply x-tracks to the bones﻿       
        bpy.ops.object.mode_set(mode='POSE')  
        return {'FINISHED'}     
#-------------------------------------------Change movieclip work in progress (Operator)-----------------------------------------------       
'''class TestClipVideo(bpy.types.Operator):  
    bl_space_type = 'CLIP_EDITOR' #add for tracking
    bl_idname = "object.testclipvideo"  
    bl_label = "Apply Motion Tracks"    
    bl_context = "posemode"
    bl_context = "objectmode"
    bl_category = "Motion Studio"
    
    def execute(self, context): 
        bpy.context.area.type = 'CLIP_EDITOR'
        #print(bpy.data.movieclips[1])
        #print(bpy.data.movieclips[0])
        #bpy.ops.clip.open("xtracks")
        
        scene = bpy.context.scene
        sc = context.space_data
        clip = sc.clip
        scene.active_clip = bpy.data.movieclips[1]#bpy.data.movieclips.get()
       
      
        sc = context.space_data
        clip = sc.clip
        scene = context.scene
        #clip.name = bpy.data.movieclips["xtracks"]#"xtracks" #bpy.data.movieclips[0]
        #clip.filepath = "C:\tmp\0001-0036.avi"# bpy.data.movieclips["ytracks"]
        #bpy.ops.clip.open = "C:\tmp\0001-0036.avi"
        bpy.ops.clip.reload = bpy.data.movieclips["xtracks"]
        #bpy.types.MovieClip(bpy.data.movieclips[1])
        print(bpy.data.movieclips["xtracks"].filepath)#c:\tmp\0001-0036.avi
       
        print('Debug.log TestClipVideo')
        return {'FINISHED'}''' 
################################## DO NOT EDIT ###################################################
#------------------------------- Set Camera to "name of camera" (Operator)------------------------
class MotionStudioSetCam(bpy.types.Operator):   
    bl_idname = "object.motionstudiosetcam"  
    bl_label = "Apply XY Motion Tracks"    
    bl_context = "posemode"
    bl_context = "objectmode"
    bl_category = "Motion Studio"
    def execute(self, context): 
        scene = bpy.data.scenes["Scene"]
        
        if scene.camera == bpy.data.objects["ycamera"]:
           scene.camera = bpy.data.objects["xcamera"]
        elif scene.camera == bpy.data.objects["xcamera"]:
             scene.camera = bpy.data.objects["ycamera"]      
        return {'FINISHED'}     
################################################################################################
     
      
      

#------------------------------- Set Camera to "name of camera" (Operator)----------------------------------
class MotionStudioSetClip(bpy.types.Operator):   
    bl_idname = "object.motionstudiosetclip"  
    bl_space_type = 'CLIP_EDITOR'
    bl_label = "Apply XY Motion Tracks"    
    bl_context = "posemode"
    bl_context = "objectmode"
    bl_category = "Motion Studio"
    def execute(self, context): 
        bpy.context.area.type = 'CLIP_EDITOR'
        
        scene = bpy.data.scenes["Scene"]
        sc = context.space_data
        clip = sc.clip
        print(clip)
        YV = bpy.data.movieclips[1]
        XV = bpy.data.movieclips[0]
 
        return {'FINISHED'}   
        
        
        
'''        if clip.name == bpy.data.movieclips["ytracks"]:  
           clip = bpy.data.movieclips["xtracks"]  
        elif clip.name == bpy.data.movieclips["xtracks"]:  
             clip = bpy.data.movieclips["ytracks"]'''
          

          
        
        
       
#***********************************************************************************************************     
#---------------------------- Apply Tracks from both cameras in one shot (Operator) ------------------------
#*********************************************************************************************************** 
#--------------------------****Change movieclip work in progress****----------------------------------------


class MotionStudioApplyXYTracks(bpy.types.Operator):  
    bl_space_type = 'CLIP_EDITOR' #add for tracking
    bl_idname = "object.motionstudioapplyxytracks"  
    bl_label = "Apply XY Motion Tracks"    
    bl_context = "posemode"
    bl_context = "objectmode"
    bl_category = "Motion Studio"

  

    def execute(self, context): 
        bpy.context.area.type = 'CLIP_EDITOR'
        bpy.ops.clip.select_all(action='TOGGLE') #selet all tracks       
        scene = context.scene
        sc = context.space_data
        clip = sc.clip  
#---------------------------Set Camera & Clip----------------------------------------             
        scene.camera = bpy.data.objects["ycamera"] #Set scene camera to "name of came"  
        scene.active_clip = bpy.data.movieclips["ytracks"] #Set clip
#----------------------- Create Empties----------------------------------        
        #bpy.context.area.type = 'CLIP_EDITOR'
        #bpy.ops.clip.select_all(action='TOGGLE') #selet all tracks
        bpy.ops.clip.track_to_empty() #Create empty y-tracks
#--------------------------Constraints Damped Track--------------------------------------        
        bpy.context.area.type = 'VIEW_3D' # Returns to 3dveiw 
        bl_context = "posemode"
        obj = bpy.data.objects["metarig"]
        bpy.context.scene.objects.active = obj
        bpy.ops.object.motiontracksy() #Apply y-tracks to the bones
#----------------------- Create Empties----------------------------------  
        
        bpy.context.area.type = 'CLIP_EDITOR'
        bpy.ops.clip.select_all(action='TOGGLE') #selet all tracks
#---------------------------Set Camera & Clip ----------------------------------------        

        
        scene.camera = bpy.data.objects["xcamera"] #Set scene camera to "name of came"
        scene.active_clip = bpy.data.movieclips["xtracks"]        
#----------------------- Create Empties----------------------------------               
        bpy.ops.clip.track_to_empty() #Create empty x-tracks
#--------------------------Constraints Damped Track--------------------------------------        
        bpy.context.area.type = 'VIEW_3D' # Returns to 3dveiw 
        bl_context = "posemode"
        obj = bpy.data.objects["metarig"]
        bpy.context.scene.objects.active = obj 
        bpy.ops.object.motiontracksx() #Apply x-tracks to the bones﻿       
        bpy.ops.object.mode_set(mode='POSE') #return to pose mode     
        return {'FINISHED'}     
  
     
#***********************************************************************************************************     
#------------------------------------------Constraints (Operator)-----------------------------------------------------
#*********************************************************************************************************** 
class MotionTracksy(bpy.types.Operator):  
    bl_idname = "object.motiontracksy"  #called
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

        #obj = bpy.data.objects["metarig"]
        #bpy.context.scene.objects.active = obj 
        bpy.ops.object.mode_set(mode='POSE')    
        #****************************************************************************************************		
        #---------------------------------------front Camera Empty Damped Tracking-----------------------
        #****************************************************************************************************
        #http://www.blender.org/api/blender_python_api_2_73_release/bpy.types.DampedTrackConstraint.html#bpy.types.DampedTrackConstraint.track_axis
        #[‘TRACK_X’, ‘TRACK_Y’, ‘TRACK_Z’, ‘TRACK_NEGATIVE_X’, ‘TRACK_NEGATIVE_Y’, ‘TRACK_NEGATIVE_Z’], default ‘TRACK_X’
  
        
        #***************************************************************************
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

        #*************************  Fix Me ******************************************************
        #Option 1 divide Track.hips.L x.position and Track.hips.R x.position
        #Opyion 2: Create a hips suit marking and disregard Hips.L/.R data	
        #----------------------------- hips -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['hips'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["hips"].constraints["Damped Track"].target = bpy.data.objects["Track.hip"]
        bpy.context.object.pose.bones["hips"].constraints["Damped Track"].track_axis = 'TRACK_Y'
        
        #******************************************************************************

        
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
        bpy.ops.object.motionhidetracksy('INVOKE_DEFAULT')
        return {'FINISHED'}











#--------------------------------------------Apply x Constraints (Operator)-----------------------------------------
       
class MotionTracksX(bpy.types.Operator):  
    bl_idname = "object.motiontracksx"  #called
    #bl_label = "Motion Tools"  
    #bl_category = "Tools"
    bl_category = "Motion Studio"
    bl_context = "posemode"
    bl_label = "MotionTracks"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context): 

        #obj = bpy.data.objects["metarig"]
        #bpy.context.scene.objects.active = obj 
        bpy.ops.object.mode_set(mode='POSE')    
        #****************************************************************************************************		
        #---------------------------------------front Camera Empty Damped Tracking-----------------------
        #****************************************************************************************************
		
        #----------------------------- thigh.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['thigh.L'].bone
        ActiveBone = bpy.ops.pose  
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["thigh.L"].constraints["Damped Track.001"].target = bpy.data.objects["Track.thigh.L2"]  
        bpy.context.object.pose.bones["thigh.L"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'
        #----------------------------- thigh.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['thigh.R'].bone  
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["thigh.R"].constraints["Damped Track.001"].target = bpy.data.objects["Track.thigh.R2"]   
        bpy.context.object.pose.bones["thigh.R"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'
        #----------------------------- shin.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shin.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shin.L"].constraints["Damped Track.001"].target = bpy.data.objects["Track.shin.L2"] 
        bpy.context.object.pose.bones["shin.L"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'		
        #----------------------------- shin.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shin.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shin.R"].constraints["Damped Track.001"].target = bpy.data.objects["Track.shin.R2"]
        bpy.context.object.pose.bones["shin.R"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'        
        #----------------------------- shoulder.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shoulder.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shoulder.L"].constraints["Damped Track.001"].target = bpy.data.objects["Track.shoulder.L2"] 
        bpy.context.object.pose.bones["shoulder.L"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'		
        #----------------------------- shoulder.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shoulder.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shoulder.R"].constraints["Damped Track.001"].target = bpy.data.objects["Track.shoulder.R2"]
        bpy.context.object.pose.bones["shoulder.R"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'        
        #-----------------------------head -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['head'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["head"].constraints["Damped Track.001"].target = bpy.data.objects["Track.head.2"]
        bpy.context.object.pose.bones["head"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'        
        #----------------------------- neck -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['neck'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["neck"].constraints["Damped Track.001"].target = bpy.data.objects["Track.neck.2"]
        bpy.context.object.pose.bones["neck"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'		
        #----------------------------- chest -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['chest'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["chest"].constraints["Damped Track.001"].target = bpy.data.objects["Track.chest.2"]
        bpy.context.object.pose.bones["chest"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'	
        #----------------------------- spine -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['spine'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["spine"].constraints["Damped Track.001"].target = bpy.data.objects["Track.spine.2"]
        bpy.context.object.pose.bones["spine"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'		
        
       
        #----------------------------- hips -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['hips'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["hips"].constraints["Damped Track.001"].target = bpy.data.objects["Track.hip.2"]
        bpy.context.object.pose.bones["hips"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'
       
        
        
        #----------------------------- upper_arm.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['upper_arm.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["upper_arm.L"].constraints["Damped Track.001"].target = bpy.data.objects["Track.upper_arm.L2"]
        bpy.context.object.pose.bones["upper_arm.L"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'        
        #----------------------------- upper_arm.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['upper_arm.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["upper_arm.R"].constraints["Damped Track.001"].target = bpy.data.objects["Track.upper_arm.R2"]
        bpy.context.object.pose.bones["upper_arm.R"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'		
        #----------------------------- forearm.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['forearm.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["forearm.L"].constraints["Damped Track.001"].target = bpy.data.objects["Track.forearm.L2"]
        bpy.context.object.pose.bones["forearm.L"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'        
        #----------------------------- forearm.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['forearm.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["forearm.R"].constraints["Damped Track.001"].target = bpy.data.objects["Track.forearm.R2"]
        bpy.context.object.pose.bones["forearm.R"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'       
        bpy.ops.object.motionhidetracksx('INVOKE_DEFAULT')
        return {'FINISHED'}  

#******************************************************************************************************       
#--------------------------------------Hide & Delete Tracks -------------------------------------------
#****************************************************************************************************** 
#--------------------------------- Hide Empty y Tracks from Vieport (Operator) ----------------------------
class MotionHideTracksy(bpy.types.Operator):  
    bl_idname = "object.motionhidetracksy" 
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
        bpy.data.objects["Track.hip"].hide = True
        bpy.data.objects["Track.upper_arm.L"].hide = True
        bpy.data.objects["Track.upper_arm.R"].hide = True
        bpy.data.objects["Track.forearm.L"].hide = True
        bpy.data.objects["Track.forearm.R"].hide = True
        return {'FINISHED'}
#----------------------------- Hide Empty x Tracks from Vieport (Operator) ----------------------------
class MotionHideTracksx(bpy.types.Operator):  
    bl_idname = "object.motionhidetracksx"  #called
    bl_category = "Motion Studio"
    bl_context = "posemode"
    bl_label = "MotionTracks"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):         
        #------------------------------------- Xtrack -------------------
        bpy.data.objects["Track.thigh.L2"].hide = True
        bpy.data.objects["Track.thigh.R2"].hide = True  
        bpy.data.objects["Track.shin.L2"].hide = True
        bpy.data.objects["Track.shin.R2"].hide = True
        bpy.data.objects["Track.shoulder.L2"].hide = True
        bpy.data.objects["Track.shoulder.R2"].hide = True
        bpy.data.objects["Track.head.2"].hide = True
        bpy.data.objects["Track.neck.2"].hide = True
        bpy.data.objects["Track.chest.2"].hide = True
        bpy.data.objects["Track.spine.2"].hide = True
        bpy.data.objects["Track.hip.2"].hide = True
        bpy.data.objects["Track.upper_arm.L2"].hide = True
        bpy.data.objects["Track.upper_arm.R2"].hide = True
        bpy.data.objects["Track.forearm.L2"].hide = True
        bpy.data.objects["Track.forearm.R2"].hide = True
        
        return {'FINISHED'}


#------------------------------------------- Hide Empty Tracks from Vieport--------------

class MotiondeleteTracks(bpy.types.Operator):  
    bl_idname = "object.motiondeletetracks"  #called
    bl_category = "Motion Studio"
    bl_context = "posemode"
    bl_label = "MotionTracks"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #bpy.data.objects[object_name].select = True
        #bpy.ops.object.delete() 
        # remove all selected.

        bpy.data.objects["Track.thigh.L"].select = True     
        bpy.data.objects["Track.thigh.R"].select = True  
        bpy.data.objects["Track.shin.L"].select = True
        bpy.data.objects["Track.shin.R"].select = True
        bpy.data.objects["Track.shoulder.L"].select = True
        bpy.data.objects["Track.shoulder.R"].select = True
        bpy.data.objects["Track.head"].select = True
        bpy.data.objects["Track.neck"].select = True
        bpy.data.objects["Track.chest"].select = True
        bpy.data.objects["Track.spine"].select = True
        bpy.data.objects["Track.hip"].select = True
        bpy.data.objects["Track.upper_arm.L"].select = True
        bpy.data.objects["Track.upper_arm.R"].select = True
        bpy.data.objects["Track.forearm.L"].select = True
        bpy.data.objects["Track.forearm.R"].select = True
        
        bpy.data.objects["Track.thigh.L"].hide = False
        bpy.data.objects["Track.thigh.R"].hide = False  
        bpy.data.objects["Track.shin.L"].hide = False
        bpy.data.objects["Track.shin.R"].hide = False
        bpy.data.objects["Track.shoulder.L"].hide = False
        bpy.data.objects["Track.shoulder.R"].hide = False
        bpy.data.objects["Track.head"].hide = False
        bpy.data.objects["Track.neck"].hide = False
        bpy.data.objects["Track.chest"].hide = False
        bpy.data.objects["Track.spine"].hide = False
        bpy.data.objects["Track.hip"].hide = False
        bpy.data.objects["Track.upper_arm.L"].hide = False
        bpy.data.objects["Track.upper_arm.R"].hide = False
        bpy.data.objects["Track.forearm.L"].hide = False
        bpy.data.objects["Track.forearm.R"].hide = False
       
        #------------------------------------- Xtrack -------------------
        bpy.data.objects["Track.thigh.L2"].select = True
        bpy.data.objects["Track.thigh.R2"].select = True  
        bpy.data.objects["Track.shin.L2"].select = True
        bpy.data.objects["Track.shin.R2"].select = True
        bpy.data.objects["Track.shoulder.L2"].select = True
        bpy.data.objects["Track.shoulder.R2"].select = True
        bpy.data.objects["Track.head.2"].select = True
        bpy.data.objects["Track.neck.2"].select = True
        bpy.data.objects["Track.chest.2"].select = True
        bpy.data.objects["Track.spine.2"].select = True
        bpy.data.objects["Track.hip.2"].select = True
        bpy.data.objects["Track.upper_arm.L2"].select = True
        bpy.data.objects["Track.upper_arm.R2"].select = True
        bpy.data.objects["Track.forearm.L2"].select = True
        bpy.data.objects["Track.forearm.R2"].select = True
        
        
        bpy.data.objects["Track.thigh.L2"].hide = False
        bpy.data.objects["Track.thigh.R2"].hide = False  
        bpy.data.objects["Track.shin.L2"].hide = False
        bpy.data.objects["Track.shin.R2"].hide = False
        bpy.data.objects["Track.shoulder.L2"].hide = False
        bpy.data.objects["Track.shoulder.R2"].hide = False
        bpy.data.objects["Track.head.2"].hide = False
        bpy.data.objects["Track.neck.2"].hide = False
        bpy.data.objects["Track.chest.2"].hide = False
        bpy.data.objects["Track.spine.2"].hide = False
        bpy.data.objects["Track.hip.2"].hide = False
        bpy.data.objects["Track.upper_arm.L2"].hide = False
        bpy.data.objects["Track.upper_arm.R2"].hide = False
        bpy.data.objects["Track.forearm.L2"].hide = False
        bpy.data.objects["Track.forearm.R2"].hide = False        

        bpy.ops.object.delete()#delet all selected objects ***MUST NOT BE HIDDEN****
        return {'FINISHED'}    
    
    
#----------------------------------------------Register -----------------------------
#register     http://www.blender.org/api/blender_python_api_2_59_0/info_overview.html   
        
if __name__ == "__main__":  # only for live edit. 
    bpy.utils.register_module(__name__)
    
def register():
     bpy.utils.register_module(__name__)

def unregister():
       bpy.utils.unregister_module(__name__)

print("MotionStudio has loaded")    
    


