import ctypes
import platform
import os

system = platform.system()

# Load the shared library
if (system == "Linux"):
    lib_extension = ".so"
elif (system == "Darwin"):  # macOS
    lib_extension = ".dylib"
elif (system == "Windows"):
    lib_extension = ".dll"
else:
    raise Exception("Unsupported platform: {}".format(system))

# Construct the path to the shared library
lib_path = os.path.join(os.path.dirname(__file__), "libRGFW" + lib_extension)

# Load the shared library
lib = ctypes.CDLL(lib_path)
from ctypes import Structure, POINTER, CFUNCTYPE, c_char_p, c_int, c_uint, c_double, c_void_p, c_uint32, c_uint64, c_char, c_uint16, c_uint8, c_int32, c_float, cdll

class vector(Structure):
    _fields_ = [("x", c_int32), ("y", c_int32)]

class rect(Structure):
    _fields_ = [("x", c_int32), ("y", c_int32), ("w", c_int32), ("h", c_int32)]

class area(Structure):
    _fields_ = [("w", c_uint), ("h", c_uint)]

class monitor(Structure):
    _fields_ = [("name", c_char_p), ("rect", rect), ("scaleX", c_float), ("scaleY", c_float), ("physW", c_float), ("physH", c_float)]

class Event(Structure):
    _fields_ = [("keyName", c_char * 16), 
                ("droppedFiles", ((c_char * 260) * 260)), 
                ("droppedFilesCount", c_uint32), 
                ("type", c_uint32), 
                ("point", vector), 
                ("keyCode", c_uint32), 
                ("fps", c_uint32), 
                ("frameTime", c_uint64), 
                ("frameTime2", c_uint64), 
                ("inFocus", c_uint8), 
                ("lockState", c_uint8), 
                ("joystick", c_uint16), 
                ("button", c_uint8), 
                ("scroll", c_double), 
                ("axisesCount", c_uint8), 
                ("axis", vector * 2)]



class window_src(Structure):
    if (system == "Linux"):
        _fields_ = [
            ("display", ctypes.c_void_p),
            ("window", ctypes.c_void_p),
            ("rSurf", ctypes.c_void_p),
            ("bitmap", ctypes.c_void_p),
            ("jsPressed", (ctypes.c_uint8 * 16) * 4),
            ("joysticks", ctypes.c_int32 * 4),
            ("joystickCount", ctypes.c_uint16),
            ("scale", area),
            ("winArgs", ctypes.c_uint32)
        ]
    elif (system == "Darwin"):  # macOS
        _fields_ = [
            ("display", ctypes.c_uint32),
            ("displayLink", ctypes.c_void_p),
            ("window", ctypes.c_void_p),
            ("rSurf", ctypes.c_void_p),
            ("view", ctypes.c_void_p),
            ("jsPressed", ctypes.c_uint8 * (4 * 16)),
            ("joysticks", ctypes.c_int32 * 4),
            ("joystickCount", ctypes.c_uint16),
            ("scale", area),
            ("cursorChanged", ctypes.c_uint8),
            ("winArgs", ctypes.c_uint32)
        ]
    elif (system == "Windows"):
        _fields_ = [
            ("window", ctypes.c_void_p),
            ("hdc", ctypes.c_void_p),
            ("hOffset", ctypes.c_uint32),
            ("rSurf", ctypes.c_void_p),
            ("maxSize", area),
            ("minSize", area),
            ("winArgs", ctypes.c_uint32),
            ("jsPressed", ctypes.c_uint8 * (4 * 16)),
            ("joysticks", ctypes.c_int32 * 4),
            ("joystickCount", ctypes.c_uint16),
            ("scale", area)
        ]

bufferRendering = True

try:
    if (bufferRendering == True):
        bufferRendering = True
except:
    bufferRendering = False

class window(Structure):
    if bufferRendering == True:
        _fields_ = [("src", window_src), ("buffer", POINTER(c_uint8)), ("event", Event), ("r", rect), ("fpsCap", c_uint8)]
    else:
        _fields_ = [("src", window_src), ("event", Event), ("r", rect), ("fpsCap", c_int32)]

    def checkEvent(this):
        return lib.RGFW_window_checkEvent(this)
        
    def shouldClose(this):
        return lib.RGFW_window_shouldClose(this)

    def close(this):
        return lib.RGFW_window_close(this)
    
    def setMinSize(this, a):
        return lib.RGFW_window_setMinSize(this, a)
    
    def setMaxSize(this, a):
        return lib.RGFW_window_setMaxSize(this, a)

    def maximize(this):
        return lib.RGFW_window_maximize(this)

    def minimize(this):
        return lib.RGFW_window_minimize(this)

    def restore(this):
        return lib.RGFW_window_restore(this)

    def setName(this, name):
        return lib.RGFW_window_setName(this, name)

    def setIcon(this, icon, a, channels):
        ctypes_array = (ctypes.c_ubyte * len(icon))(*icon)

        pointer_to_array = ctypes.cast(ctypes_array, ctypes.POINTER(ctypes.c_ubyte))

        return lib.RGFW_window_setIcon(this, pointer_to_array, a, channels)

    def setMouse(this, image, a, channels):
        ctypes_array = (ctypes.c_ubyte * len(image))(*image)

        pointer_to_array = ctypes.cast(ctypes_array, ctypes.POINTER(ctypes.c_ubyte))

        return lib.RGFW_window_setMouse(this, pointer_to_array, a, channels)

    def setMouseDefault(this):
        return lib.RGFW_window_setMouseDefault(this)

    def mouseHold(this):
        return lib.RGFW_window_mouseHold(this)

    def mouseUnhold(this):
        return lib.RGFW_window_mouseUnhold(this)

    def hide(this):
        return lib.RGFW_window_hide(this)

    def show(this):
        return lib.RGFW_window_show(this)

    def setShouldClose(this):
        return lib.RGFW_window_setShouldClose(this)

    def showMouse(this, show):
        return lib.RGFW_window_showMouse(this, show)

    def moveMouse(this, v):
        return lib.RGFW_window_moveMouse(this, v)

    def shouldClose(this):
        return lib.RGFW_window_shouldClose(this)

    def isFullscreen(this):
        return lib.RGFW_window_isFullscreen(this)

    def isHidden(this):
        return lib.RGFW_window_isHidden(this)

    def isMinimized(this):
        return lib.RGFW_window_isMinimized(this)

    def isMaximized(this):
        return lib.RGFW_window_isMaximized(this)

    def scaleToMonitor(this):
        return lib.RGFW_window_scaleToMonitor(this)

    def RGFW_window_getMonitor(this):
        return lib.RGFW_window_getMonitor(this)

    def makeCurrent(this):
        return lib.RGFW_window_makeCurrent(this)

    def getMousePoint(this): 
        return lib.RGFW_window_getMousePoint(this)
    
    def swapBuffers(this):
        return lib.RGFW_window_swapBuffers(this)

    def swapInterval(this, swapInterval):
        return lib.RGFW_window_swapInterval(this, swapInterval)

    def setGPURender(this, set):
        return lib.RGFW_window_setGPURender(this, set)
    
    def setCPURender(this, set):
        return lib.RGFW_window_setCPURender(this, set)

    def setMouseStandard(this, mouse):
        return lib.RGFW_window_setMouseStandard(this, mouse)

    def move(this, v):
        return lib.RGFW_window_move(this, v)

    def moveToMonitor(this, m):
        return lib.RGFW_window_moveToMonitor(this, m)

    def resize(this, a):
        return lib.RGFW_window_resize(this, a)



if (system == "Darwin" or system == "Linux"):  # macOS or linux
	thread = c_uint64
else:
    thread = c_void_p

# Function prototypes
lib.RGFW_createWindow.argtypes = [c_char_p, rect, c_uint16]
lib.RGFW_createWindow.restype = POINTER(window)

lib.RGFW_getScreenSize.argtypes = []
lib.RGFW_getScreenSize.restype = area

lib.RGFW_window_checkEvent.argtypes = [POINTER(window)]
lib.RGFW_window_checkEvent.restype = POINTER(Event)

lib.RGFW_window_close.argtypes = [POINTER(window)]
lib.RGFW_window_close.restype = None

lib.RGFW_window_move.argtypes = [POINTER(window), vector]
lib.RGFW_window_move.restype = None

lib.RGFW_window_moveToMonitor.argtypes = [POINTER(window), monitor]
lib.RGFW_window_moveToMonitor.restype = None

lib.RGFW_window_resize.argtypes = [POINTER(window), area]
lib.RGFW_window_resize.restype = None

lib.RGFW_window_shouldClose.argtypes = [POINTER(window)]
lib.RGFW_window_resize.restype = c_uint8

lib.RGFW_getMonitors.argtypes = []
lib.RGFW_getMonitors.restype = POINTER(monitor)

lib.RGFW_getPrimaryMonitor.argtypes = []
lib.RGFW_getPrimaryMonitor.restype = monitor

lib.RGFW_window_setMinSize.argtypes = [POINTER(window), area]
lib.RGFW_window_setMinSize.restype = None

lib.RGFW_window_setMaxSize.argtypes = [POINTER(window), area]
lib.RGFW_window_setMaxSize.restype = None

lib.RGFW_window_maximize.argtypes = [POINTER(window)]
lib.RGFW_window_maximize.restype = None

lib.RGFW_window_minimize.argtypes = [POINTER(window)]
lib.RGFW_window_minimize.restype = None

lib.RGFW_window_restore.argtypes = [POINTER(window)]
lib.RGFW_window_restore.restype = None

lib.RGFW_window_setName.argtypes = [POINTER(window), c_char_p]
lib.RGFW_window_setName.restype = None

lib.RGFW_window_setIcon.argtypes = [POINTER(window), POINTER(c_uint8), area, c_int32]
lib.RGFW_window_setIcon.restype = None

lib.RGFW_window_setMouse.argtypes = [POINTER(window), POINTER(c_uint8), area, c_int32]
lib.RGFW_window_setMouse.restype = None

lib.RGFW_window_setMouseDefault.argtypes = [POINTER(window)]
lib.RGFW_window_setMouseDefault.restype = None

lib.RGFW_window_mouseHold.argtypes = [POINTER(window)]
lib.RGFW_window_mouseHold.restype = None

lib.RGFW_window_mouseUnhold.argtypes = [POINTER(window)]
lib.RGFW_window_mouseUnhold.restype = None

lib.RGFW_window_hide.argtypes = [POINTER(window)]
lib.RGFW_window_hide.restype = None

lib.RGFW_window_show.argtypes = [POINTER(window)]
lib.RGFW_window_show.restype = None

lib.RGFW_window_setShouldClose.argtypes = [POINTER(window)]
lib.RGFW_window_setShouldClose.restype = None

lib.RGFW_getGlobalMousePoint.argtypes = []
lib.RGFW_getGlobalMousePoint.restype = vector

lib.RGFW_window_showMouse.argtypes = [POINTER(window), c_int]
lib.RGFW_window_showMouse.restype = None

lib.RGFW_window_moveMouse.argtypes = [POINTER(window), vector]
lib.RGFW_window_moveMouse.restype = None

lib.RGFW_window_shouldClose.argtypes = [POINTER(window)]
lib.RGFW_window_shouldClose.restype = c_uint8

lib.RGFW_window_isFullscreen.argtypes = [POINTER(window)]
lib.RGFW_window_isFullscreen.restype = c_uint8

lib.RGFW_window_isHidden.argtypes = [POINTER(window)]
lib.RGFW_window_isHidden.restype = c_uint8

lib.RGFW_window_isMinimized.argtypes = [POINTER(window)]
lib.RGFW_window_isMinimized.restype = c_uint8

lib.RGFW_window_isMaximized.argtypes = [POINTER(window)]
lib.RGFW_window_isMaximized.restype = c_uint8

lib.RGFW_window_scaleToMonitor.argtypes = [POINTER(window)]
lib.RGFW_window_scaleToMonitor.restype = None

lib.RGFW_window_getMonitor.argtypes = [POINTER(window)]
lib.RGFW_window_getMonitor.restype = monitor

lib.RGFW_window_makeCurrent.argtypes = [POINTER(window)]
lib.RGFW_window_makeCurrent.restype = None

lib.RGFW_window_getMousePoint.argtypes = [POINTER(window)]
lib.RGFW_window_getMousePoint.restype = vector

lib.RGFW_window_setGPURender.argtypes = [POINTER(window), c_int]
lib.RGFW_window_setGPURender.restype = None

lib.RGFW_window_setCPURender.argtypes = [POINTER(window), c_int]
lib.RGFW_window_setCPURender.restype = None

lib.RGFW_Error.argtypes = []
lib.RGFW_Error.restype = c_uint8

lib.RGFW_isPressedI.argtypes = [POINTER(window), c_uint32]
lib.RGFW_isPressedI.restype = c_uint8

lib.RGFW_keyCodeTokeyStr.argtypes = [c_uint64]
lib.RGFW_keyCodeTokeyStr.restype = c_char_p

lib.RGFW_keyStrToKeyCode.argtypes = [c_char_p]
lib.RGFW_keyStrToKeyCode.restype = c_uint32

lib.RGFW_clipboardFree.argtypes = [c_char_p]
lib.RGFW_clipboardFree.restype = None

lib.RGFW_readClipboard.argtypes = [POINTER(c_uint)]
lib.RGFW_readClipboard.restype = c_char_p

lib.RGFW_writeClipboard.argtypes = [c_char_p, c_uint32]
lib.RGFW_writeClipboard.restype = None

lib.RGFW_keystrToChar.argtypes = [c_char_p]
lib.RGFW_keystrToChar.restype = c_char

lib.RGFW_createThread.argtypes = [CFUNCTYPE(c_void_p, c_void_p), c_void_p]
lib.RGFW_createThread.restype = thread

lib.RGFW_cancelThread.argtypes = [thread]
lib.RGFW_cancelThread.restype = None

lib.RGFW_joinThread.argtypes = [thread]
lib.RGFW_joinThread.restype = None

lib.RGFW_setThreadPriority.argtypes = [thread, c_uint8]
lib.RGFW_setThreadPriority.restype = None

lib.RGFW_registerJoystick.argtypes = [POINTER(window), c_int32]
lib.RGFW_registerJoystick.restype = c_uint16

lib.RGFW_registerJoystickF.argtypes = [POINTER(window), c_char_p]
lib.RGFW_registerJoystickF.restype = c_uint16

lib.RGFW_isPressedJS.argtypes = [POINTER(window), c_uint16, c_uint8]
lib.RGFW_isPressedJS.restype = c_uint32

lib.RGFW_setGLStencil.argtypes = [c_int32]
lib.RGFW_setGLStencil.restype = None

lib.RGFW_setGLSamples.argtypes = [c_int32]
lib.RGFW_setGLSamples.restype = None

lib.RGFW_setGLStereo.argtypes = [c_int32]
lib.RGFW_setGLStereo.restype = None

lib.RGFW_setGLAuxBuffers.argtypes = [c_int32]
lib.RGFW_setGLAuxBuffers.restype = None

lib.RGFW_setGLVersion.argtypes = [c_int32, c_int32]
lib.RGFW_setGLVersion.restype = None

lib.RGFW_getProcAddress.argtypes = [c_char_p]
lib.RGFW_getProcAddress.restype = c_void_p

lib.RGFW_window_swapBuffers.argtypes = [POINTER(window)]


lib.RGFW_window_swapBuffers.restype = None

lib.RGFW_window_swapInterval.argtypes = [POINTER(window), c_int32]
lib.RGFW_window_swapInterval.restype = None

lib.RGFW_window_setGPURender.argtypes = [POINTER(window), c_int]
lib.RGFW_window_setGPURender.restype = None

lib.RGFW_window_checkFPS.argtypes = [POINTER(window)]
lib.RGFW_window_checkFPS.restype = None

lib.RGFW_getTime.argtypes = []
lib.RGFW_getTime.restype = c_uint64

lib.RGFW_getTimeNS.argtypes = []
lib.RGFW_getTimeNS.restype = c_uint64

lib.RGFW_sleep.argtypes = [c_uint]
lib.RGFW_sleep.restype = None

lib.RGFW_window_setMouseStandard.argtypes = (POINTER(window), c_uint8)
lib.RGFW_window_setMouseStandard.restype = None


keyPressed = 2 # a key has been pressed */
keyReleased = 3 #!< a key has been released*/
"""
#! key event note
	the code of the key pressed is stored in
	RGFW_Event.keyCode
	!!Keycodes defined at the bottom of the header file!!

	while a string version is stored in
	RGFW_Event.KeyString

	RGFW_Event.lockState holds the current lockState
	this means if CapsLock, NumLock are active or not
"""
mouseButtonPressed = 4 #!< a mouse button has been pressed (left,middle,right)*/
mouseButtonReleased = 5 #!< a mouse button has been released (left,middle,right)*/
mousePosChanged = 6 #!< the position of the mouse has been changed*/
"""
#! mouse event note
	the x and y of the mouse can be found in the vector, RGFW_Event.point

	RGFW_Event.button holds which mouse button was pressed
"""
jsButtonPressed = 7 #!< a joystick button was pressed */
jsButtonReleased = 8 #!< a joystick button was released */
jsAxisMove = 9 #!< an axis of a joystick was moved*/
"""
#! joystick event note
	RGFW_Event.joystick holds which joystick was altered, if any
	RGFW_Event.button holds which joystick button was pressed

	RGFW_Event.axis holds the data of all the axis
	RGFW_Event.axisCount says how many axis there are

"""

RGFW_windowMoved = 10 #!< the window was moved (by the user) */
RGFW_windowResized = 11 #!< the window was resized (by the user) */
"""
# attribs change event note
	The event data is sent straight to the window structure
	with win->r.x, win->r.y, win->r.w and win->r.h
"""

RGFW_focusIn = 12 #!< window is in focus now */
RGFW_focusOut = 13 #!< window is out of focus now */

""" attribs change event note
	The event data is sent straight to the window structure
	with win->r.x, win->r.y, win->r.w and win->r.h
"""

quit = 33 #!< the user clicked the quit button*/ 
dnd = 34 #!< a file has been dropped into the window*/
dnd_init = 35 #!< the start of a dnd event, when the place where the file drop is known */
"""
 dnd data note
	The x and y coords of the drop are stored in the vector RGFW_Event.point

	RGFW_Event.droppedFilesCount holds how many files were dropped

	This is also the size of the array which stores all the dropped file string,
	RGFW_Event.droppedFiles
"""

mouseLeft  = 1 #!< left mouse button is pressed*/
mouseMiddle  = 2 #!< mouse-wheel-button is pressed*/
mouseRight  = 3 #!< right mouse button is pressed*/
mouseScrollUp = 4 #!< mouse wheel is scrolling up*/
mouseScrollDown =  5 #!< mouse wheel is scrolling down*/

CAPSLOCK = (1 << 1)
NUMLOCK = (1 << 2)

JS_A = 0 # or PS X button */
JS_B = 1 # or PS circle button */
JS_Y = 2 # or PS triangle button */
JS_X = 3 # or PS square button */
JS_START = 9 # start button */
JS_SELECT = 8 # select button */
JS_HOME = 10 # home button */
JS_UP = 13 # dpad up */
JS_DOWN = 14 # dpad down*/
JS_LEFT = 15 # dpad left */
JS_RIGHT = 16 # dpad right */
JS_L1 = 4 # left bump */
JS_L2 = 5 # left trigger*/
JS_R1 = 6 # right bumper */
JS_R2 = 7 # right trigger */

TRANSPARENT_WINDOW		    = (1<<9)  #!< the window is transparent */
NO_BORDER		    = (1<<3)  #!< the window doesn't have border */
NO_RESIZE		    = (1<<4)  #!< the window cannot be resized  by the user */
ALLOW_DND         = (1<<5)  #!< the window supports drag and drop*/
HIDE_MOUSE     = (1<<6)  #! the window should hide the mouse or not (can be toggled later on) using `RGFW_window_mouseShow*/
FULLSCREEN     = (1<<8)  # the window is fullscreen by default or not */
CENTER     = (1<<10)  #! center the window on the screen */
OPENGL_SOFTWARE     = (1<<11)  #! use OpenGL software rendering */
COCOA_MOVE_TO_RESOURCE_DIR = (1 << 12)  # (cocoa only), move to resource folder */
SCALE_TO_MONITOR = (1 << 13)  # scale the window to the screen */

NO_GPU_RENDER     = (1<<14)  # don't render (using the GPU based API)*/
NO_CPU_RENDER     = (1<<15)  # don't render (using the CPU based buffer rendering)*/


def cstrToStr(str : ctypes.c_char_p):
    return ctypes.string_at(str).decode('utf-8')

def createWindow(name, rect, args):
    c_string = ctypes.c_char_p(name.encode('utf-8'))
    window_ptr = lib.RGFW_createWindow(c_string, rect, args)
    if window_ptr is None:
        raise RuntimeError("Failed to create window")

    window_ptr.contents.setCPURender(False)
    return window_ptr.contents

def getMonitors():
    return lib.RGFW_getMonitors()

def getPrimaryMonitor():
    return lib.RGFW_getPrimaryMonitor()

def getGlobalMousePoint():
    return lib.RGFW_getGlobalMousePoint()

def Error():
    return lib.RGFW_Error()

def isPressedI(win, key):
    return lib.RGFW_isPressedI(win, key)

def keyCodeTokeyStr(key):
    return lib.RGFW_keyCodeTokeyStr(key)

def keyStrToKeyCode(key):
    return lib.RGFW_keyStrToKeyCode(key)

def readClipboard(size):
    return lib.RGFW_readClipboard(size)
    
def clipboardFree(string):
    return lib.RGFW_clipboardFree(string)

def writeClipboard(text):
    c_string = ctypes.c_char_p(text.encode('utf-8'))
    return lib.RGFW_writeClipboard(c_string, len(text))

def keystrToChar(key):
    return lib.RGFW_keystrToChar(key)

def createThread(function_ptr, args):
    return lib.RGFW_createThread(function_ptr, args)

def cancelThread(thread):
    return lib.RGFW_cancelThread(thread)

def joinThread(thread):
    return lib.RGFW_joinThread(thread)

def setThreadPriority(thread, priority):
    return lib.RGFW_setThreadPriority(thread, priority)

def registerJoystick(win, jsNumber):
    return lib.RGFW_registerJoystick(win, jsNumber)

def registerJoystickF(win, file):
    return lib.RGFW_registerJoystickF(win, file)

def isPressedJS(win, controller, button):
    return lib.RGFW_isPressedJS(win, controller, button)

def setGLStencil(stencil):
    return lib.RGFW_setGLStencil(stencil)

def setGLSamples(samples):
    return lib.RGFW_setGLSamples(samples)

def setGLStereo(stereo):
    return lib.RGFW_setGLStereo(stereo)

def setGLAuxBuffers(auxBuffers):
    return lib.RGFW_setGLAuxBuffers(auxBuffers)

def setGLVersion(major, minor):
    return lib.RGFW_setGLVersion(major, minor)

def getProcAddress(procname):
    return lib.RGFW_getProcAddress(procname)

def getTime():
    return lib.RGFW_getTime()

def getTimeNS():
    return lib.RGFW_getTimeNS()

def sleep(microsecond):
    return lib.RGFW_sleep(microsecond)

def getScreenSize():
    return lib.RGFW_getScreenSize()


KEY_NULL = 0
Escape = 1
F1 = 2
F2 = 3
F3 = 4
F4 = 5
F5 = 6
F6 = 7
F7 = 8
F8 = 9
F9 = 10
F10 = 11
F11 = 12
F12 = 13
Backtick = 14
KEY_0 = 15
KEY_1 = 16
KEY_2 = 17
KEY_3 = 18
KEY_4 = 19
KEY_5 = 20
KEY_6 = 21
KEY_7 = 22
KEY_8 = 23
KEY_9 = 24

Minus = 25
Equals = 26
BackSpace = 27
Tab = 28
CapsLock = 29
ShiftL = 30
ControlL = 31
AltL = 32
SuperL = 33
ShiftR = 34
ControlR = 35
AltR = 36
SuperR = 37
Space = 38

a = 39
b = 40
c = 41
d = 42
e = 43
f = 44
g = 45
h = 46
i = 47
j = 48
k = 49
l = 50
m = 51
n = 52
o = 53
p = 54
q = 55
r = 56
s = 57
t = 58
u = 59
v = 60
w = 61
x = 62
y = 63
z = 64

Period  = 65
Comma = 66
Slash = 67
Bracket = 68
CloseBracket = 69
Semicolon = 70
Return = 71
Quote = 72
BackSlash = 73

Up = 74
Down = 75
Left = 76
Right = 77

Delete = 78
Insert = 79
End = 80
Home = 81
PageUp = 82
PageDown = 83

Numlock = 84
KP_Slash = 85
Multiply = 86
KP_Minus = 87
KP_1 = 88
KP_2 = 89
KP_3 = 90
KP_4 = 91
KP_5 = 92
KP_6 = 93
KP_7 = 94
KP_8 = 95
KP_9 = 96
KP_0 = 97
KP_Period = 98
KP_Return = 99

# mouse icons
MOUSE_NORMAL = 0 
MOUSE_ARROW = 2
MOUSE_IBEAM = 3
MOUSE_CROSSHAIR = 4
MOUSE_POINTING_HAND = 5
MOUSE_RESIZE_EW = 6
MOUSE_RESIZE_NS = 7
MOUSE_RESIZE_NWSE = 8
MOUSE_RESIZE_NESW = 9
MOUSE_RESIZE_ALL = 10
MOUSE_NOT_ALLOWED = 11