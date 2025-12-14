# guided_tracking.py
import cv2
import time
from dronekit import connect
from yaw_utils import condition_yaw

# ---------- CONFIG ----------
CONNECTION_STR = "udp:127.0.0.1:14550"
CAM_INDEX = 0            # 0 for USB; for CSI with libcamera you'd adapt capture
FRAME_W, FRAME_H = 416, 416
TRACKING_CH = 7        # RC channel used as tracking enable switch
AUTONOMOUS_CH = 8      # RC channel used for autonomous following enable switch
TRACKING_THRESHOLD = 1500
K_heading = 20.0         # degrees per normalized x-error (tune)
max_nudge_deg = 12.0     # maximum heading change per command
detection_timeout_s = 2.0
FORWARD_SPEED = 10       # m/s - keep plane moving (handled by plane)
# ----------------------------

def detect_person(frame):
    """
    Placeholder detector.
    Replace with your model inference; return (cx, cy, w, h) in pixels for the best person
    or None if no person detected.
    """
    # --- naive color threshold placeholder (replace with real model) ---
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # fake "detection" if bright center
    h, w = gray.shape
    mean = gray[h//3:2*h//3, w//3:2*w//3].mean()
    if mean > 70:
        return (w//2, h//2, w//3, h//3)
    return None

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def main():
    print("Connecting to vehicle...")
    vehicle = connect(CONNECTION_STR, wait_ready=True, heartbeat_timeout=30)
    cap = cv2.VideoCapture(CAM_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)

    last_seen = 0
    try:
        while True:
            # 1) read flight mode and tracking switch
            mode = vehicle.mode.name
            ch_val = vehicle.channels.get(str(TRACKING_CH), None)
            tracking_switch_on = (ch_val is not None and int(ch_val) > TRACKING_THRESHOLD)

            # If not in GUIDED, do nothing (safe)
            if mode != "GUIDED" or not tracking_switch_on:
                # optional: reset timers
                last_seen = 0
                # Could optionally call a function to "hold heading" once
                time.sleep(0.1)
                continue

            # 2) read camera frame
            ret, frame = cap.read()
            if not ret:
                print("Camera read failed")
                time.sleep(0.1)
                continue

            # 3) run detection
            det = detect_person(frame)
            now = time.time()
            if det is None:
                # no detection
                if last_seen == 0:
                    last_seen = now  # start timeout
                elif now - last_seen > detection_timeout_s:
                    # lost target: go to LOITER (safe), then wait for pilot or reacquire
                    print("Target lost -> switching to LOITER")
                    vehicle.mode = vehicle.mode.mapping()['LOITER'] if hasattr(vehicle.mode, 'mapping') else 'LOITER'
                    # Alternatively: vehicle.mode = VehicleMode("LOITER")
                    last_seen = 0
                    continue
                else:
                    # short gap, hold heading
                    time.sleep(0.05)
                    continue
            else:
                # detected
                last_seen = now

                # compute center error
                cx, cy, bw, bh = det
                err_x_norm = (cx - (FRAME_W/2)) / (FRAME_W/2)    # -1..1

                # compute heading nudge
                nudge_deg = K_heading * err_x_norm
                nudge_deg = clamp(nudge_deg, -max_nudge_deg, max_nudge_deg)

                # send relative yaw nudge (relative=True)
                print(f"Detected: err={err_x_norm:.2f}, nudge={nudge_deg:.2f} deg")
                condition_yaw(vehicle, nudge_deg, yaw_rate=5, relative=True)

                # small sleep — controls command rate
                time.sleep(0.2)

    except KeyboardInterrupt:
        print("User interrupt")
    finally:
        print("Closing")
        cap.release()
        vehicle.close()

if __name__ == "__main__":
    main()
