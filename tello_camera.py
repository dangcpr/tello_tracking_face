import sys
import cv2
from djitellopy import tello
import const as const
from face_tracking import FaceTracker

tello_controller = tello.Tello()
face_tracker = FaceTracker()


def connectDrone():
    """Connect to the drone."""
    tello_controller.connect()


def takeoffDrone():
    """Take off from the drone."""
    try:
        tello_controller.takeoff()
    except Exception as e:
        print("Takeoff error:", e)


def landDrone():
    """Land on the drone."""
    tello_controller.land()


def moveDrone(distance, keyboard):
    """Move the drone in a given direction by a given distance."""
    print('start ' + keyboard)
    if keyboard == const.MOVE_FORWARD:
        tello_controller.move_forward(distance)
    elif keyboard == const.MOVE_BACKWARD:
        tello_controller.move_back(distance)
    elif keyboard == const.MOVE_LEFT:
        tello_controller.move_left(distance)
    elif keyboard == const.MOVE_RIGHT:
        tello_controller.move_right(distance)
    elif keyboard == const.MOVE_UP:
        tello_controller.move_up(distance)
    elif keyboard == const.MOVE_DOWN:
        tello_controller.move_down(distance)
    elif keyboard == const.TAKEOFF:
        tello_controller.takeoff()
    elif keyboard == const.LAND:
        tello_controller.land()
    print('end ' + keyboard)


def on_key_press(key):
    """Handle key press events."""
    if key == ord("w") or key == ord("W"):
        moveDrone(30, const.MOVE_FORWARD)
    elif key == ord("s") or key == ord("S"):
        moveDrone(30, const.MOVE_BACKWARD)
    elif key == ord("a") or key == ord("A"):
        moveDrone(30, const.MOVE_LEFT)
    elif key == ord("d") or key == ord("D"):
        moveDrone(30, const.MOVE_RIGHT)
    elif key == ord("q") or key == ord("Q"):
        moveDrone(30, const.MOVE_UP)
    elif key == ord("e") or key == ord("E"):
        moveDrone(30, const.MOVE_DOWN)
    elif key == ord("l") or key == ord("L"):
        landDrone()
    elif key == ord("t") or key == ord("T"):
        takeoffDrone()
    elif key == 27:  # Escape key
        sys.exit(0)


def open_camera():
    """Open the drone's camera stream."""
    tello_controller.streamon()
    print("tello battery:", tello_controller.get_battery())
    frame_read = tello_controller.get_frame_read()

    print("Camera initialized. Press keys to control:")
    print("W/S - Forward/Backward")
    print("A/D - Left/Right")
    print("Q/E - Up/Down")
    print("T - Takeoff | L - Land | ESC - Exit")

    while True:
        frame = frame_read.frame
        
        info = face_tracker.findFace(frame, cv2)
        face_tracker.trackFace(info, const.SCREEN_WIDTH, const.SCREEN_HEIGHT, tello_controller)
    
        cv2.resize(frame, (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        cv2.imshow("Tello Camera", frame)

        key = cv2.waitKey(1) & 0xFF
        if key != 255:  # 255 means no key pressed
            on_key_press(key)

    # Stop stream, turn off, and close window
    # tello_controller.streamoff()
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    connectDrone()
    face_tracker = FaceTracker()
    print("Drone control active. Press keys to control:")
    print("W/S - Forward/Backward")
    print("A/D - Left/Right")
    print("Q/E - Up/Down")
    print("T - Takeoff")
    print("L - Land")
    print("ESC - Disconnect and Exit")

    try:
        open_camera()
    except Exception as e:
        print(f"Error: {e}")
