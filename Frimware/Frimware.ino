#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm(0x40);

//PCA9685
#define SERVO_MIN 110
#define SERVO_MAX 500

#define MOVE_INTERVAL 20
#define MOVE_STEP 1

// Servo channels
#define BASE_CH       0
#define SHOULDER_CH  1
#define ELBOW_CH    2
#define WRIST_CH     3
#define GRIPPER_CH  4

//LIMITS
// Base
#define BASE_MIN 30
#define BASE_MAX 150

// Shoulder
#define SHOULDER_MIN 60
#define SHOULDER_MAX 120

// Elbow
#define ELBOW_MIN 45
#define ELBOW_MAX 135

// Wrist
#define WRIST_MIN 45
#define WRIST_MAX 135

// Gripper
#define GRIPPER_MIN 0
#define GRIPPER_MAX 90

//CURRENT POSITIONS
int current_base = 0;
int current_shoulder = 90;
int current_elbow = 90;
int current_wrist = 0;
int current_gripper = 90;

//TARGET POSITIONS
int target_base = 0;
int target_shoulder = 90;
int target_elbow = 90;
int target_wrist = 0;
int target_gripper = 90;

unsigned long previous_move = 0;

//SERVO FUNCTION
void move_servo(int channel, int angle) {
  angle = constrain(angle, 0, 180);
  int pulse = map(angle, 0, 180, SERVO_MIN, SERVO_MAX);
  pwm.setPWM(channel, 0, pulse);
}

//SET TARGETS
void set_targets(
  int base,
  int shoulder,
  int elbow,
  int wrist,
  int gripper
) {

  target_base = constrain(base, BASE_MIN, BASE_MAX);

  target_shoulder = constrain(
    shoulder, SHOULDER_MIN, SHOULDER_MAX
  );

  target_elbow = constrain(
    elbow, ELBOW_MIN, ELBOW_MAX
  );

  target_wrist = constrain(
    wrist, WRIST_MIN, WRIST_MAX
  );

  target_gripper = constrain(
    gripper, GRIPPER_MIN, GRIPPER_MAX
  );
}

//SMOOTH MOVEMENT
void update_servo(int &current, int target, int channel) {
  if (current < target) {
    current = min(current + MOVE_STEP, target);
  }
  else if (current > target) {
    current = max(current - MOVE_STEP, target);
  }

  move_servo(channel, current);
}

void setup() {
  Serial.begin(115200);

  Serial.setTimeout(50);

  Wire.begin(21, 22);

  pwm.begin();
  pwm.setPWMFreq(50);

  // Initial positions
  move_servo(BASE_CH, current_base);
  move_servo(SHOULDER_CH, current_shoulder);
  move_servo(ELBOW_CH, current_elbow);
  move_servo(WRIST_CH, current_wrist);
  move_servo(GRIPPER_CH, current_gripper);

  Serial.println("ARM_READY");
}

void loop() {
  // Receive serial command:
  // base,shoulder,elbow,wrist,gripper
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');

    int base, shoulder, elbow, wrist, gripper;

    if (sscanf(
      data.c_str(),
      "%d,%d,%d,%d,%d",
      &base,
      &shoulder,
      &elbow,
      &wrist,
      &gripper
    ) == 5) {

      set_targets(
        base,
        shoulder,
        elbow,
        wrist,
        gripper
      );
    }
  }

  // Smooth servo movement
  if (millis() - previous_move >= MOVE_INTERVAL) {
    previous_move = millis();

    update_servo(current_base, target_base, BASE_CH);
    update_servo(current_shoulder, target_shoulder, SHOULDER_CH);
    update_servo(current_elbow, target_elbow, ELBOW_CH);
    update_servo(current_wrist, target_wrist, WRIST_CH);
    update_servo(current_gripper, target_gripper, GRIPPER_CH);
  }
}