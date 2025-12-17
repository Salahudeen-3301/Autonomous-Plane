import cv2
import time
from dronekit import connect, VehicleMode
from yaw_utils import condition_yaw
from Video_Track import Track
from ultralytics import YOLO

# ---------- CONFIG ----------
CONNECTION_STR = "udp:127.0.0.1:14550"
CAM_INDEX = 0
FRAME_W, FRAME_H = 416, 416

TRACKING_CH = 7          # RC channel for enabling tracking
TRACKING_THRESHOLD = 1500

K_heading = 20.0
MAX_NUDGE_DEG = 12.0

DETECTION_GRACE_S = 2.0      # brief loss tolerance
LOITER_TIME_S = 180.0        # 3 minutes

STATE_AUTO = "AUTO"
STATE_TRACKING = "TRACKING"
STATE_LOITERING = "LOITERING"
model = YOLO("yolo11n.pt")
# ----------------------------

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def detect_person(frame):
    Track(frame)
    return None

def main():
    print("Connecting to vehicle...")
    vehicle = connect(CONNECTION_STR, wait_ready=True, heartbeat_timeout=30)

    cap = cv2.VideoCapture(CAM_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)

    state = STATE_AUTO
    last_seen_time = None
    loiter_start_time = None

    print("Starting autonomy state machine with RC gating")

    try:
        while True:
            now = time.time()
            mode = vehicle.mode.name

            # Read RC channel for tracking
            ch_val = vehicle.channels.get(str(TRACKING_CH), 0)
            tracking_enabled = int(ch_val) > TRACKING_THRESHOLD

            # ---------- AUTO (mission flying) ----------
            if state == STATE_AUTO:
                if mode != "AUTO":
                    vehicle.mode = VehicleMode("AUTO")
                    time.sleep(1)
                    continue

                if not tracking_enabled:
                    # Nothing else to do; keep flying mission
                    time.sleep(0.05)
                    continue

                ret, frame = cap.read()
                if not ret:
                    continue

                det = detect_person(frame)
                if det is not None:
                    print("Human detected -> switching to GUIDED")
                    vehicle.mode = VehicleMode("GUIDED")
                    state = STATE_TRACKING
                    last_seen_time = now
                    time.sleep(1)

            # ---------- TRACKING (GUIDED) ----------
            elif state == STATE_TRACKING:
                if mode != "GUIDED":
                    print("GUIDED exited by pilot -> returning to AUTO")
                    state = STATE_AUTO
                    continue

                if not tracking_enabled:
                    print("Tracking switch OFF -> resuming AUTO")
                    vehicle.mode = VehicleMode("AUTO")
                    state = STATE_AUTO
                    continue

                ret, frame = cap.read()
                if not ret:
                    continue

                det = detect_person(frame)
                if det is None:
                    # No detection
                    if last_seen_time and (now - last_seen_time > DETECTION_GRACE_S):
                        print("Target lost -> switching to LOITER")
                        vehicle.mode = VehicleMode("LOITER")
                        state = STATE_LOITERING
                        loiter_start_time = now
                        time.sleep(1)
                    continue

                # Target detected
                last_seen_time = now
                cx, cy, bw, bh = det

                # Compute horizontal error
                err_x = (cx - FRAME_W / 2) / (FRAME_W / 2)
                nudge = clamp(K_heading * err_x, -MAX_NUDGE_DEG, MAX_NUDGE_DEG)

                # Send relative yaw nudge
                print(f"Tracking: err={err_x:.2f}, nudge={nudge:.2f}")
                condition_yaw(vehicle, nudge, yaw_rate=5, relative=True)

                time.sleep(0.2)

            # ---------- LOITERING ----------
            elif state == STATE_LOITERING:
                if mode != "LOITER":
                    vehicle.mode = VehicleMode("LOITER")
                    time.sleep(1)
                    continue

                ret, frame = cap.read()
                if ret and tracking_enabled:
                    det = detect_person(frame)
                    if det is not None:
                        print("Target reacquired -> GUIDED")
                        vehicle.mode = VehicleMode("GUIDED")
                        state = STATE_TRACKING
                        last_seen_time = now
                        time.sleep(1)
                        continue

                if now - loiter_start_time > LOITER_TIME_S or not tracking_enabled:
                    print("Loiter timeout or tracking disabled -> resuming AUTO")
                    vehicle.mode = VehicleMode("AUTO")
                    state = STATE_AUTO
                    time.sleep(1)

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("User interrupt")

    finally:
        print("Closing")
        cap.release()
        vehicle.close()


if __name__ == "__main__":
    main()
