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
class point(Structure):
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
                ("point", point), 
                ("keyCode", c_uint8), 
                ("repeat", c_uint8),
                ("inFocus", c_uint8), 
                ("lockState", c_uint8),
                ("button", c_uint8), 
                ("scroll", c_double), 

                ("gamepad", c_uint16), 
                ("axisesCount", c_uint8), 
                ("whichAxis", c_uint8), 
                ("axis", point * 4),
                
                ("frameTime", c_uint64), 
                ("frameTime2", c_uint64)]

bufferRendering = True

try:
    if (bufferRendering == True):
        bufferRendering = True
except:
    bufferRendering = False

class window_src(Structure):
    if (system == "Linux"):
        if (bufferRendering == True):
            _fields_ = [
                ("display", ctypes.c_void_p),
                ("window", ctypes.c_void_p),
                ("ctx", ctypes.c_void_p),
                ("bitmap", ctypes.c_void_p),
                ("gc", ctypes.c_void_p),
            ]
        else:
            _fields_ = [("display", ctypes.c_void_p), ("window", ctypes.c_void_p), ("ctx", ctypes.c_void_p),]
    elif (system == "Darwin"):  # macOS
        if (bufferRendering == True):
            _fields_ = [
                ("display", ctypes.c_uint32),
                ("displayLink", ctypes.c_void_p),
                ("window", ctypes.c_void_p),
                ("dndPassed", ctypes.c_uint8),
                ("ctx", ctypes.c_void_p),
                ("view", ctypes.c_void_p),
                ("viebitmapw", ctypes.c_void_p),
                ("image", ctypes.c_void_p)
            ]
        else:
            _fields_ = [
                ("display", ctypes.c_uint32), ("displayLink", ctypes.c_void_p), ("window", ctypes.c_void_p), ("dndPassed", ctypes.c_uint8), ("ctx", ctypes.c_void_p), ("view", ctypes.c_void_p), ("viebitmapw", ctypes.c_void_p), ("image", ctypes.c_void_p)
            ]
    elif (system == "Windows"):
        if (bufferRendering == True):
            _fields_ = [
                ("window", ctypes.c_void_p),
                ("hdc", ctypes.c_void_p),
                ("hOffset", ctypes.c_uint32),
                ("ctx", ctypes.c_void_p),
                ("hdcMem", ctypes.c_void_p),
                ("bitmap", ctypes.c_void_p),
                ("maxSize", area),
                ("minSize", area)
            ]
        else:
            _fields_ = [
                ("window", ctypes.c_void_p), ("hdc", ctypes.c_void_p), ("hOffset", ctypes.c_uint32), ("ctx", ctypes.c_void_p), ("maxSize", area), ("minSize", area)
            ]

class window(Structure):
    if bufferRendering == True:
        _fields_ = [("src", window_src), ("buffer", POINTER(c_uint8)), ("userPtr", ctypes.c_void_p), ("event", Event), ("r", rect), ("_lastMousePoint", point), ("winArgs", ctypes.c_uint32)]
    else:
         _fields_ = [("src", window_src), ("userPtr", ctypes.c_void_p), ("event", Event), ("r", rect), ("_lastMousePoint", point), ("winArgs", ctypes.c_uint32)]
    
    def checkEvent(this):
        return lib.RGFW_window_checkEvent(this)
    
    def eventWait(this, waitMS):
        return lib.RGFW_window_eventWait(this, waitMS)

    def checkEvents(this, waitMS):
        return lib.RGFW_window_checkEvents(this, waitMS)
        
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

    def makeCurrent_OpenGL(this):
        return lib.RGFW_window_makeCurrent_OpenGL(this)

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
lib.RGFW_setClassName.argtypes = [c_char_p]
lib.RGFW_setClassName.restype = None

lib.RGFW_setBufferSize.argtypes = [area]
lib.RGFW_setBufferSize.restype = None

lib.RGFW_createWindow.argtypes = [c_char_p, rect, c_uint16]
lib.RGFW_createWindow.restype = POINTER(window)

lib.RGFW_getScreenSize.argtypes = []
lib.RGFW_getScreenSize.restype = area

lib.RGFW_window_checkEvent.argtypes = [POINTER(window)]
lib.RGFW_window_checkEvent.restype = POINTER(Event)

lib.RGFW_window_checkEvents.argtypes = [POINTER(window), c_uint32]
lib.RGFW_window_checkEvents.restype = None

lib.RGFW_window_eventWait.argtypes = [POINTER(window), c_int32]
lib.RGFW_window_eventWait.restype = None

lib.RGFW_window_eventWait.argtypes = []
lib.RGFW_window_eventWait.restype = None

lib.RGFW_window_close.argtypes = [POINTER(window)]
lib.RGFW_window_close.restype = None

lib.RGFW_window_move.argtypes = [POINTER(window), point]
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
lib.RGFW_getGlobalMousePoint.restype = point

lib.RGFW_window_showMouse.argtypes = [POINTER(window), c_int]
lib.RGFW_window_showMouse.restype = None

lib.RGFW_window_moveMouse.argtypes = [POINTER(window), point]
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

lib.RGFW_window_makeCurrent_OpenGL.argtypes = [POINTER(window)]
lib.RGFW_window_makeCurrent_OpenGL.restype = None

lib.RGFW_window_getMousePoint.argtypes = [POINTER(window)]
lib.RGFW_window_getMousePoint.restype = point

lib.RGFW_window_setGPURender.argtypes = [POINTER(window), c_int]
lib.RGFW_window_setGPURender.restype = None

lib.RGFW_window_setCPURender.argtypes = [POINTER(window), c_int]
lib.RGFW_window_setCPURender.restype = None

lib.RGFW_Error.argtypes = []
lib.RGFW_Error.restype = c_uint8

lib.RGFW_isReleased.argtypes = [POINTER(window), c_uint8]
lib.RGFW_isReleased.restype = c_uint8

lib.RGFW_isHeld.argtypes = [POINTER(window), c_uint8]
lib.RGFW_isHeld.restype = c_uint8

lib.RGFW_isPressed.argtypes = [POINTER(window), c_uint8]
lib.RGFW_isPressed.restype = c_uint8

lib.RGFW_isClicked.argtypes = [POINTER(window), c_uint8]
lib.RGFW_isClicked.restype = c_uint8

lib.RGFW_isMouseReleased.argtypes = [POINTER(window), c_uint8]
lib.RGFW_isMouseReleased.restype = c_uint8

lib.RGFW_isMouseHeld.argtypes = [POINTER(window), c_uint8]
lib.RGFW_isMouseHeld.restype = c_uint8

lib.RGFW_isMousePressed.argtypes = [POINTER(window), c_uint8]
lib.RGFW_isMousePressed.restype = c_uint8

lib.RGFW_shouldShift.argtypes = [c_uint32, c_uint8]
lib.RGFW_shouldShift.restype = c_char

lib.RGFW_keyCodeToChar.argtypes = [c_uint32, c_uint8]
lib.RGFW_keyCodeToChar.restype = c_char

lib.RGFW_keyCodeToCharAuto.argtypes = [c_uint32, c_uint8]
lib.RGFW_keyCodeToCharAuto.restype = c_char

lib.RGFW_clipboardFree.argtypes = [c_char_p]
lib.RGFW_clipboardFree.restype = None

lib.RGFW_readClipboard.argtypes = [POINTER(c_uint)]
lib.RGFW_readClipboard.restype = c_char_p

lib.RGFW_writeClipboard.argtypes = [c_char_p, c_uint32]
lib.RGFW_writeClipboard.restype = None

lib.RGFW_createThread.argtypes = [CFUNCTYPE(c_void_p, c_void_p), c_void_p]
lib.RGFW_createThread.restype = thread

lib.RGFW_cancelThread.argtypes = [thread]
lib.RGFW_cancelThread.restype = None

lib.RGFW_joinThread.argtypes = [thread]
lib.RGFW_joinThread.restype = None

lib.RGFW_setThreadPriority.argtypes = [thread, c_uint8]
lib.RGFW_setThreadPriority.restype = None

lib.RGFW_registerGamepad.argtypes = [POINTER(window), c_int32]
lib.RGFW_registerGamepad.restype = c_uint16

lib.RGFW_registerGamepadF.argtypes = [POINTER(window), c_char_p]
lib.RGFW_registerGamepadF.restype = c_uint16

lib.RGFW_isPressedGP.argtypes = [POINTER(window), c_uint16, c_uint8]
lib.RGFW_isPressedGP.restype = c_uint32

lib.RGFW_setGLStencil.argtypes = [c_int32]
lib.RGFW_setGLStencil.restype = None

lib.RGFW_setGLSamples.argtypes = [c_int32]
lib.RGFW_setGLSamples.restype = None

lib.RGFW_setGLStereo.argtypes = [c_int32]
lib.RGFW_setGLStereo.restype = None

lib.RGFW_setGLAuxBuffers.argtypes = [c_int32]
lib.RGFW_setGLAuxBuffers.restype = None

lib.RGFW_setDoubleBuffer.argtypes = [c_uint8]
lib.RGFW_setDoubleBuffer.restype = None

lib.RGFW_setGLVersion.argtypes = [c_uint8, c_int32, c_int32]
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

# RGFW.windowMoved, the window and its new rect value  */
windowmovefunc       = CFUNCTYPE(POINTER(window), rect)
# RGFW.windowResized, the window and its new rect value  */
windowresizefunc       = CFUNCTYPE(POINTER(window), rect)
# RGFW.quit, the window that was closed */
windowquitfunc       = CFUNCTYPE(POINTER(window))
# RGFW.focusIn / RGFW_focusOut, the window who's focus has changed and if its inFocus */
FOCUSCALLBACK       = CFUNCTYPE(POINTER(window), c_uint8)
# RGFW.mouseEnter / RGFW_mouseLeave, the window that changed, the point of the mouse (enter only) and if the mouse has entered */
mouseNotifyfunc       = CFUNCTYPE(POINTER(window), point, c_uint8)
# RGFW.mousePosChanged, the window that the move happened on and the new point of the mouse  */
mouseposfunc       = CFUNCTYPE(POINTER(window), point)
#  RGFW.dnd, the window that had the drop, the drop data and the amount files dropped */
dndfunc       = CFUNCTYPE(POINTER(window), POINTER(c_char_p), c_uint32)
# RGFW.dnd_init, the window, the point of the drop on the windows */
dndInitfunc       = CFUNCTYPE(POINTER(window), point)
# RGFW.windowRefresh, the window that needs to be refreshed */
windowrefreshfunc       = CFUNCTYPE(POINTER(window))
# RGFW.keyPressed / RGFW_keyReleased, the window that got the event, the keycode, the string version, the state of mod keys, if it was a press (else it's a release) */
keyfunc       = CFUNCTYPE(POINTER(window), c_uint32, c_char * 16, c_uint8, c_uint8)
# RGFW.mouseButtonPressed / RGFW_mouseButtonReleased, the window that got the event, the button that was pressed, the scroll value, if it was a press (else it's a release)  */
mousebuttonfunc       = CFUNCTYPE(POINTER(window), c_uint8, c_double, c_uint8)
# RGFW.gpButtonPressed / RGFW_gpButtonReleased, the window that got the event, the button that was pressed, the scroll value, if it was a press (else it's a release) */
gpButtonfunc       = CFUNCTYPE(POINTER(window), c_uint16, c_uint8, c_uint8)
# RGFW.gpAxisMove, the window that got the event, the gamepad in question, the axis values and the amount of axises */
gpAxisfunc       = CFUNCTYPE(POINTER(window), c_uint16, point * 2, c_uint8)


lib.RGFW_setWindowMoveCallback.argtypes = [windowmovefunc]
lib.RGFW_setWindowMoveCallback.restype = None

lib.RGFW_setWindowResizeCallback.argtypes = [windowresizefunc]
lib.RGFW_setWindowResizeCallback.restype = None

lib.RGFW_setWindowQuitCallback.argtypes = [windowquitfunc]
lib.RGFW_setWindowQuitCallback.restype = None

lib.RGFW_setMousePosCallback.argtypes = [mouseposfunc]
lib.RGFW_setMousePosCallback.restype = None

lib.RGFW_setWindowRefreshCallback.argtypes = [windowrefreshfunc]
lib.RGFW_setWindowRefreshCallback.restype = None

lib.RGFW_setFocusCallback.argtypes = [FOCUSCALLBACK]
lib.RGFW_setFocusCallback.restype = None

lib.RGFW_setMouseNotifyCallBack.argtypes = [mouseNotifyfunc]
lib.RGFW_setMouseNotifyCallBack.restype = None

lib.RGFW_setDndCallback.argtypes = [dndfunc]
lib.RGFW_setDndCallback.restype = None

lib.RGFW_setDndInitCallback.argtypes = [dndInitfunc]
lib.RGFW_setDndInitCallback.restype = None

lib.RGFW_setKeyCallback.argtypes = [keyfunc]
lib.RGFW_setKeyCallback.restype = None

lib.RGFW_setMouseButtonCallback.argtypes = [mousebuttonfunc]
lib.RGFW_setMouseButtonCallback.restype = None

lib.RGFW_setgpButtonCallback.argtypes = [gpButtonfunc]
lib.RGFW_setgpButtonCallback.restype = None

lib.RGFW_setgpAxisCallback.argtypes = [gpAxisfunc]
lib.RGFW_setgpAxisCallback.restype = None

keyPressed = 1 # a key has been pressed */
keyReleased = 2 #!< a key has been released*/
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
mouseButtonPressed = 3 #!< a mouse button has been pressed (left,middle,right)*/
mouseButtonReleased = 4 #!< a mouse button has been released (left,middle,right)*/
mousePosChanged = 5 #!< the position of the mouse has been changed*/
"""
#! mouse event note
	the x and y of the mouse can be found in the point, RGFW_Event.point

	RGFW_Event.button holds which mouse button was pressed
"""
gpButtonPressed = 6 #!< a gamepad button was pressed */
gpButtonReleased = 7 #!< a gamepad button was released */
gpAxisMove = 8 #!< an axis of a gamepad was moved*/
"""
#! gamepad event note
	RGFW_Event.gamepad holds which gamepad was altered, if any
	RGFW_Event.button holds which gamepad button was pressed

	RGFW_Event.axis holds the data of all the axis
	RGFW_Event.axisCount says how many axis there are

"""

windowMoved = 9 #!< the window was moved (by the user) */
windowResized = 10 #!< the window was resized (by the user) */
"""
# attribs change event note
	The event data is sent straight to the window structure
	with win->r.x, win->r.y, win->r.w and win->r.h
"""

focusIn = 12 #!< window is in focus now */
focusOut = 13 #!< window is out of focus now */

""" attribs change event note
	The event data is sent straight to the window structure
	with win->r.x, win->r.y, win->r.w and win->r.h
"""

mouseEnter = 14 #* mouse entered the window */
mouseLeave =15 #* mouse left the window */

windowRefresh = 16 #* The window content needs to be refreshed */


quit = 16 #!< the user clicked the quit button*/ 
dnd = 17 #!< a file has been dropped into the window*/
dnd_init = 18 #!< the start of a dnd event, when the place where the file drop is known */
"""
 dnd data note
	The x and y coords of the drop are stored in the point RGFW_Event.point

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

GP_A = 0 # or PS X button */
GP_B = 1 # or PS circle button */
GP_Y = 2 # or PS triangle button */
GP_X = 3 # or PS square button */
GP_START = 9 # start button */
GP_SELECT = 8 # select button */
GP_HOME = 10 # home button */
GP_UP = 13 # dpad up */
GP_DOWN = 14 # dpad down*/
GP_LEFT = 15 # dpad left */
GP_RIGHT = 16 # dpad right */
GP_L1 = 4 # left bump */
GP_L2 = 5 # left trigger*/
GP_R1 = 6 # right bumper */
GP_R2 = 7 # right trigger */
GP_L3 = 11 # left thumb stick */
GP_R3 = 12  # !< right thumb stick */

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

def setClassName(str):
    c_string = ctypes.c_char_p(str.encode('utf-8'))
    lib.RGFW_csetClassName(c_string)

def RGFW_setBufferSize(area):
    lib.RGFW_setBufferSize(area)

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

# ! returns true if the key should be shifted */
def shouldShift(keycode, lockState):
    return lib.RGFW_shouldShift(keycode, lockState)

# ! get char from RGFW keycode (using a LUT), uses shift'd version if shift = true */
def keyCodeToChar(keycode, shift):
    return lib.RGFW_keyCodeToChar(keycode, shift)

# ! get char from RGFW keycode (using a LUT), uses lockState for shouldShift) */
def keyCodeToCharAuto(keycode, lockState):
    return lib.RGFW_keyCodeToCharAuto(keycode, lockState)

def isPressed(win, key):
    return lib.RGFW_isPressed(win, key)

def isReleased(win, key):
    return lib.RGFW_isReleased(win, key)

def isClicked(win, key):
    return lib.RGFW_isClicked(win, key)

def isMousePressed(win, key):
    return lib.RGFW_isMousePressed(win, key)

def wasMousePressed(win, key):
    return lib.RGFW_wasMousePressed(win, key)

def isMouseReleased(win, key):
    return lib.RGFW_isMouseReleased(win, key)

def readClipboard(size):
    return lib.RGFW_readClipboard(size)
    
def clipboardFree(string):
    return lib.RGFW_clipboardFree(string)

def writeClipboard(text):
    c_string = ctypes.c_char_p(text.encode('utf-8'))
    return lib.RGFW_writeClipboard(c_string, len(text))

def createThread(function_ptr, args):
    return lib.RGFW_createThread(function_ptr, args)

def cancelThread(thread):
    return lib.RGFW_cancelThread(thread)

def joinThread(thread):
    return lib.RGFW_joinThread(thread)

def setThreadPriority(thread, priority):
    return lib.RGFW_setThreadPriority(thread, priority)

def registerGamepad(win, gpNumber):
    return lib.RGFW_registerGamepad(win, gpNumber)

def registerGamepadF(win, file):
    return lib.RGFW_registerGamepadF(win, file)

def isPressedGP(win, controller, button):
    return lib.RGFW_isPressedGP(win, controller, button)

def setGLStencil(stencil):
    return lib.RGFW_setGLStencil(stencil)

def setGLSamples(samples):
    return lib.RGFW_setGLSamples(samples)

def setGLStereo(stereo):
    return lib.RGFW_setGLStereo(stereo)

def setGLAuxBuffers(auxBuffers):
    return lib.RGFW_setGLAuxBuffers(auxBuffers)

def setDoubleBuffer(useDoubleBuffer): 
    return lib.RGFW_setDoubleBuffer(useDoubleBuffer)


GL_CORE = 0
GL_COMPATIBILITY = 1

def setGLVersion(profile, major, minor):
    return lib.RGFW_setGLVersion(profile, major, minor)

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

def stopCheckEvents():
    return lib.RGFW_stopCheckEvents(this)

def setWindowMoveCallback(func): 
    lib.RGFW_setWindowMoveCallback(func)
def setWindowResizeCallback(func): 
    lib.RGFW_setWindowResizeCallback(func)
def setWindowQuitCallback(func): 
    lib.RGFW_setWindowQuitCallback(func)
def setMousePosCallback(func): 
    lib.RGFW_setMousePosCallback(func)
def setWindowRefreshCallback(func): 
    lib.RGFW_setWindowRefreshCallback(func)
def setFocusCallback(func): 
    nfunc = FOCUSCALLBACK(func)
    lib.RGFW_setFocusCallback(nfunc)

def setMouseNotifyCallback(func): 
    lib.RGFW_setMouseNotifyCallBack(func)
def setDndCallback(func): 
    lib.RGFW_setDndCallback(func)
def setDndInitCallback(func): 
    lib.RGFW_setDndInitCallback(func)
def setKeyCallback(func): 
    lib.RGFW_setKeyCallback = func 
def setMouseButtonCallback(func): 
    lib.RGFW_setMouseButtonCallback(func)
def setgpButtonCallback(func): 
    lib.RGFW_setgpButtonCallback(func)
def setgpAxisCallback(func):
    lib.RGFW_setgpAxisCallback(func)

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
