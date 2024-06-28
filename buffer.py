import RGFW

screenSize : RGFW.area

def drawRect(win, r, color):
    for x in range(r.w):
        for y in range(r.h):
            index = (r.y + y) * (4 * screenSize.w) + (r.x + x) * 4
            
            for i in range(3):
                win.buffer[index + i] = color[i]

def main():
    win = RGFW.createWindow("RGFW Example Window", RGFW.rect(500, 500, 500, 500), RGFW.ALLOW_DND | RGFW.CENTER)
    
    win.setGPURender(0)
    win.setCPURender(1)

    global screenSize
    screenSize = RGFW.getScreenSize()

    while (win.shouldClose() == False):
        while (win.checkEvent()):
            if (win.event.type == RGFW.quit):
                break
        
        if (win.event.type == RGFW.quit):
            break
        
        color1 = [0, 0, 255]
        drawRect(win, RGFW.rect(0, 0, win.r.w, win.r.h), color1)

        color2 = [255, 0, 0]
        drawRect(win, RGFW.rect(200, 200, 200, 200), color2)
        
        win.swapBuffers()
    
    win.close()
    
main()