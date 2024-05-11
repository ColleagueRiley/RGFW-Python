import RGFW
from OpenGL.GL import *

icon = [0xFF, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0xFF, 0xFF, 0xFF, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0xFF]
running = 1

def main():
    global win2
    global running
 
    win = RGFW.createWindow(b"RGFW Example Window", RGFW.rect(500, 500, 500, 500), RGFW.ALLOW_DND | RGFW.CENTER)
    win.contents.makeCurrent()

    win.contents.setIcon(icon, RGFW.area(3, 3), 4)

    win.contents.swapInterval(1)

    win2 = RGFW.createWindow(b"subwindow", RGFW.rect(200, 200, 200, 200), 0)
    
    glEnable(GL_BLEND)
    
    glEnable(GL_BLEND)             
    glClearColor(0, 0, 0, 0)

    while (running and not RGFW.isPressedI(win, RGFW.Escape)):
        win2.contents.checkEvent()
        
        while (win.contents.checkEvent()):
            print(win.contents.event.type)

            if (win.contents.event.type == RGFW.windowAttribsChange):
                print("attribs changed\n")
            if (win.contents.event.type == RGFW.quit):
                running = 0  
                break
            
            if (RGFW.isPressedI(win, RGFW.Up)):
                str = RGFW.readClipboard(None)
                print("Pasted : ", str)
                RGFW.clipboardFree(str)
            
            elif (RGFW.isPressedI(win, RGFW.Down)):
                RGFW.writeClipboard("DOWN", 4)
            elif (RGFW.isPressedI(win, RGFW.Space)):
                print("fps : ", win.contents.event.fps)
            elif (RGFW.isPressedI(win, RGFW.w)):
                win.contents.setMouseDefault()
            elif (RGFW.isPressedI(win, RGFW.q)):
                win.contents.showMouse(0)
            elif (RGFW.isPressedI(win, RGFW.t)):
                win.contents.setMouse(icon, RGFW.area(3, 3), 4)
            
            if (win.contents.event.type == RGFW.dnd):
                for i in range(win.contents.event.droppedFilesCount):
                    print("dropped : ", win.contents.event.droppedFiles[i])
            

            elif (win.contents.event.type == RGFW.jsButtonPressed):
                print("pressed :", win.contents.event.button)

            elif (win.contents.event.type == RGFW.jsAxisMove and not win.contents.event.button):
                print("{", win.contents.event.axis[0].x, "} {", win.contents.event.axis[0].y, "}")

        drawLoop(win)
        drawLoop(win2)
    
    win.contents.close()

def drawLoop(w):
    w.contents.makeCurrent()

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
    
    w.contents.swapBuffers()


main()