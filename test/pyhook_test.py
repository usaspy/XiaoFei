import pyHook
import pythoncom

i =100
class KeyBoardManager(object):
    keyIsPressed = False
    def onKeyDown(self,event):
        #print(str(event.Key) + ' is pressed')
        fp = open("d:/1.txt", 'w')
        fp.write('Hello, world!')
        fp.close()
        self.keyIsPressed = True
        return True

if __name__ == '__main__':
    ss = KeyBoardManager()
    hookmanager = pyHook.HookManager()
    hookmanager.KeyDown = ss.onKeyDown
    hookmanager.HookKeyboard()


    pythoncom.PumpMessages()