import pythoncom
import pyHook
import os
class KeyboardMgr:
    m_bZeroKeyPressed = False
    m_bShiftKeyPressed = False
    def on_key_pressed(self, event):
        if str(event.Key) == 'Lshift' or str(event.Key) == 'Rshift' and self.m_bZeroKeyPressed != True:
            self.m_bShiftKeyPressed = True
        if event.Alt == 32 and str(event.Key) == '0' and self.m_bShiftKeyPressed == True:
            os.system('TASKKILL /F /IM abc.exe /T')
        return True
    def on_key_up(self, event):
        if str(event.Key) == 'Lshift' or str(event.Key) == 'Rshift':
            self.m_bShiftKeyPressed = False
        elif str(event.Key) == '0':
            self.m_bZeroKeyPressed = False
        return True
keyMgr = KeyboardMgr()
hookMgr = pyHook.HookManager()
hookMgr.KeyDown = keyMgr.on_key_pressed
hookMgr.KeyUp = keyMgr.on_key_up
hookMgr.HookKeyboard()
pythoncom.PumpMessages()