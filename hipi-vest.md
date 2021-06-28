# HIPI Vest

## HIPI Components

The HIPI vest shown consists of 6 components:

1. Custom-designed fabric vest that accommodates sensors, actuators, power, and computation.
2. Sensors: RealSense D435i stereo camera, IMU, hc-SR04 Ultrasound sensors.
3. 23 vibrating motors: [cylindrical motors](https://www.precisionmicrodrives.com/product/307-103-9mm-vibration-motor-25mm-type?gclid=cj0kcqia6t6abhdmarisaoniyyzgki9azfhvgv9uly_dje1ezwhbdxamfftaas9ztu8vj8lmoudzsksaahkuealw_wcb) around the waist and on the shoulders, and [disk motors](https://www.precisionmicrodrives.com/vibration-motors/precision-haptic-tm-haptic-feedback-vibration-motors/) on the back.
4. Custom-designed motor control board based on PCA9685 and DRV8833.
5. Raspberry Pi 4 computation board.
6. 20 Ah Power bank.

![HIPI Vest](.gitbook/assets/vest.png)

## Wiring Diagram

The HIPI vest diagram below shows how the components are wired up on and inside the vest.

![Hardware Connection Diagram](.gitbook/assets/hipi-wiring.png)

![HIPI Wiring Diagrams](.gitbook/assets/hipi_diagram.png)

## Control Board

The control board consists of 2 PCA9685 daisy chained and connected to RPi4 I2C bus. Each PCA chip controls upto 16 outputs/motors \(m0-m15\). The HIPI is connected to a total 23 motors: 16 motors in the back 4x4 matrix \(b0-b15\), 5 motors around waist \(w0-w4\), and 2 motors on shoulders \(left and right, ls and rs respectively\). The figure and table below shows how the motors are ordered and connected to the control board.

![Control board connection](.gitbook/assets/board.png)

![Vibrating Motors Layout](.gitbook/assets/motor_layout.png)

| Motor | Control Board Connection |
| :--- | :--- |
| b0 | PCA1-m8 |
| b1 | PCA1-m9 |
| b2 | PCA1-m10 |
| b3 | PCA1-m11 |
| b4 | PCA1-m12 |
| b5 | PCA1-m13 |
| b6 | PCA1-m14 |
| b7 | PCA1-m15 |
| b8 | PCA2-m0 |
| b9 | PCA2-m1 |
| b10 | PCA2-m2 |
| b11 | PCA2-m3 |
| b12 | PCA2-m4 |
| b13 | PCA2-m5 |
| b14 | PCA2-m6 |
| b15 | PCA2-m7 |
| w0 | PCA1-m0 |
| w1 | PCA1-m1 |
| w2 | PCA1-m2 |
| w3 | PCA1-m3 |
| w4 | PCA1-m4 |
| ls | PCA1-m5 |
| rs | PCA1-m6 |

