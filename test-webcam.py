from .. import init


cam = init.init_local_camera()
cam.save_photo('test.jpg')

cam.release()