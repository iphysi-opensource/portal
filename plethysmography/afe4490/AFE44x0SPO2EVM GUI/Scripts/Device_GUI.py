import ConfigParser
import string
import os
import ctypes
from ctypes import *

class Device_GUI():

   def __init__(self,GUI_Module_App_Name):
      
      config=ConfigParser.ConfigParser()
      cur_file_path= os.path.split(__file__)
      Application_Root_Path=os.path.split(cur_file_path[0])
      cfg_file_path=os.path.join(Application_Root_Path[0], GUI_Module_App_Name + '.ini')
      cfgfile = open(cfg_file_path)
      config.readfp(cfgfile)
      cfgfile.close()

      Application_Name=config.get(GUI_Module_App_Name,"GUI Application")

      Application_Name=Application_Name.strip("\"")
      self.Application_Is_LabVIEW=ctypes.c_uint(Application_Name=="LabVIEW.exe")
      
      dll_path=os.path.join(Application_Root_Path[0],"Shared Library\Device GUI.dll")
      self.DeviceGUI=cdll.LoadLibrary(dll_path)

      self.GUI_Name=ctypes.create_string_buffer(Application_Name)

   def write_register(self,Block_Name,Register_Name,Data):

      Error_Code=ctypes.c_int(0)
      Register=ctypes.create_string_buffer(Register_Name)
      Block=ctypes.create_string_buffer(Block_Name)
      Data_In=ctypes.c_int64(Data)
      Complete=ctypes.c_uint(0)
      buf=c_char_p(6)
      Err_Str=ctypes.create_string_buffer(1000)
      Err_Str_Len=ctypes.c_int(-1)
      
      self.DeviceGUI.WriteRegister(Data_In,ctypes.byref(Register),ctypes.byref(Block),ctypes.byref(self.GUI_Name),ctypes.byref(Err_Str),ctypes.byref(Error_Code),ctypes.byref(Complete),ctypes.byref(Err_Str_Len))
      if(Error_Code.value!=0 and Error_Code.value!=1073676294):
         raise LabVIEW_Exception(Error_Code.value,Err_Str.value)
      return Complete.value                
   
   def read_register(self,Block_Name,Register_Name):

      Error_Code=ctypes.c_int(0)
      Register=ctypes.create_string_buffer(Register_Name)
      Block=ctypes.create_string_buffer(Block_Name)
      Complete=ctypes.c_uint(0)
      buf=c_char_p(6)
      Err_Str=ctypes.create_string_buffer(1000)
      Err_Str_Len=ctypes.c_int(-1)
      Data=ctypes.c_int()
          
      self.DeviceGUI.ReadRegister(ctypes.byref(Register),ctypes.byref(Block),ctypes.byref(self.GUI_Name),ctypes.byref(Err_Str),ctypes.byref(Error_Code),ctypes.byref(Data),ctypes.byref(Err_Str_Len))
      if(Error_Code.value!=0 and Error_Code.value!=1073676294):
         raise LabVIEW_Exception(Error_Code.value,Err_Str.value)
      return Data.value


#functions from below are used for communication between Python and the GUI. Please do not call these functions in your script

   def get_script_from_gui(self):
      Method=ctypes.c_int(0)
      TimeOut=ctypes.c_int(100)
      TimedOut=ctypes.c_uint(0)
      DataIn=ctypes.create_string_buffer(500)
      DataOut=ctypes.create_string_buffer(500)
      DataOut_Len=ctypes.c_int(-1)
      Error_Code=ctypes.c_int(0)
      Err_Str=ctypes.create_string_buffer(1000)
      Err_Str_Len=ctypes.c_int(-1)

      self.DeviceGUI.GetScriptFromGUI(Method,TimeOut,ctypes.byref(DataIn),ctypes.byref(self.GUI_Name),ctypes.byref(Err_Str),ctypes.byref(Error_Code),ctypes.byref(TimedOut),ctypes.byref(DataOut),ctypes.byref(DataOut_Len),ctypes.byref(Err_Str_Len))
      if(Error_Code.value!=0):
         raise LabVIEW_Exception(Error_Code.value,Err_Str.value)
      return TimedOut.value, DataOut.value

   def get_active_IDLE_window(self):
      Write=ctypes.c_uint(0)
      ActiveWindowIn=ctypes.create_string_buffer(500)
      ActiveWindowOut=ctypes.create_string_buffer(500)
      ActiveWindowOut_Len=ctypes.c_int(-1)
      Error_Code=ctypes.c_int(0)
      Err_Str=ctypes.create_string_buffer(1000)
      Err_Str_Len=ctypes.c_int(-1)

      self.DeviceGUI.GetActiveIDLEWindow(ctypes.byref(Write),ctypes.byref(ActiveWindowIn),ctypes.byref(self.GUI_Name),ctypes.byref(Err_Str),ctypes.byref(Error_Code),ctypes.byref(ActiveWindowOut), ctypes.byref(ActiveWindowOut_Len),ctypes.byref(Err_Str_Len))
      if(Error_Code.value!=0):
         raise LabVIEW_Exception(Error_Code.value,Err_Str.value)
      return ActiveWindowOut.value

   def notify_IDLE_launch(self,window_id):
      Write=ctypes.c_uint(0)
      ResponseNotifier=ctypes.create_string_buffer("launch_idle")
      WindowID=ctypes.create_string_buffer(window_id)
      Error_Code=ctypes.c_int(0)
      Err_Str=ctypes.create_string_buffer(1000)
      Err_Str_Len=ctypes.c_int(-1)

      self.DeviceGUI.NotifyIDLELaunch(ctypes.byref(WindowID),ctypes.byref(ResponseNotifier),ctypes.byref(self.GUI_Name), ctypes.byref(Err_Str),ctypes.byref(Error_Code),ctypes.byref(Err_Str_Len))
      if(Error_Code.value!=0):
         raise LabVIEW_Exception(Error_Code.value,Err_Str.value)      
            
   def notify_IDLE_close(self,window_id):
      IDLE_Window_ID=ctypes.create_string_buffer(window_id)          
      Error_Code=ctypes.c_int(0)
      Err_Str=ctypes.create_string_buffer(1000)
      Err_Str_Len=ctypes.c_int(-1)
      self.DeviceGUI.NotifyIDLEClose(ctypes.byref(IDLE_Window_ID),ctypes.byref(self.GUI_Name), ctypes.byref(Err_Str),ctypes.byref(Error_Code),ctypes.byref(Err_Str_Len))
      if(Error_Code.value!=0):
         raise LabVIEW_Exception(Error_Code,Err_Str.value)
      
   def __del__(self):
      #
      print "Script completed sucessfully"


class LabVIEW_Exception(Exception):
    """class for exceptions returned from LabVIEW
These errors could be both instrument error as well as LabVIEW errors"""
    pass
      
  
