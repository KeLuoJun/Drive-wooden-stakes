import keyboard
import mss
import cv2
import numpy
from time import time, sleep
import pyautogui

# 设置全局暂停时间为 0 秒
pyautogui.PAUSE = 0

print("Press 's' to start playing.")
print("Once started press 'q' to quit.")
keyboard.wait('s')
left = True
x = 340
y = 850
sct = mss.mss()
dimensions_left = {
    'left': 290,
    'top': 600,
    'width': 150,
    'height': 250
}
dimensions_right = {
    'left': 520,
    'top': 600,
    'width': 150,
    'height': 250
}

wood_left = cv2.imread('./images/woodleft.jpg', cv2.IMREAD_GRAYSCALE)
wood_right = cv2.imread('./images/woodright.jpg', cv2.IMREAD_GRAYSCALE)
w = wood_left.shape[1]
h = wood_left.shape[0]

fps_time = time()
while True:
    if left:
        scr = numpy.array(sct.grab(dimensions_left))
        wood = wood_left
    else:
        scr = numpy.array(sct.grab(dimensions_right))
        wood = wood_right
    # scr_gray= scr[:, :, 3]
    scr_gray = cv2.cvtColor(scr, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(scr_gray, wood, cv2.TM_CCOEFF_NORMED)

    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    print(f"Max Val: {max_val}, Max Loc: {max_loc}")
    scr = scr.copy()
    if max_val > .85:
        left = not left
        if left:
            x = 340
        else:
            x = 600
        cv2.rectangle(scr, max_loc, (max_loc[0] + w, max_loc[1] + h),
                      (0, 255, 255), 2)
        
    cv2.imshow('Screen Shot', scr)
    cv2.waitKey(1)
    pyautogui.click(x=x, y=y)
    sleep(.01)
    if keyboard.is_pressed('q'):
        break

    print('FPS: {}'.format(1 / (time() - fps_time)))
    fps_time = time()