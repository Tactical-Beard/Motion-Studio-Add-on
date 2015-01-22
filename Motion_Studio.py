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
from mathutils import Vector
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
    bl_description = "Object mode panel buttons"
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
        layout.operator("object.motionvectorlocation", text="Apply Vector", icon='CONSTRAINT_BONE')
        
#------------------------------- Add Metrig And 3D Cursor To Center (Operator)---------------------------------------- 
class MotionTracksAddMetaRigToCenter(bpy.types.Operator):
    bl_idname = "object.snap_cursor_center_armature_human_metarig_add" 
    bl_label = "Center"#has to have a label 
    bl_description = "Snaps the 3d cursor to center and then creates an armature at the 3d cursor."  
    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.object.armature_human_metarig_add()
        return{'FINISHED'}
#------------------------------- Add Armature Objectmode----------------------------------------     
class MoionLibaryImport(View3DPanel, Panel):
    bl_label = "Motion Libary"
    bl_context = "objectmode"
    bl_category = "Motion Studio"
    bl_description = "Imports .fbx files"

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
    bl_description = "Sets rig to a t-pose"

    @staticmethod
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Draw:")
        layout.operator("mcp.set_t_pose", text="Set T-pose", icon='OUTLINER_DATA_ARMATURE')
        layout.operator("object.moionstudioapplyrestpose", text="Set Rest Pose", icon='MOD_ARMATURE')
        #layout.operator("mcp.rest_current_pose", text="Reset Rest Pose", icon='MOD_ARMATURE')

#------------------------------- Clear Pose to Rest Pose (Operator)----------------------------------------     
class MoionStudioApplyRestPose(bpy.types.Operator):
    bl_idname = "object.moionstudioapplyrestpose"
    bl_label = "Motion Studio"
    #bl_context = "posemode"
    bl_category = "Motion Studio"
    bl_description = "Clears pose rotations aka rest pose for metarig"
            
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
    bl_description = "Loads and retargets .bvh files"
        
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
    bl_description = "Deletes current keyframe"
    
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
    bl_description = "Deletes all keyframes"
    #bl_options = {'REGISTER', 'UNDO'}
    bl_description = ""
    
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
    bl_description = "Pose mode tool panel buttons."
    
    def draw(self, context): 
        layout = self.layout
        col = layout.column(align=True)
        layout.operator("object.motionstudioapplyxytracks", text="Apply Tracks", icon='POSE_HLT')
        col = layout.column(align=True)
        col = layout.column(align=True)
        '''
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
        '''
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)   
        #layout.operator("object.motionstudiosetcam", text="Toggle Camera", icon='CAMERA_DATA')#Toggle Scene Camera 
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
    bl_description = "Movie Clip Editor Tool panel buttons."
    
    def draw(self, context): 
        layout = self.layout
        col = layout.column(align=True)
        layout.operator("object.motionstudioapplyxytracks", text="Apply All Tracks", icon='PLAY')
        

        
        #layout.operator("object.motiontracks", text="Apply Tracks", icon='ANIM_DATA')
        #print ("Animation Tracks Removed")
        #layout.operator("object.motiontracks", text="Unapply Tracks", icon='CANCEL')
        #print ("Animation Tracks Removed")
        layout.operator("object.motiontrackstoemptys", text="Apply Live Track", icon='REC')
        #layout.operator("object.livemotiontracks", text="Apply Live Track", icon='REC')
       
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        #layout.operator("object.testclipvideo", text="testclipvideo", icon='CAMERA_DATA')
      
        layout.operator("object.motionstudiosetmovieclip", text="Switch Clip/Cam", icon='CAMERA_DATA')
#**********************************************************************************************
'''
#------------------------------- Create Empties And Apply Tracks Y (Operator)----------------------------------------     

class MotionTracksToEmptys(bpy.types.Operator):  
    bl_space_type = 'CLIP_EDITOR' #add for tracking
    bl_idname = "object.motiontrackstoemptys"  
    bl_label = "Apply Motion Tracks"    
    bl_context = "posemode"
    bl_context = "objectmode"
    bl_category = "Motion Studio"
    bl_description = "Links empties with motion tracks on the y."
  

    def execute(self, context): 
        bpy.context.area.type = 'CLIP_EDITOR'
        bpy.ops.clip.select_all(action='TOGGLE') #selet all tracks
        scene = context.scene
        scene.camera = bpy.data.objects["ycamera"] #Set scene camera to "name of came"
        scene.active_clip = bpy.data.movieclips["ytracks"]
        bpy.ops.clip.track_to_empty() # create tracked emptys 
          

        
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
    bl_description = "Links empties with motion tracks on the x."
  

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
#-------------------------------------------Change movieclip in Movie Clip Editor (Operator)-----------------------------------------------       
class TestClipVideo(bpy.types.Operator):  
    bl_space_type = 'CLIP_EDITOR' #add for tracking
    bl_idname = "object.testclipvideo"  
    bl_label = "Apply Motion Tracks"    
    bl_context = "posemode"
    bl_context = "objectmode"
    bl_category = "Motion Studio"
    ### Button in movie clip editor ###
    def execute(self, context): 
        bpy.context.area.type = 'CLIP_EDITOR'    
        bpy.context.space_data.clip = bpy.data.movieclips[0] #taking the first clip  Works
        print('Debug.log TestClipVideo')
        return {'FINISHED'}
    
'''    
    
################################## DO NOT EDIT ###################################################
#------------------------------- Camera and active clip has been switched 'VIEW_3D' (Operator)------------------------
class MotionStudioSetCam(bpy.types.Operator):   
    bl_idname = "object.motionstudiosetcam"  
    bl_label = "Apply XY Motion Tracks"    
    bl_context = "posemode"
    bl_context = "objectmode"
    bl_category = "Motion Studio"
    bl_description = "Toggles between scene camera/active clip from xcamera/xtracks and ycamera/ytracks."
    def execute(self, context): 
        bpy.context.area.type = 'VIEW_3D'   
        scene = bpy.data.scenes["Scene"]
        bl_space_type = 'CLIP_EDITOR'
        if scene.camera == bpy.data.objects["ycamera"]:
           scene.camera = bpy.data.objects["xcamera"]
           scene.active_clip = bpy.data.movieclips["xtracks"]
           bl_space_type = 'CLIP_EDITOR'
           bpy.context.area.type = 'CLIP_EDITOR'   
           bpy.context.space_data.clip = bpy.data.movieclips[0] #Set clip 
           bpy.context.area.type = 'VIEW_3D'   
        elif scene.camera == bpy.data.objects["xcamera"]:
             scene.camera = bpy.data.objects["ycamera"]    
             scene.active_clip = bpy.data.movieclips["ytracks"]
             bl_space_type = 'CLIP_EDITOR'
             bpy.context.area.type = 'CLIP_EDITOR'        
             bpy.context.space_data.clip = bpy.data.movieclips[1] #Set clip 
             bpy.context.area.type = 'VIEW_3D'     
             self.report({'INFO'}, "Camera and active clip has been switched")
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
    bl_description = "Changes the name of the camera."
    def execute(self, context): 
        bpy.context.area.type = 'CLIP_EDITOR'
        
        scene = bpy.data.scenes["Scene"]
        if scene.camera.name == "xxxxxxxx":
           scene.camera.name = ""
           return {'FINISHED'}      
    
################################## DO NOT EDIT ###################################################
#------------------------------- Camera and active clip has been switched 'CLIP_EDITOR'  (Operator)------------------------
class MotionStudioSetMovieClip(bpy.types.Operator):   
    bl_idname = "object.motionstudiosetmovieclip"  
    bl_label = "Apply XY Motion Tracks"    
    bl_context = "posemode"
    bl_context = "objectmode"
    bl_category = "Motion Studio"
    bl_description = "Toggles between scene camera/active clip from xcamera/xtracks and ycamera/ytracks."
    def execute(self, context): 
        bpy.context.area.type = 'CLIP_EDITOR'
        scene = bpy.data.scenes["Scene"]
        
        if scene.camera == bpy.data.objects["ycamera"]:
           scene.camera = bpy.data.objects["xcamera"]
           scene.active_clip = bpy.data.movieclips["xtracks"]
           
           bpy.context.space_data.clip = bpy.data.movieclips[0] #Set clip
        elif scene.camera == bpy.data.objects["xcamera"]:
             scene.camera = bpy.data.objects["ycamera"] 
             scene.active_clip = bpy.data.movieclips["ytracks"]
             bpy.context.space_data.clip = bpy.data.movieclips[1] #Set clip      
             self.report({'INFO'}, "Camera and active clip has been switched")
        return {'FINISHED'}     
################################################################################################
  
          
        
        
       
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
    bl_description = "Links empties to tracks and then calls to apply them to bones in the x and y."
  
    def execute(self, context): 
        bpy.context.area.type = 'CLIP_EDITOR'
        bpy.ops.clip.select_all(action='TOGGLE') #selet all tracks       
        scene = context.scene
        sc = context.space_data
        clip = sc.clip  
        if scene.camera == bpy.data.objects["xcamera"]:
             scene.camera = bpy.data.objects["ycamera"] 
             scene.active_clip = bpy.data.movieclips["ytracks"]
             bpy.context.space_data.clip = bpy.data.movieclips[1] #Set clip   
       
       
#---------------------------Set Camera & Clip----------------------------------------             
        scene.camera = bpy.data.objects["ycamera"] #Set scene camera to "name of came"
        bpy.context.space_data.clip = bpy.data.movieclips[1] #Set clip in movie clip editor  
        scene.active_clip = bpy.data.movieclips["ytracks"]#Set clip
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
        bpy.context.space_data.clip = bpy.data.movieclips[0] #Set clip in movie clip editor
        scene.active_clip = bpy.data.movieclips["xtracks"] #Set clip in scene      
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
    bl_description = "Selects each bone then adds a damped track constraint."
    @staticmethod
    def execute(self, context): 
        #print(self)
        #print(dir(self))
        #print(context)
        #print(dir(context))

        obj = bpy.data.objects["metarig"]
        bpy.context.scene.objects.active = obj 
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
        bpy.context.object.pose.bones["thigh.L"].constraints["Damped Track"].influence  = 0.5 
        #----------------------------- thigh.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['thigh.R'].bone  
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["thigh.R"].constraints["Damped Track"].target = bpy.data.objects["Track.thigh.R"]   
        bpy.context.object.pose.bones["thigh.R"].constraints["Damped Track"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["thigh.R"].constraints["Damped Track"].influence  = 0.5 
        #----------------------------- shin.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shin.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shin.L"].constraints["Damped Track"].target = bpy.data.objects["Track.shin.L"] 
        bpy.context.object.pose.bones["shin.L"].constraints["Damped Track"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["shin.L"].constraints["Damped Track"].influence  = 0.5 		
        #----------------------------- shin.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shin.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shin.R"].constraints["Damped Track"].target = bpy.data.objects["Track.shin.R"]
        bpy.context.object.pose.bones["shin.R"].constraints["Damped Track"].track_axis = 'TRACK_Y' 
        bpy.context.object.pose.bones["shin.R"].constraints["Damped Track"].influence  = 0.5        
        #----------------------------- shoulder.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shoulder.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shoulder.L"].constraints["Damped Track"].target = bpy.data.objects["Track.shoulder.L"] 
        bpy.context.object.pose.bones["shoulder.L"].constraints["Damped Track"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["shoulder.L"].constraints["Damped Track"].influence  = 0.5 		
        #----------------------------- shoulder.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shoulder.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shoulder.R"].constraints["Damped Track"].target = bpy.data.objects["Track.shoulder.R"]
        bpy.context.object.pose.bones["shoulder.R"].constraints["Damped Track"].track_axis = 'TRACK_Y' 
        bpy.context.object.pose.bones["shoulder.R"].constraints["Damped Track"].influence  = 0.5        
        #-----------------------------head -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['head'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["head"].constraints["Damped Track"].target = bpy.data.objects["Track.head"]
        bpy.context.object.pose.bones["head"].constraints["Damped Track"].track_axis = 'TRACK_Y' 
        bpy.context.object.pose.bones["head"].constraints["Damped Track"].influence  = 0.5        
        #----------------------------- neck -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['neck'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["neck"].constraints["Damped Track"].target = bpy.data.objects["Track.neck"]
        bpy.context.object.pose.bones["neck"].constraints["Damped Track"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["neck"].constraints["Damped Track"].influence  = 0.5 		
        #----------------------------- chest -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['chest'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["chest"].constraints["Damped Track"].target = bpy.data.objects["Track.chest"]
        bpy.context.object.pose.bones["chest"].constraints["Damped Track"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["chest"].constraints["Damped Track"].influence  = 0.5 	
        #----------------------------- spine -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['spine'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["spine"].constraints["Damped Track"].target = bpy.data.objects["Track.spine"]
        bpy.context.object.pose.bones["spine"].constraints["Damped Track"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["spine"].constraints["Damped Track"].influence  = 0.5 

        #*************************  Fix Me ******************************************************
        #Option 1 divide Track.hips.L x.position and Track.hips.R x.position
        #Opyion 2: Create a hips suit marking and disregard Hips.L/.R data	
        #----------------------------- hips -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['hips'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["hips"].constraints["Damped Track"].target = bpy.data.objects["Track.hip"]
        bpy.context.object.pose.bones["hips"].constraints["Damped Track"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["hips"].constraints["Damped Track"].influence  = 0.5 
        
        #******************************************************************************

        
        #----------------------------- upper_arm.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['upper_arm.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["upper_arm.L"].constraints["Damped Track"].target = bpy.data.objects["Track.upper_arm.L"]
        bpy.context.object.pose.bones["upper_arm.L"].constraints["Damped Track"].track_axis = 'TRACK_Y' 
        bpy.context.object.pose.bones["upper_arm.L"].constraints["Damped Track"].influence  = 0.5        
        #----------------------------- upper_arm.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['upper_arm.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["upper_arm.R"].constraints["Damped Track"].target = bpy.data.objects["Track.upper_arm.R"]
        bpy.context.object.pose.bones["upper_arm.R"].constraints["Damped Track"].track_axis = 'TRACK_Y'	
        bpy.context.object.pose.bones["upper_arm.R"].constraints["Damped Track"].influence  = 0.5 	
        #----------------------------- forearm.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['forearm.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["forearm.L"].constraints["Damped Track"].target = bpy.data.objects["Track.forearm.L"]
        bpy.context.object.pose.bones["forearm.L"].constraints["Damped Track"].track_axis = 'TRACK_Y' 
        bpy.context.object.pose.bones["forearm.L"].constraints["Damped Track"].influence  = 0.5        
        #----------------------------- forearm.R ------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['forearm.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["forearm.R"].constraints["Damped Track"].target = bpy.data.objects["Track.forearm.R"]
        bpy.context.object.pose.bones["forearm.R"].constraints["Damped Track"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["forearm.R"].constraints["Damped Track"].influence  = 0.5 
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
    bl_description = "Selects each bone then adds a damped track constraint."
    @staticmethod
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
        bpy.context.object.pose.bones["thigh.L"].constraints["Damped Track.001"].influence  = 0.5 
        #----------------------------- thigh.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['thigh.R'].bone  
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["thigh.R"].constraints["Damped Track.001"].target = bpy.data.objects["Track.thigh.R2"]   
        bpy.context.object.pose.bones["thigh.R"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["thigh.R"].constraints["Damped Track.001"].influence  = 0.5 
        #----------------------------- shin.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shin.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shin.L"].constraints["Damped Track.001"].target = bpy.data.objects["Track.shin.L2"] 
        bpy.context.object.pose.bones["shin.L"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'	
        bpy.context.object.pose.bones["shin.L"].constraints["Damped Track.001"].influence  = 0.5 	
        #----------------------------- shin.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shin.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shin.R"].constraints["Damped Track.001"].target = bpy.data.objects["Track.shin.R2"]
        bpy.context.object.pose.bones["shin.R"].constraints["Damped Track.001"].track_axis = 'TRACK_Y' 
        bpy.context.object.pose.bones["shin.R"].constraints["Damped Track.001"].influence  = 0.5        
        #----------------------------- shoulder.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shoulder.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shoulder.L"].constraints["Damped Track.001"].target = bpy.data.objects["Track.shoulder.L2"] 
        bpy.context.object.pose.bones["shoulder.L"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["shoulder.L"].constraints["Damped Track.001"].influence  = 0.5 		
        #----------------------------- shoulder.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['shoulder.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["shoulder.R"].constraints["Damped Track.001"].target = bpy.data.objects["Track.shoulder.R2"]
        bpy.context.object.pose.bones["shoulder.R"].constraints["Damped Track.001"].track_axis = 'TRACK_Y' 
        bpy.context.object.pose.bones["shoulder.R"].constraints["Damped Track.001"].influence  = 0.5        
        #-----------------------------head -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['head'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["head"].constraints["Damped Track.001"].target = bpy.data.objects["Track.head.2"]
        bpy.context.object.pose.bones["head"].constraints["Damped Track.001"].track_axis = 'TRACK_Y' 
        bpy.context.object.pose.bones["head"].constraints["Damped Track.001"].influence  = 0.5        
        #----------------------------- neck -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['neck'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["neck"].constraints["Damped Track.001"].target = bpy.data.objects["Track.neck.2"]
        bpy.context.object.pose.bones["neck"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["neck"].constraints["Damped Track.001"].influence  = 0.5 		
        #----------------------------- chest -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['chest'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["chest"].constraints["Damped Track.001"].target = bpy.data.objects["Track.chest.2"]
        bpy.context.object.pose.bones["chest"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["chest"].constraints["Damped Track.001"].influence  = 0.5 	
        #----------------------------- spine -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['spine'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["spine"].constraints["Damped Track.001"].target = bpy.data.objects["Track.spine.2"]
        bpy.context.object.pose.bones["spine"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'		
        bpy.context.object.pose.bones["spine"].constraints["Damped Track.001"].influence  = 0.5 
       
        #----------------------------- hips -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['hips'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["hips"].constraints["Damped Track.001"].target = bpy.data.objects["Track.hip.2"]
        bpy.context.object.pose.bones["hips"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["hips"].constraints["Damped Track.001"].influence  = 0.5 
        
        
        #----------------------------- upper_arm.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['upper_arm.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["upper_arm.L"].constraints["Damped Track.001"].target = bpy.data.objects["Track.upper_arm.L2"]
        bpy.context.object.pose.bones["upper_arm.L"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["upper_arm.L"].constraints["Damped Track.001"].influence  = 0.5         
        #----------------------------- upper_arm.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['upper_arm.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["upper_arm.R"].constraints["Damped Track.001"].target = bpy.data.objects["Track.upper_arm.R2"]
        bpy.context.object.pose.bones["upper_arm.R"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["upper_arm.R"].constraints["Damped Track.001"].influence  = 0.5 		
        #----------------------------- forearm.L -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['forearm.L'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["forearm.L"].constraints["Damped Track.001"].target = bpy.data.objects["Track.forearm.L2"]
        bpy.context.object.pose.bones["forearm.L"].constraints["Damped Track.001"].track_axis = 'TRACK_Y'
        bpy.context.object.pose.bones["forearm.L"].constraints["Damped Track.001"].influence  = 0.5         
        #----------------------------- forearm.R -------------------------------------------------------------
        bpy.data.objects["metarig"].data.bones.active = bpy.data.objects["metarig"].pose.bones['forearm.R'].bone     
        ActiveBone.constraint_add(type='DAMPED_TRACK')
        context.object.pose.bones["forearm.R"].constraints["Damped Track.001"].target = bpy.data.objects["Track.forearm.R2"]
        bpy.context.object.pose.bones["forearm.R"].constraints["Damped Track.001"].track_axis = 'TRACK_Y' 
        bpy.context.object.pose.bones["forearm.R"].constraints["Damped Track.001"].influence  = 0.5 
        bpy.ops.object.motionhidetracksx('INVOKE_DEFAULT')
        bpy.context.area.type = 'CLIP_EDITOR'
        scene = context.scene
        sc = context.space_data
        clip = sc.clip  
        if scene.camera == bpy.data.objects["xcamera"]:
           scene.camera = bpy.data.objects["ycamera"] 
           scene.active_clip = bpy.data.movieclips["ytracks"]
           
           bpy.context.space_data.clip = bpy.data.movieclips[1] #Set clip  
           bpy.context.area.type = 'VIEW_3D' 
           return {'FINISHED'}  



#******************************************************************************************************       
#-------------------------------------- Vector 3 location-------------------------------------------
#****************************************************************************************************** 
#--------------------------------- Hide Empty y Tracks from Vieport (Operator) ----------------------------

class MotionVectorLocation(bpy.types.Operator):  
    bl_idname = "object.motionvectorlocation" 
    bl_category = "Motion Studio"
    bl_context = "objectmode"
    bl_label = "MotionTracks"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Hides empty tracks."
    def execute(self, context): 
        vec_1 = bpy.data.objects["Sphere"].location
        #vec_1 = Vector((0,-1,0))
        bpy.data.objects["Cube"].location = vec_1  
        
        return {'FINISHED'}  




#******************************************************************************************************       
#-------------------------------------- Clamp Animation location-------------------------------------------
#****************************************************************************************************** 
#--------------------------------- Hide Empty y Tracks from Vieport (Operator) ----------------------------
class MotionStudioObjectssModePanel(View3DPanel, Panel):
    bl_label = "Clamp Pose"
    bl_context = "posemode"
    bl_category = "Motion Studio"
    bl_description = "Clamps all bones by axis."
    @staticmethod
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Human Rigs:")

    def draw(self, context):
        layout = self.layout


       
        row = layout.row()
        col = row.column()
        #lbx = col.box()
        col.label(text="Human Rigs:")
        #col.prop(bpy.data.objects["metarig"], "location")
        layout.operator("object.motionvectorlocation", text="Clamp", icon="CONSTRAINT_BONE")
        #col.prop(bpy.data.objects["metarig"], "track_axis")
       # col.prop(bpy.data.objects["metarig"], "hide", text="Hide")
        layout.operator("object.motionhidemarkerrig", text="Hide MarkerRig", icon="VISIBLE_IPO_ON")
        
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)
        col = layout.column(align=True)   
        #col.prop(bpy.data.objects["metarig"], "select")# use for armature selection ui
        pyramide_panel_layout = self.layout.column(align = True)
        pyramide_panel_layout.prop( context.scene, 'pyramide_height' ) # draw input field for pyramide's height
        pyramide_panel_layout.prop( context.scene, 'pyramide_width' ) # draw input field for pyramide's width
        pyramide_panel_layout.operator("object.motionhidemarkerrig", text = "Build!") # draw Build! button
        col.prop(bpy.data.objects["metarig"], "pose_library")
class MotionHideMarkerRig(bpy.types.Operator):  
    bl_idname = "object.motionhidemarkerrig" 
    bl_category = "Motion Studio"
    bl_context = "posemode"
    bl_label = "MotionTracks"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Hides empty tracks."
    
    def execute(self, context):   
        if bpy.data.objects["marker.thigh.L"].hide == False:        
           bpy.data.objects["marker.thigh.L"].hide = True
           bpy.data.objects["marker.thigh.R"].hide = True  
           bpy.data.objects["marker.shin.L"].hide = True
           bpy.data.objects["marker.shin.R"].hide = True
           bpy.data.objects["marker.shoulder.L"].hide = True
           bpy.data.objects["marker.shoulder.R"].hide = True
           bpy.data.objects["marker.head"].hide = True
           bpy.data.objects["marker.neck"].hide = True
           bpy.data.objects["marker.chest"].hide = True
           bpy.data.objects["marker.spine"].hide = True
           bpy.data.objects["marker.hip"].hide = True
           bpy.data.objects["marker.upper_arm.L"].hide = True
           bpy.data.objects["marker.upper_arm.R"].hide = True
           bpy.data.objects["marker.forearm.L"].hide = True
           bpy.data.objects["marker.forearm.R"].hide = True          
           return {'FINISHED'}
        
        elif bpy.data.objects["marker.thigh.L"].hide == True:
             bpy.data.objects["marker.thigh.L"].hide = False
             bpy.data.objects["marker.thigh.R"].hide = False  
             bpy.data.objects["marker.shin.L"].hide = False
             bpy.data.objects["marker.shin.R"].hide = False
             bpy.data.objects["marker.shoulder.L"].hide = False
             bpy.data.objects["marker.shoulder.R"].hide = False
             bpy.data.objects["marker.head"].hide = False
             bpy.data.objects["marker.neck"].hide = False
             bpy.data.objects["marker.chest"].hide = False
             bpy.data.objects["marker.spine"].hide = False
             bpy.data.objects["marker.hip"].hide = False
             bpy.data.objects["marker.upper_arm.L"].hide = False
             bpy.data.objects["marker.upper_arm.R"].hide = False
             bpy.data.objects["marker.forearm.L"].hide = False
             bpy.data.objects["marker.forearm.R"].hide = False
             return {'FINISHED'}
        
        
        
        
        
        
        
        
        
        
        
class MotionVectorLocation(bpy.types.Operator):  
    bl_idname = "object.motionvectorlocation" 
    bl_category = "Motion Studio"
    bl_context = "objectmode"
    bl_label = "MotionTracks"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Hides empty tracks."
    def execute(self, context):
        bpy.context.area.type = 'VIEW_3D'  
        
        vec_text = bpy.data.objects["Sphere"].location
        #vec_text = Vector((0,-1,0))
        obj = bpy.data.objects["metarig"]
        bpy.context.scene.objects.active = obj 
        bpy.ops.object.mode_set(mode='POSE')    
        
        
        clamPos  = Vector((0,0,0.5))
        aPos11 = context.object.pose.bones["hips"].location
        '''               
        aPos1  = context.object.pose.bones["thigh.L"].location
        aPos2  = context.object.pose.bones["thigh.R"].location  
        aPos3  = context.object.pose.bones["shin.L"].location
        aPos4  = context.object.pose.bones["shin.R"].location
        aPos5  = context.object.pose.bones["shoulder.L"].location
        aPos6  = context.object.pose.bones["shoulder.R"].location
        aPos7  = context.object.pose.bones["head"].location
        aPos8  = context.object.pose.bones["neck"].location
        aPos9  = context.object.pose.bones["chest"].location
        aPos10 = context.object.pose.bones["spine"].location
        aPos11 = context.object.pose.bones["hips"].location
        aPos12 = context.object.pose.bones["upper_arm.L"].location
        aPos13 = context.object.pose.bones["upper_arm.R"].location
        aPos14 = context.object.pose.bones["forearm.L"].location
        aPos15 = context.object.pose.bones["forearm.R"].location
        

        vec_1  =   Vector((aPos1.x + clamPos.x,  aPos1.y   + clamPos.y, aPos1.z   + clamPos.z))
        vec_2  =   Vector((aPos2.x+ clamPos.x,  aPos2.y   + clamPos.y, aPos2.z  + clamPos.z))
        vec_3 =    Vector((aPos3.x+ clamPos.x,  aPos3.y   + clamPos.y, aPos3.z  + clamPos.z))
        vec_4  =   Vector((aPos4.x+ clamPos.x,  aPos4.y   + clamPos.y, aPos4.z  + clamPos.z))
        vec_5  =   Vector((aPos5.x+ clamPos.x,  aPos5.y   + clamPos.y, aPos5.z  + clamPos.z))
        vec_6  =   Vector((aPos6.x+ clamPos.x,  aPos6.y   + clamPos.y, aPos6.z  + clamPos.z))
        vec_7  =   Vector((aPos7.x+ clamPos.x,  aPos7.y   + clamPos.y, aPos7.z  + clamPos.z))
        vec_8  =   Vector((aPos8.x+ clamPos.x,  aPos8.y   + clamPos.y, aPos8.z  + clamPos.z))
        vec_9  =   Vector((aPos9.x+ clamPos.x,  aPos9.y   + clamPos.y, aPos9.z  + clamPos.z))
        vec_10  = Vector((aPos10.x + clamPos.x,  aPos10.y  + clamPos.y, aPos10.z  + clamPos.z))
        vec_11  = Vector((aPos11.x + clamPos.x,  aPos11.y  + clamPos.y, aPos11.z  + clamPos.z))
        vec_12  = Vector((aPos12.x + clamPos.x,  aPos12.y  + clamPos.y, aPos12.z  + clamPos.z))
        vec_13  = Vector((aPos13.x + clamPos.x,  aPos13.y  + clamPos.y, aPos13.z  + clamPos.z))
        vec_14  = Vector((aPos14.x + clamPos.x,  aPos14.y  + clamPos.y, aPos14.z  + clamPos.z))
        vec_15  = Vector((aPos15.x + clamPos.x,  aPos15.y  + clamPos.y, aPos15.z  + clamPos.z))
        
        bpy.data.objects["Cube"].location = vec_text 
        context.object.pose.bones["thigh.L"].location = vec_1 
        context.object.pose.bones["thigh.R"].location = vec_2  
        context.object.pose.bones["shin.L"].location = vec_3
        context.object.pose.bones["shin.R"].location = vec_4
        context.object.pose.bones["shoulder.L"].location = vec_5
        context.object.pose.bones["shoulder.R"].location = vec_6
        context.object.pose.bones["head"].location = vec_7
        context.object.pose.bones["neck"].location = vec_8
        context.object.pose.bones["chest"].location = vec_9
        context.object.pose.bones["spine"].location = vec_10
        context.object.pose.bones["hips"].location = vec_11
        context.object.pose.bones["upper_arm.L"].location = vec_12
        context.object.pose.bones["upper_arm.R"].location = vec_13
        context.object.pose.bones["forearm.L"].location = vec_14
        context.object.pose.bones["forearm.R"].location = vec_15
        '''
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
    bl_description = "Hides empty tracks."
    
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
    bl_description = "Hides empty tracks."
    
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
    bl_description = "Selects and unhides empty tracks before deleting them."
    
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
    

