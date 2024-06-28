import RGFW
from OpenGL.GL import *

icon = [0xFF, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0xFF, 0xFF, 0xFF, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0xFF]
running = 1

def main():
    global win2
    global running
    
    win = RGFW.createWindow("RGFW Example Window", RGFW.rect(500, 500, 500, 500), RGFW.ALLOW_DND | RGFW.CENTER)
    win.makeCurrent()

    win.setIcon(icon, RGFW.area(3, 3), 4)

    win.swapInterval(1)

    win.buffer[0] = 1

    win2 = RGFW.createWindow("subwindow", RGFW.rect(200, 200, 200, 200), 0)

    glEnable(GL_BLEND)
    
    glEnable(GL_BLEND)             
    glClearColor(0, 0, 0, 0)
    
    while (RGFW.window.shouldClose(win) == False):
        win2.checkEvent()
        while (win.checkEvent()):
            if (win.event.type == RGFW.RGFW_windowMoved):
                print("window moved")
            elif (win.event.type == RGFW.RGFW_windowResized):
                print("window resized")
            if (win.event.type == RGFW.quit):
                running = 0  
                break
            
            if (RGFW.isPressedI(win, RGFW.Up)):
                string = RGFW.readClipboard(None)
                print("Pasted : ", RGFW.cstrToStr(string))

            elif (RGFW.isPressedI(win, RGFW.Down)):
                RGFW.writeClipboard("DOWN")
            elif (RGFW.isPressedI(win, RGFW.Space)):
                print("fps : ", win.event.fps)
            elif (RGFW.isPressedI(win, RGFW.w)):
                win.setMouseDefault()
            elif (RGFW.isPressedI(win, RGFW.q)):
                win.showMouse(0)
            elif (RGFW.isPressedI(win, RGFW.t)):
                win.setMouse(icon, RGFW.area(3, 3), 4)
            
            if (win.event.type == RGFW.dnd):
                for i in range(win.event.droppedFilesCount):
                    print("dropped :", RGFW.cstrToStr(win.event.droppedFiles[i]))
            elif (win.event.type == RGFW.jsButtonPressed):
                print("pressed :", win.event.button)

            elif (win.event.type == RGFW.jsAxisMove and not win.event.button):
                print("{", win.event.axis[0].x, "} {", win.event.axis[0].y, "}")

        drawLoop(win)
        drawLoop(win2)
    
    win.close()

def drawLoop(w):
    w.makeCurrent()

    glClearColor(255, 255, 255, 255)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    
    glBegin(GL_TRIANGLES)

    glColor3f(1, 0, 0) 
    glVertex2f(-0.6, -0.75)

    glColor3f(0, 1, 0) 
    glVertex2f(0.6, -0.75)

    glColor3f(0, 0, 1) 
    glVertex2f(0, 0.75)

    glEnd()
    
    w.swapBuffers()


main()