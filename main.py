import cv2
import time

from HandTrack.hand_detector import HandDetector
from gestures.clap import ClapDetector
from gestures.launcher import AppLauncher
from display import draw_hud, draw_gesture_hint, draw_flash_banner


FLASH_DURATION = 2.0


def main() -> None:
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    detector = HandDetector(max_hands=2)
    clap     = ClapDetector(clap_threshold=130, apart_threshold=200, cooldown_sec=1.5)
    launcher = AppLauncher()

    prev_time   = 0.0
    flash_until = 0.0

    print("Iniciando Hand Gesture Controller — presiona 'q' para salir.")

    while True:
        success, img = cap.read()
        if not success:
            print("No se pudo leer el frame. Verifica la cámara.")
            break

        img = cv2.flip(img, 1)

        img       = detector.find_hands(img)
        all_hands = detector.find_all_positions(img)

        lm_list      = all_hands[0] if all_hands else []
        finger_count = 0
        hand_state   = "Sin mano"

        if lm_list:
            detector.find_position(img, hand_no=0)
            finger_count = detector.count_fingers()
            hand_state   = detector.get_hand_state(finger_count)

        hand0 = all_hands[0] if len(all_hands) > 0 else []
        hand1 = all_hands[1] if len(all_hands) > 1 else []

        if clap.update(hand0, hand1):
            launcher.open("Spotify")
            flash_until = time.time() + FLASH_DURATION

        curr_time = time.time()
        fps       = int(1 / (curr_time - prev_time)) if prev_time else 0
        prev_time = curr_time

        draw_hud(img, fps, finger_count, hand_state)
        draw_gesture_hint(img)

        if curr_time < flash_until:
            draw_flash_banner(img, "¡Abriendo Spotify!")

        cv2.imshow("Hand Gesture Controller — Fase 1", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()