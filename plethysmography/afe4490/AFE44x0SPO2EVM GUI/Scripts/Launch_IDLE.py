import idlelib.PyShell
#from idlelib import *
import uuid
#! /usr/bin/env python

import os
import os.path
import sys
import string
import getopt
import re
import socket
import time
import threading
import traceback
import types
import imp
from itertools import cycle

import linecache
from code import InteractiveInterpreter

try:
    from Tkinter import *
except ImportError:
    print>>sys.__stderr__, "** IDLE can't import Tkinter.  " \
                           "Your Python may not be configured for Tk. **"
    sys.exit(1)
import tkMessageBox

from idlelib.EditorWindow import EditorWindow, fixwordbreaks
from idlelib.FileList import FileList
from idlelib.ColorDelegator import ColorDelegator
from idlelib.UndoDelegator import UndoDelegator
from idlelib.OutputWindow import OutputWindow
from idlelib.configHandler import idleConf
from idlelib import idlever
from idlelib import rpc
from idlelib import Debugger
from idlelib import RemoteDebugger
from idlelib import macosxSupport


usage_msg = """\

USAGE: idle  [-deins] [-t title] [file]*
       idle  [-dns] [-t title] (-c cmd | -r file) [arg]*
       idle  [-dns] [-t title] - [arg]*

  -h         print this help message and exit
  -n         run IDLE without a subprocess (see Help/IDLE Help for details)

The following options will override the IDLE 'settings' configuration:

  -e         open an edit window
  -i         open a shell window

The following options imply -i and will open a shell:

  -c cmd     run the command in a shell, or
  -r file    run script from file

  -d         enable the debugger
  -s         run $IDLESTARTUP or $PYTHONSTARTUP before anything else
  -t title   set title of shell window

A default edit window will be bypassed when -c, -r, or - are used.

[arg]* are passed to the command (-c) or script (-r) in sys.argv[1:].

Examples:

idle
        Open an edit window or shell depending on IDLE's configuration.

idle foo.py foobar.py
        Edit the files, also open a shell if configured to start with shell.

idle -est "Baz" foo.py
        Run $IDLESTARTUP or $PYTHONSTARTUP, edit foo.py, and open a shell
        window with the title "Baz".

idle -c "import sys; print sys.argv" "foo"
        Open a shell window and run the command, passing "-c" in sys.argv[0]
        and "foo" in sys.argv[1].

idle -d -s -r foo.py "Hello World"
        Open a shell window, run a startup script, enable the debugger, and
        run foo.py, passing "foo.py" in sys.argv[0] and "Hello World" in
        sys.argv[1].

echo "import sys; print sys.argv" | idle - "foobar"
        Open a shell window, run the script piped in, passing '' in sys.argv[0]
        and "foobar" in sys.argv[1].
"""

original_main=idlelib.PyShell.main

def Launch_IDLE_main():
    #original_main()
    global flist, root, use_subprocess,window_handle,LV_ActiveX

    use_subprocess = True
    enable_shell = True
    enable_edit = False
    debug = False
    cmd = None
    script = None
    startup = False

    idlelib.PyShell.use_subprocess = True
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:del:ihnr:st:")
    except getopt.error, msg:
        sys.stderr.write("Error: %s\n" % str(msg))
        sys.stderr.write(usage_msg)
        sys.exit(2)
    for o, a in opts:
        if o == '-c':
            cmd = a
            enable_shell = True
        if o == '-d':
            debug = True
            enable_shell = True
        if o == '-e':
            enable_edit = True
            enable_shell = False
        if o=='-l':
            enable_edit = True
            enable_shell = False
            create_LabVIEW_ActiveX=True
            LV_ActiveX_Option_Val=a
        if o == '-h':
            sys.stdout.write(usage_msg)
            sys.exit()
        if o == '-i':
            enable_shell = True
        if o == '-n':
            use_subprocess = False
        if o == '-r':
            script = a
            if os.path.isfile(script):
                pass
            else:
                print "No script file: ", script
                sys.exit()
            enable_shell = True
        if o == '-s':
            startup = True
            enable_shell = True
        if o == '-t':
            PyShell.shell_title = a
            enable_shell = True
    if args and args[0] == '-':
        cmd = sys.stdin.read()
        enable_shell = True
    # process sys.argv and sys.path:
    for i in range(len(sys.path)):
        sys.path[i] = os.path.abspath(sys.path[i])
    if args and args[0] == '-':
        sys.argv = [''] + args[1:]
    elif cmd:
        sys.argv = ['-c'] + args
    elif script:
        sys.argv = [script] + args
    elif args:
        enable_edit = True
        pathx = []
        for filename in args:
            pathx.append(os.path.dirname(filename))
        for dir in pathx:
            dir = os.path.abspath(dir)
            if dir not in sys.path:
                sys.path.insert(0, dir)
    else:
        dir = os.getcwd()
        if not dir in sys.path:
            sys.path.insert(0, dir)
    # check the IDLE settings configuration (but command line overrides)
    edit_start = idleConf.GetOption('main', 'General',
                                    'editor-on-startup', type='bool')
    enable_edit = enable_edit or edit_start

    #Start LabVIEW GUI ActiveX Server
    if(create_LabVIEW_ActiveX):
        LV_Options=LV_ActiveX_Option_Val.split(",")
        if(len(LV_Options)<2):
            print "expected 2 arguments but got ", len(LV_Options)
            sys.exit()
        else:
            pass
        LV_Options=LV_ActiveX_Option_Val.split(",")
        GUI_Module_Name=LV_Options[0].strip()
        GUI_Module_Path=LV_Options[1].strip()
        GUI_Module_App_Name=LV_Options[2].strip()
        GUI_Module_Info=imp.find_module(GUI_Module_Name,[GUI_Module_Path])
        GUI_Module=imp.load_module(GUI_Module_Name,GUI_Module_Info[0],GUI_Module_Info[1],GUI_Module_Info[2])
        GUI=GUI_Module.Device_GUI(GUI_Module_App_Name)
        #GUI.create_activex_server()
    
    # start editor and/or shell windows:
    root = Tk(className="Idle")

    fixwordbreaks(root)
    root.withdraw()
    flist = idlelib.PyShell.PyShellFileList(root)
    macosxSupport.setupApp(root, flist)

    if enable_edit:
        if not (cmd or script):
            for filename in args:
                flist.open(filename)
            if not args:
                window_handle=flist.new()
                unique_id=str(uuid.uuid1())
    if enable_shell:
        shell = flist.open_shell()
        if not shell:
            return # couldn't open shell

        if macosxSupport.runningAsOSXApp() and flist.dict:
            # On OSX: when the user has double-clicked on a file that causes
            # IDLE to be launched the shell window will open just in front of
            # the file she wants to see. Lower the interpreter window when
            # there are open files.
            shell.top.lower()

    shell = flist.pyshell
    # handle remaining options:
    if debug:
        shell.open_debugger()
    if startup:
        filename = os.environ.get("IDLESTARTUP") or \
                   os.environ.get("PYTHONSTARTUP")
        if filename and os.path.isfile(filename):
            shell.interp.execfile(filename)
    if shell and cmd or script:
        shell.interp.runcommand("""if 1:
            import sys as _sys
            _sys.argv = %r
            del _sys
            \n""" % (sys.argv,))
        if cmd:
            shell.interp.execsource(cmd)
        elif script:
            shell.interp.prepend_syspath(script)
            shell.interp.execfile(script)
            
    def switch_color():
        active_window=GUI.get_active_IDLE_window()
        if(active_window==unique_id):
            window_handle.text['bg']=next(colors)
        else:
            window_handle.text['bg']='SystemWindow'
        root.after(1000, switch_color)

    #
    def Get_Macro_Script_from_LV_GUI():
        #get the active IDLE window for the GUI
        if((window_handle!=None)):
            active_window=GUI.get_active_IDLE_window()            
            #if current window is active window then get script from the GUI
            if(active_window==unique_id):
                Data=GUI.get_script_from_gui()
                if(Data[0]==False):                    
                    window_handle.text.insert(INSERT,Data[1])             
        root.after(100,Get_Macro_Script_from_LV_GUI)

    if(create_LabVIEW_ActiveX):
        #Notify the GUI that IDLE launched and send the Window ID
        GUI.notify_IDLE_launch(unique_id)       
        #poll the GUI for any new script in the queue
        root.after(100,Get_Macro_Script_from_LV_GUI)
        root.after(500, switch_color)
        print "IDLE window launched. Notification to GUI issued with unique id: "+unique_id
    colors = cycle(['PaleGreen1','SystemWindow'])


        
    root.mainloop()
    root.destroy()
    if(create_LabVIEW_ActiveX):
        print "Recording stopped. Closing IDLE."
        GUI.notify_IDLE_close(unique_id)


idlelib.PyShell.main=Launch_IDLE_main

idlelib.PyShell.main()
