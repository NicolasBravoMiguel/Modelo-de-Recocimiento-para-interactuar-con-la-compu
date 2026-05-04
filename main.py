import cv2
import time
from hand_detector import HandDetector


# Colores HUD (BGR)
COLOR_FPS    = (0, 255, 0)      # verde
COLOR_FINGER = (255, 255, 0)    # cian
COLOR_STATE  = (0, 200, 255)    # amarillo-naranja
COLOR_WARN   = (0, 80, 255)     # rojo-naranja


def draw_hud(img, fps: int, finger_count: int, hand_state: str) -> None:
    """Dibuja el HUD con FPS, dedos y estado sobre el frame."""
    cv2.putText(img, f"FPS: {fps}",            (15, 45),  cv2.FONT_HERSHEY_SIMPLEX, 1.1, COLOR_FPS,    2)
    cv2.putText(img, f"Dedos: {finger_count}", (15, 95),  cv2.FONT_HERSHEY_SIMPLEX, 1.1, COLOR_FINGER, 2)
    cv2.putText(img, f"Mano:  {hand_state}",   (15, 145), cv2.FONT_HERSHEY_SIMPLEX, 1.1, COLOR_STATE,  2)


def main() -> None:
    # Índice 0 = cámara integrada del Mac (FaceTime HD)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    detector = HandDetector(max_hands=1)
    prev_time = 0.0

    print("Iniciando Hand Gesture Controller — presiona 'q' para salir.")

    while True:
        success, img = cap.read()
        if not success:
            print("No se pudo leer el frame. Verifica la cámara.")
            break

        # Voltear horizontalmente para vista espejo natural
        img = cv2.flip(img, 1)

        # Detección
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)

        finger_count = 0
        hand_state = "Sin mano"

        if lm_list:
            finger_count = detector.count_fingers()
            hand_state = detector.get_hand_state(finger_count)

        # Calcular FPS
        curr_time = time.time()
        fps = int(1 / (curr_time - prev_time)) if prev_time else 0
        prev_time = curr_time

        draw_hud(img, fps, finger_count, hand_state)

        cv2.imshow("Hand Gesture Controller — Fase 1", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()