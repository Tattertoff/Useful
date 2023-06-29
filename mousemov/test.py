import pyautogui

x,y = pyautogui.size()
x,y=int(str(x)),int(str(y))
print(x)
print(y)
pyautogui.dragTo(500, 100, duration=5) 
