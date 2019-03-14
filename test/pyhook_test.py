import pyHook
import pythoncom

class KeyBoardManager(object):
    keyIsPressed = False
    def onKeyDown(self,event):
        print(str(event.Key) + ' is pressed')
        self.keyIsPressed = True
        return True


if __name__ == '__main__':
    ss = KeyBoardManager()
    hookmanager = pyHook.HookManager()
    hookmanager.KeyDown = ss.onKeyDown
    hookmanager.HookKeyboard()


    pythoncom.PumpMessages()