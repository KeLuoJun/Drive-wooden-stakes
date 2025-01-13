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
x = 1000  # 鼠标点击位置
y = 1150
sct = mss.mss()
# 设置要截取的屏幕区域
dimensions_left = {
    'left': 900,
    'top': 800,
    'width': 350,
    'height': 600
}
dimensions_right = {
    'left': 1350,
    'top': 800,
    'width': 300,
    'height': 600
}

wood_left = cv2.imread('./images/woodleft.png', cv2.IMREAD_UNCHANGED)
wood_right = cv2.imread('./images/woodright.png', cv2.IMREAD_UNCHANGED)
wood_left = wood_left[:, :, :3]
wood_right = wood_right[:, :, :3]
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
    scr_gray= scr[:, :, :3]

    result = cv2.matchTemplate(scr_gray, wood, cv2.TM_CCOEFF_NORMED)

    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    print(f"Max Val: {max_val}, Max Loc: {max_loc}")
    scr = scr.copy()
    if max_val > .85:
        left = not left
        if left:
            x = 1000
        else:
            x = 1500
        cv2.rectangle(scr, max_loc, (max_loc[0] + w, max_loc[1] + h),
                      (0, 255, 255), 2)

    # 创建窗口并设置窗口属性
    # 保持窗口不被覆盖
    cv2.namedWindow('Screen Shot', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Screen Shot', cv2.WND_PROP_TOPMOST, 1)

    # 显示图像
    cv2.imshow('Screen Shot', scr)
    cv2.moveWindow('Screen Shot', 300, 400)  # 将窗口移动到屏幕 (100, 100) 位置
    cv2.waitKey(1)
    pyautogui.click(x=x, y=y)
    sleep(.02)

    if keyboard.is_pressed('q'):
        break

    print('FPS: {}'.format(1 / (time() - fps_time)))
    fps_time = time()