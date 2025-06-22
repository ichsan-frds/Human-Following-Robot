import cv2
import mediapipe as mp
import serial

# Inisialisasi koneksi serial dengan Arduino
arduino = serial.Serial('COM4', 9600)  # Ganti COM3 dengan port Anda

# Inisialisasi MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)  # Kamera sebagai feed video

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Tidak ada frame yang diambil.")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Logika untuk menentukan pergerakan
        nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
        if nose.x < 0.4:  # Jika hidung berada di sisi kiri
            print("Belok kiri")
            arduino.write(b'L')  # Mengirimkan perintah 'L' ke Arduino
        elif nose.x > 0.6:  # Jika hidung berada di sisi kanan
            print("Belok kanan")
            arduino.write(b'R')  # Mengirimkan perintah 'R' ke Arduino
        else:  # Jika hidung di tengah
            print("Maju")
            arduino.write(b'F')  # Mengirimkan perintah 'F' ke ArduinoQ
    else:
        print("Berhenti")
        arduino.write(b'S')  # Mengirimkan perintah 'S' ke Arduino

    cv2.imshow("Video Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()