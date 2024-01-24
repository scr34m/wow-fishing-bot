import pyautogui as pag
import time, sys, os
import cv2 as cv
import numpy as np
from loguru import logger
from mss import mss
from pynput.keyboard import Key, Listener

width = 100
height = 100
directory = '../images'
count = 0

def capture(img):
  global count
  import os
  if not os.path.exists(directory):
    os.makedirs(directory)
  cv.imwrite(directory + '/template' + str(count) + '.PNG', img)
  count = count + 1

def main():
  def cap(key):
    if key is Key.space: 
      logger.info("Captured")
      capture(im)

  logger.remove(0)
  logger.add(sys.stderr, format = "<green>{time:HH:mm:ss.SSS}</green> | <level>{message}</level>", colorize=True)

  logger.info("Press <space> to capture an image or <q> for quit")

  listener = Listener(
    on_release=cap)
  listener.start()

  with mss() as sct:
    while True:
      x, y = pag.position()
      area = {
        "top": int(y - height / 2),
        "left": int(x - width / 2),
        "width": int(width),
        "height": int(height)
      }
      im = np.array(sct.grab(area))
      cv.imshow('preview', im)

      key_bit = cv.waitKey(250) & 0xFF
      if key_bit == ord("q"):
        break
  cv.destroyAllWindows()

main()
