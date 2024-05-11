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
    _fields_ = [("keyName", c_char_p), ("droppedFiles", POINTER(c_char_p)), ("droppedFilesCount", c_uint32), ("type", c_uint32), ("point", vector), ("keyCode", c_uint32), ("inFocus", c_uint32), ("fps", c_uint32), ("current_ticks", c_uint32), ("frames", c_uint32), ("lockState", c_uint8), ("joystick", c_uint16), ("button", c_uint8), ("scroll", c_double), ("axisesCount", c_uint8), ("axis", vector * 2)]

class window_src(Structure):
    if (system == "Linux"):
        _fields_ = [
            ("display", ctypes.c_void_p),
            ("window", ctypes.c_void_p),
            ("cursor", ctypes.c_void_p),
            ("rSurf", ctypes.c_void_p),
            ("jsPressed", ctypes.c_uint8 * (4 * 16)),
            ("joysticks", ctypes.c_int32 * 4),
            ("joystickCount", ctypes.c_uint16),
            ("scale", area)
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

try:
    if (bufferRendering == True):
        bufferRendering = True
except:
    bufferRendering = False

class window(Structure):
    if  bufferRendering == True:
        _fields_ = [("src", window_src), ("buffer", POINTER(c_uint8)), ("event", Event), ("r", rect), ("fpsCap", c_uint8)]
    else:
        _fields_ = [("src", window_src), ("event", Event), ("r", rect), ("fpsCap", c_uint8)]
    
    def __init__(self, window_ptr):
        self.window_ptr = window_ptr

    def checkEvent(this):
        this.event.type = this.window_ptr.contents.event.type
        this.r = this.window_ptr.contents.r
        this.window_ptr.contents.fpsCap = this.fpsCap
        
        if (bufferRendering == True):
            this.window_ptr.contents.buffer = this.buffer
        print(this.window_ptr.contents.event.type)
        return lib.RGFW_window_checkEvent(this.window_ptr)

    def shouldClose(this):
        return lib.RGFW_window_shouldClose(this.window_ptr)

    def close(this):
        return lib.RGFW_window_close(this.window_ptr)
    
    def setMinSize(this, a):
        return lib.RGFW_window_setMinSize(this.window_ptr, a)
    
    def setMaxSize(this, a):
        return lib.RGFW_window_setMaxSize(this.window_ptr, a)

    def maximize(this):
        return lib.RGFW_window_maximize(this.window_ptr)

    def minimize(this):
        return lib.RGFW_window_minimize(this.window_ptr)

    def restore(this):
        return lib.RGFW_window_restore(this.window_ptr)

    def setName(this, name):
        return lib.RGFW_window_setName(this.window_ptr, name)

    def setIcon(this, icon, a, channels):
        ctypes_array = (ctypes.c_ubyte * len(icon))(*icon)

        pointer_to_array = ctypes.cast(ctypes_array, ctypes.POINTER(ctypes.c_ubyte))

        return lib.RGFW_window_setIcon(this.window_ptr, pointer_to_array, a, channels)

    def setMouse(this, image, a, channels):
        return lib.RGFW_window_setMouse(this.window_ptr, image, a, channels)

    def setMouseDefault(this):
        return lib.RGFW_window_setMouseDefault(this.window_ptr)

    def mouseHold(this):
        return lib.RGFW_window_mouseHold(this.window_ptr)

    def mouseUnhold(this):
        return lib.RGFW_window_mouseUnhold(this.window_ptr)

    def hide(this):
        return lib.RGFW_window_hide(this.window_ptr)

    def show(this):
        return lib.RGFW_window_show(this.window_ptr)

    def setShouldClose(this):
        return lib.RGFW_window_setShouldClose(this).window_ptr

    def showMouse(this, show):
        return lib.RGFW_window_showMouse(this.window_ptr, show)

    def moveMouse(this, v):
        return lib.RGFW_window_moveMouse(this.window_ptr, v)

    def shouldClose(this):
        return lib.RGFW_window_shouldClose(this.window_ptr)

    def isFullscreen(this):
        return lib.RGFW_window_isFullscreen(this.window_ptr)

    def isHidden(this):
        return lib.RGFW_window_isHidden(this.window_ptr)

    def isMinimized(this):
        return lib.RGFW_window_isMinimized(this.window_ptr)

    def isMaximized(this):
        return lib.RGFW_window_isMaximized(this.window_ptr)

    def scaleToMonitor(this):
        return lib.RGFW_window_scaleToMonitor(this.window_ptr)

    def RGFW_window_getMonitor(this):
        return lib.RGFW_window_getMonitor(this.window_ptr)

    def makeCurrent(this):
        return lib.RGFW_window_makeCurrent(this.window_ptr)

    def swapBuffers(this):
        return lib.RGFW_window_swapBuffers(this.window_ptr)

    def swapInterval(this, swapInterval):
        return lib.RGFW_window_swapInterval(this.window_ptr, swapInterval)

    def setGPURender(this, set):
        return lib.RGFW_window_setGPURender(this.window_ptr, set)

    def checkFPS(this):
        return lib.RGFW_window_checkFPS(this.window_ptr)

    def setMouseStandard(this, mouse):
        return lib.RGFW_window_setMouseStandard(this.window_ptr, mouse)

    def move(this, v):
        return lib.RGFW_window_move(this.window_ptr, v)

    def moveToMonitor(this, m):
        return lib.RGFW_window_moveToMonitor(this.window_ptr, m)

    def resize(this, a):
        return lib.RGFW_window_resize(this.window_ptr, a)



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

lib.RGFW_Error.argtypes = []
lib.RGFW_Error.restype = c_uint8

lib.RGFW_isPressedI.argtypes = [POINTER(window), c_uint32]
lib.RGFW_isPressedI.restype = c_uint8

lib.RGFW_keyCodeTokeyStr.argtypes = [c_uint64]
lib.RGFW_keyCodeTokeyStr.restype = c_char_p

lib.RGFW_keyStrToKeyCode.argtypes = [c_char_p]
lib.RGFW_keyStrToKeyCode.restype = c_uint32

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

lib.RGFW_getFPS.argtypes = []
lib.RGFW_getFPS.restype = c_uint32

lib.RGFW_sleep.argtypes = [c_uint]
lib.RGFW_sleep.restype = None

def RGFW_OS_BASED_VALUE(l, w, m):
    if (system == "Linux"):
        return l
    elif (system == "Windows"):
        return w
    elif (system == "Darwin"):  # macOS
        return m

if (system == "Darwin"):  # macOS
    lib.NSCursor_arrowStr.argtypes = [c_char_p]
    lib.NSCursor_arrowStr.restype = c_void_p

    lib.NSCursor_performSelector.argtypes = [c_void_p, c_void_p]
    lib.NSCursor_performSelector.restype = None

    lib.selector.argtypes = [c_void_p]
    lib.selector.restype = c_void_p
    
    lib.RGFW_window_setMouseStandard.argtypes = [POINTER(window), c_void_p]
    lib.RGFW_window_setMouseStandard.restype = None
else:
    lib.RGFW_window_setMouseStandard.argtypes = (POINTER(window), c_int32)
    lib.RGFW_window_setMouseStandard.restype = None

def NSCursor_arrowStr(str):
    if (system == "Darwin"):
        return lib.NSCursor_arrowStr(str)

def NSCursor_performSelector(p):
    if (system == "Darwin"):
        return lib.NSCursor_performSelector(p)
    
def selector(p):
    if (system == "Darwin"):
        return lib.selector(p)

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

windowAttribsChange = 10 #!< the window was moved or resized (by the user) */
"""
# attribs change event note
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


def createWindow(name, rect, args):
    c_string = ctypes.c_char_p(name.encode('utf-8'))
    window_ptr = lib.RGFW_createWindow(c_string, rect, args)
    if window_ptr is None:
        raise RuntimeError("Failed to create window")

    return window(window_ptr)

def getMonitors():
    return lib.RGFW_getMonitors()

def getPrimaryMonitor():
    return lib.RGFW_getPrimaryMonitor()

def getGlobalMousePoint():
    return lib.RGFW_getGlobalMousePoint()

def Error():
    return lib.RGFW_Error()

def isPressedI(win, key):
    return lib.RGFW_isPressedI(win.window_ptr, key)

def keyCodeTokeyStr(key):
    return lib.RGFW_keyCodeTokeyStr(key)

def keyStrToKeyCode(key):
    return lib.RGFW_keyStrToKeyCode(key)

def readClipboard(size):
    c_string_pointer = lib.RGFW_readClipboard(size)
    return ctypes.string_at(c_string_pointer).decode('utf-8')

def clipboardFree(str):
    return

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
    return lib.RGFW_registerJoystick(win.window_ptr, jsNumber)

def registerJoystickF(win, file):
    return lib.RGFW_registerJoystickF(win.window_ptr, file)

def isPressedJS(win, controller, button):
    return lib.RGFW_isPressedJS(win.window_ptr, controller, button)

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

def getFPS():
    return lib.RGFW_getFPS()

def sleep(microsecond):
    return lib.RGFW_sleep(microsecond)

def getScreenSize():
    return lib.RGFW_getScreenSize()


Escape = RGFW_OS_BASED_VALUE(0xff1b, 0x1B, 53)
F1 = RGFW_OS_BASED_VALUE(0xffbe, 0x70, 127)
F2 = RGFW_OS_BASED_VALUE(0xffbf, 0x71, 121)
F3 = RGFW_OS_BASED_VALUE(0xffc0, 0x72, 100)
F4 = RGFW_OS_BASED_VALUE(0xffc1, 0x73, 119)
F5 = RGFW_OS_BASED_VALUE(0xffc2, 0x74, 97)
F6 = RGFW_OS_BASED_VALUE(0xffc3, 0x75, 98)
F7 = RGFW_OS_BASED_VALUE(0xffc4, 0x76, 99)
F8 = RGFW_OS_BASED_VALUE(0xffc5, 0x77, 101)
F9 = RGFW_OS_BASED_VALUE(0xffc6, 0x78, 102)
F10 = RGFW_OS_BASED_VALUE(0xffc7, 0x79, 110)
F11 = RGFW_OS_BASED_VALUE(0xffc8, 0x7A, 104)
F12 = RGFW_OS_BASED_VALUE(0xffc9, 0x7B, 112)
F13 = RGFW_OS_BASED_VALUE(0xffca, 0x7C, 106)
F14 = RGFW_OS_BASED_VALUE(0xffcb, 0x7D, 108)
F15 = RGFW_OS_BASED_VALUE(0xffcc, 0x7E, 114)

Backtick = RGFW_OS_BASED_VALUE(96 , 192, 50)

K0 = RGFW_OS_BASED_VALUE(0x0030, 0x30, 29)
K1 = RGFW_OS_BASED_VALUE(0x0031, 0x31, 18)
K2 = RGFW_OS_BASED_VALUE(0x0032, 0x32, 19)
K3 = RGFW_OS_BASED_VALUE(0x0033, 0x33, 20)
K4 = RGFW_OS_BASED_VALUE(0x0034, 0x34, 21)
K5 = RGFW_OS_BASED_VALUE(0x0035, 0x35, 23)
K6 = RGFW_OS_BASED_VALUE(0x0036, 0x36, 22)
K7 = RGFW_OS_BASED_VALUE(0x0037, 0x37, 26)
K8 = RGFW_OS_BASED_VALUE(0x0038, 0x38, 28)
K9 = RGFW_OS_BASED_VALUE(0x0039, 0x39, 25)

Minus = RGFW_OS_BASED_VALUE(0x002d, 189, 27)
Equals = RGFW_OS_BASED_VALUE(0x003d, 187, 24)
BackSpace = RGFW_OS_BASED_VALUE(0xff08, 8, 51)
Tab = RGFW_OS_BASED_VALUE(0xff89, 0x09, 48)
CapsLock = RGFW_OS_BASED_VALUE(0xffe5, 20, 57)
ShiftL = RGFW_OS_BASED_VALUE(0xffe1, 0xA0, 56)
ControlL = RGFW_OS_BASED_VALUE(0xffe3, 0x11, 59)
AltL = RGFW_OS_BASED_VALUE(0xffe9, 164, 58)
SuperL = RGFW_OS_BASED_VALUE(0xffeb, 0x5B, 55) 
ShiftR = RGFW_OS_BASED_VALUE(0xffe2, 0x5C, 56)
ControlR = RGFW_OS_BASED_VALUE(0xffe4, 0x11, 59)
AltR = RGFW_OS_BASED_VALUE(0xffea, 165, 58)
SuperR = RGFW_OS_BASED_VALUE(0xffec, 0xA4, 55)
Space = RGFW_OS_BASED_VALUE(0x0020,  0x20, 49)

A = RGFW_OS_BASED_VALUE(0x0041, 0x41, 0)
B = RGFW_OS_BASED_VALUE(0x0042, 0x42, 11)
C = RGFW_OS_BASED_VALUE(0x0043, 0x43, 8)
D = RGFW_OS_BASED_VALUE(0x0044, 0x44, 2)
E = RGFW_OS_BASED_VALUE(0x0045, 0x45, 14)
F = RGFW_OS_BASED_VALUE(0x0046, 0x46, 3)
G = RGFW_OS_BASED_VALUE(0x0047, 0x47, 5)
H = RGFW_OS_BASED_VALUE(0x0048, 0x48, 4) 
I = RGFW_OS_BASED_VALUE(0x0049, 0x49, 34)
J = RGFW_OS_BASED_VALUE(0x004a, 0x4A, 38)
K = RGFW_OS_BASED_VALUE(0x004b, 0x4B, 40)
L = RGFW_OS_BASED_VALUE(0x004c, 0x4C, 37)
M = RGFW_OS_BASED_VALUE(0x004d, 0x4D, 46)
N = RGFW_OS_BASED_VALUE(0x004e, 0x4E, 45)
O = RGFW_OS_BASED_VALUE(0x004f, 0x4F, 31)
P = RGFW_OS_BASED_VALUE(0x0050, 0x50, 35)
Q = RGFW_OS_BASED_VALUE(0x0051, 0x51, 12)
R = RGFW_OS_BASED_VALUE(0x0052, 0x52, 15)
S = RGFW_OS_BASED_VALUE(0x0053, 0x53, 1)
T = RGFW_OS_BASED_VALUE(0x0054, 0x54, 17)
U = RGFW_OS_BASED_VALUE(0x0055, 0x55, 32)
V = RGFW_OS_BASED_VALUE(0x0056, 0x56, 9)
W = RGFW_OS_BASED_VALUE(0x0057, 0x57, 13)
X = RGFW_OS_BASED_VALUE(0x0058, 0x58, 7)
Y = RGFW_OS_BASED_VALUE(0x0059, 0x59, 16)
Z = RGFW_OS_BASED_VALUE(0x005a, 0x5A, 6)

a = RGFW_OS_BASED_VALUE(0x0061, 0x41, 0)
b = RGFW_OS_BASED_VALUE(0x0062, 0x42, 11)
c = RGFW_OS_BASED_VALUE(0x0063, 0x43, 8)
d = RGFW_OS_BASED_VALUE(0x0064, 0x44, 2)
e = RGFW_OS_BASED_VALUE(0x0065, 0x45, 14)
f = RGFW_OS_BASED_VALUE(0x0066, 0x46, 3)
g = RGFW_OS_BASED_VALUE(0x0067, 0x47, 5)
h = RGFW_OS_BASED_VALUE(0x0068, 0x48, 4)
i = RGFW_OS_BASED_VALUE(0x0069, 0x49, 34)
j = RGFW_OS_BASED_VALUE(0x006a, 0x4a, 38)
k = RGFW_OS_BASED_VALUE(0x006b, 0x4b, 40)
l = RGFW_OS_BASED_VALUE(0x006c, 0x4c, 37)
m = RGFW_OS_BASED_VALUE(0x006d, 0x4d, 46)
n = RGFW_OS_BASED_VALUE(0x006e, 0x4e, 45)
o = RGFW_OS_BASED_VALUE(0x006f, 0x4f, 31)
p = RGFW_OS_BASED_VALUE(0x0070, 0x50, 35)
q = RGFW_OS_BASED_VALUE(0x0071, 0x51, 12)
r = RGFW_OS_BASED_VALUE(0x0072, 0x52, 15)
s = RGFW_OS_BASED_VALUE(0x0073, 0x53, 1)
t = RGFW_OS_BASED_VALUE(0x0074, 0x54, 17)
u = RGFW_OS_BASED_VALUE(0x0075, 0x55, 32)
v = RGFW_OS_BASED_VALUE(0x0076, 0x56, 9)
w = RGFW_OS_BASED_VALUE(0x0077, 0x57, 13)
x = RGFW_OS_BASED_VALUE(0x0078, 0x58, 7) 
y = RGFW_OS_BASED_VALUE(0x0079, 0x59, 16)
z = RGFW_OS_BASED_VALUE(0x007a, 0x5A, 6)

Period = RGFW_OS_BASED_VALUE(0x002e, 190, 47)
Comma = RGFW_OS_BASED_VALUE(0x002c, 188, 43)
Slash = RGFW_OS_BASED_VALUE(0x002f, 191, 44)
Bracket = RGFW_OS_BASED_VALUE(0x005b, 219, 33)
CloseBracket = RGFW_OS_BASED_VALUE(0x005d, 221, 30) 
Semicolon = RGFW_OS_BASED_VALUE(0x003b, 186, 41)
Return = RGFW_OS_BASED_VALUE(0xff0d, 0x0D, 36) 
Quote = RGFW_OS_BASED_VALUE(0x0022, 222, 39)
BackSlash = RGFW_OS_BASED_VALUE(0x005c, 322, 42)

Up = RGFW_OS_BASED_VALUE(0xff52, 0x26, 126)
Down = RGFW_OS_BASED_VALUE(0xff54, 0x28, 125)
Left = RGFW_OS_BASED_VALUE(0xff51, 0x25, 123)
Right = RGFW_OS_BASED_VALUE(0xff53, 0x27, 124)

Delete = RGFW_OS_BASED_VALUE(0xffff, 0x2E, 118)
Insert = RGFW_OS_BASED_VALUE(0xff63, 0x2D, 115)
End = RGFW_OS_BASED_VALUE(0xff57, 0x23, 120)
Home = RGFW_OS_BASED_VALUE(0xff50, 0x24, 116) 
PageUp = RGFW_OS_BASED_VALUE(0xff55, 336, 117)
PageDown = RGFW_OS_BASED_VALUE(0xff56, 325, 122)

Numlock = RGFW_OS_BASED_VALUE(0xff7f, 0x90, 72)
KP_Slash = RGFW_OS_BASED_VALUE(0xffaf, 0x6F, 82)
Multiply = RGFW_OS_BASED_VALUE(0xffaa, 0x6A, 76)
KP_Minus = RGFW_OS_BASED_VALUE(0xffad, 0x6D, 67)
KP_1 = RGFW_OS_BASED_VALUE(0xffb1, 0x61, 84)
KP_2 = RGFW_OS_BASED_VALUE(0xffb2, 0x62, 85)
KP_3 = RGFW_OS_BASED_VALUE(0xffb3, 0x63, 86)
KP_4 = RGFW_OS_BASED_VALUE(0xffb4, 0x64, 87)
KP_5 = RGFW_OS_BASED_VALUE(0xffb5, 0x65, 88)
KP_6 = RGFW_OS_BASED_VALUE(0xffb6, 0x66, 89)
KP_7 = RGFW_OS_BASED_VALUE(0xffb7, 0x67, 90)
KP_8 = RGFW_OS_BASED_VALUE(0xffb8, 0x68, 92)
KP_9 = RGFW_OS_BASED_VALUE(0xffb9, 0x619, 93)
KP_0 = RGFW_OS_BASED_VALUE(0xffb0, 0x60, 83)
KP_Period = RGFW_OS_BASED_VALUE(0xffae, 0x6E, 65)
KP_Return = RGFW_OS_BASED_VALUE(0xff8d, 0x92, 77)

# mouse icons
MOUSE_ARROW 				= RGFW_OS_BASED_VALUE(68,   32512, NSCursor_arrowStr("arrowCursor"))
MOUSE_IBEAM 				= RGFW_OS_BASED_VALUE(152,  32513, NSCursor_arrowStr("IBeamCursor"))
MOUSE_CROSSHAIR		 	= RGFW_OS_BASED_VALUE(34,   32515, NSCursor_arrowStr("crosshairCursor"))
MOUSE_POINTING_HAND 		= RGFW_OS_BASED_VALUE(60,   32649, NSCursor_arrowStr("pointingHandCursor"))
MOUSE_RESIZE_EW 			= RGFW_OS_BASED_VALUE(108,  32644, NSCursor_arrowStr("resizeLeftRightCursor"))
MOUSE_RESIZE_NS  			= RGFW_OS_BASED_VALUE(116,  32645, NSCursor_arrowStr("resizeUpDownCursor"))
MOUSE_RESIZE_ALL 			= RGFW_OS_BASED_VALUE(52,   32646, NSCursor_arrowStr("closedHandCursor"))
MOUSE_RESIZE_NWSE 			= RGFW_OS_BASED_VALUE(12,   32642, NSCursor_performSelector(selector("_windowResizeNorthWestSouthEastCursor")))
MOUSE_RESIZE_NESW 			= RGFW_OS_BASED_VALUE(14,   32643, NSCursor_performSelector(selector("_windowResizeNorthEastSouthWestCursor")))
MOUSE_NOT_ALLOWED 			= RGFW_OS_BASED_VALUE(0,    32648, NSCursor_arrowStr("operationNotAllowedCursor"))
