import cv2
import mediapipe as mp


class HandDetector:
    """
    Detecta y rastrea landmarks de manos usando MediaPipe.
    Soporta una o dos manos; espera imagen ya volteada (espejo).
    """

    # Índices de los tips de los 4 dedos (sin pulgar) y sus articulaciones PIP
    _FINGERTIP_IDS = [8, 12, 16, 20]
    _FINGER_PIP_IDS = [6, 10, 14, 18]

    def __init__(self, max_hands: int = 1, detection_confidence: float = 0.7,
                 tracking_confidence: float = 0.7):
        self._mp_hands = mp.solutions.hands
        self._hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            model_complexity=0,               # 0 = más rápido, suficiente para tiempo real
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self._mp_draw = mp.solutions.drawing_utils
        self._mp_styles = mp.solutions.drawing_styles

        self._results = None
        self._lm_list: list[list[int]] = []
        self._handedness_label: str = ""

    # ------------------------------------------------------------------
    # Interfaz pública
    # ------------------------------------------------------------------

    def find_hands(self, img, draw: bool = True):
        """
        Procesa el frame y dibuja los landmarks de todas las manos detectadas.
        Recibe y devuelve imagen BGR (ya volteada con cv2.flip si se desea espejo).
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self._results = self._hands.process(img_rgb)

        if self._results.multi_hand_landmarks and draw:
            for hand_lms in self._results.multi_hand_landmarks:
                self._mp_draw.draw_landmarks(
                    img,
                    hand_lms,
                    self._mp_hands.HAND_CONNECTIONS,
                    self._mp_styles.get_default_hand_landmarks_style(),
                    self._mp_styles.get_default_hand_connections_style(),
                )
        return img

    def find_position(self, img, hand_no: int = 0) -> list[list[int]]:
        """
        Devuelve lista de [id, x, y] para cada landmark de la mano especificada.
        También almacena la etiqueta de lateralidad ("Left" / "Right").
        """
        self._lm_list = []
        self._handedness_label = ""

        if not (self._results and self._results.multi_hand_landmarks):
            return self._lm_list

        if hand_no >= len(self._results.multi_hand_landmarks):
            return self._lm_list

        h, w, _ = img.shape
        for lm_id, lm in enumerate(self._results.multi_hand_landmarks[hand_no].landmark):
            self._lm_list.append([lm_id, int(lm.x * w), int(lm.y * h)])

        if self._results.multi_handedness:
            classification = self._results.multi_handedness[hand_no].classification[0]
            self._handedness_label = classification.label   # "Left" o "Right"

        return self._lm_list

    def count_fingers(self) -> int:
        """
        Cuenta cuántos dedos están extendidos (0-5).
        Requiere haber llamado find_position() primero.
        """
        if not self._lm_list:
            return 0

        fingers = []

        # Pulgar: se compara en eje X porque se extiende lateralmente.
        # En imagen espejo: "Right" (MediaPipe) = mano derecha del usuario.
        # Mano derecha: tip.x < cmc.x cuando está extendido hacia la izquierda (afuera).
        if self._handedness_label == "Right":
            fingers.append(1 if self._lm_list[4][1] < self._lm_list[2][1] else 0)
        else:
            fingers.append(1 if self._lm_list[4][1] > self._lm_list[2][1] else 0)

        # Los cuatro dedos restantes: extendidos cuando tip.y < pip.y (más arriba en pantalla)
        for tip_id, pip_id in zip(self._FINGERTIP_IDS, self._FINGER_PIP_IDS):
            fingers.append(1 if self._lm_list[tip_id][2] < self._lm_list[pip_id][2] else 0)

        return sum(fingers)

    def get_hand_state(self, finger_count: int) -> str:
        """Devuelve estado descriptivo de la mano según dedos extendidos."""
        if finger_count == 5:
            return "Abierta"
        if finger_count == 0:
            return "Cerrada"
        return f"Parcial ({finger_count})"

    def find_all_positions(self, img) -> list[list[list[int]]]:
        """
        Devuelve una lista con los lm_list de cada mano detectada.
        Útil para gestos que requieren dos manos simultáneas.
        """
        if not (self._results and self._results.multi_hand_landmarks):
            return []
        count = len(self._results.multi_hand_landmarks)
        result = []
        for i in range(count):
            self.find_position(img, hand_no=i)
            result.append(list(self._lm_list))
        return result

    def hand_detected(self) -> bool:
        """True si hay al menos una mano visible en el frame actual."""
        return bool(self._results and self._results.multi_hand_landmarks)