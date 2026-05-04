import cv2


# Colores HUD (BGR)
COLOR_FPS    = (0, 255, 0)
COLOR_FINGER = (255, 255, 0)
COLOR_STATE  = (0, 200, 255)
COLOR_FLASH  = (0, 255, 255)


def draw_hud(img, fps: int, finger_count: int, hand_state: str) -> None:
    """Dibuja FPS, conteo de dedos y estado de la mano sobre el frame."""
    cv2.putText(img, f"FPS: {fps}",            (15, 45),  cv2.FONT_HERSHEY_SIMPLEX, 1.1, COLOR_FPS,    2)
    cv2.putText(img, f"Dedos: {finger_count}", (15, 95),  cv2.FONT_HERSHEY_SIMPLEX, 1.1, COLOR_FINGER, 2)
    cv2.putText(img, f"Mano:  {hand_state}",   (15, 145), cv2.FONT_HERSHEY_SIMPLEX, 1.1, COLOR_STATE,  2)


def draw_gesture_hint(img) -> None:
    """Muestra el hint del gesto disponible en la esquina inferior izquierda."""
    h = img.shape[0]
    cv2.putText(img, "Gesto: Aplaudir -> Spotify",
                (15, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (180, 180, 180), 1)


def draw_flash_banner(img, message: str) -> None:
    """Banner centrado que confirma que el gesto fue reconocido."""
    h, w = img.shape[:2]
    cv2.rectangle(img, (0, h // 2 - 50), (w, h // 2 + 50), (0, 0, 0), -1)
    text_size = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, 1.4, 3)[0]
    x = (w - text_size[0]) // 2
    cv2.putText(img, message, (x, h // 2 + 15),
                cv2.FONT_HERSHEY_SIMPLEX, 1.4, COLOR_FLASH, 3)