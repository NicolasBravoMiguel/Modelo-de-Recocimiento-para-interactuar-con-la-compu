import math
import time


class ClapDetector:
    """
    Detecta el gesto de aplaudir: ambas manos se acercan por debajo de un umbral
    después de haber estado separadas.

    Máquina de estados:
        APART  →  (distancia < clap_threshold)  →  TOGETHER  →  dispara acción
        TOGETHER  →  (distancia >= apart_threshold)  →  APART

    El cooldown evita disparos repetidos si las manos permanecen juntas.
    """

    # Landmark 9 = MCP del dedo medio (centro de la palma) — mejor punto de referencia que la muñeca
    _PALM_CENTER_ID = 9

    def __init__(self, clap_threshold: int = 130, apart_threshold: int = 200,
                 cooldown_sec: float = 1.5):
        self._clap_threshold = clap_threshold
        self._apart_threshold = apart_threshold
        self._cooldown_sec = cooldown_sec
        self._hands_apart = True
        self._last_clap_time = 0.0

    def update(self, lm_list_0: list, lm_list_1: list) -> bool:
        """
        Recibe los landmarks de ambas manos y devuelve True en el frame en que
        se detecta un aplauso. Devuelve False en cualquier otro caso.
        """
        if not lm_list_0 or not lm_list_1:
            # Si falta alguna mano, reiniciamos el estado
            self._hands_apart = True
            return False

        dist = self._palm_distance(lm_list_0, lm_list_1)
        now = time.time()

        if dist < self._clap_threshold:
            if self._hands_apart and (now - self._last_clap_time) >= self._cooldown_sec:
                self._hands_apart = False
                self._last_clap_time = now
                return True
            self._hands_apart = False
        elif dist > self._apart_threshold:
            self._hands_apart = True

        return False

    def _palm_distance(self, lm0: list, lm1: list) -> float:
        """Distancia euclidiana entre los centros de ambas palmas."""
        x0, y0 = lm0[self._PALM_CENTER_ID][1], lm0[self._PALM_CENTER_ID][2]
        x1, y1 = lm1[self._PALM_CENTER_ID][1], lm1[self._PALM_CENTER_ID][2]
        return math.hypot(x1 - x0, y1 - y0)