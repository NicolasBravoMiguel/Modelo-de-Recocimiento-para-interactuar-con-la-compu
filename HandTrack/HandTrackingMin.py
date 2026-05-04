import cv2
import mediapipe as mp
import time


cap = cv2.VideoCapture(1)
# Camara 0 = Compu , Camara 1 = Telefono

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    succcess, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# El objeto solo utiliza rgb por lo que lo tienes que convertir para que lo lea

    results = hands.process(imgRGB)
#print(restults.multi_hand_landmarks) = checa si el objeto esta leyendo los valores

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark): # Enumemra cada punto segun el diseño de Hands lms
                # print(id, lm)

                # Asi se consigue los valores con el id de los difrentes valores de la manos
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h) #cx cento de x - cy centro de y
                print(id,cx,cy)
                if id == 4:
                    cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)


            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

# Display Los FPS en la camara
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
# Estructura de numero a texto para los FPS
    cv2.putText(img,str(int(fps)), (10,70) ,cv2.FONT_HERSHEY_PLAIN,3,
    (255,0,255),3)


    cv2.imshow("Image",img)
    cv2.waitKey(1)



