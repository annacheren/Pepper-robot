# -*- coding: utf-8 -*-
import math
import time


def _point_direction(robot, target_x, target_y, label):
    """
    Internal helper: points arm toward (target_x, target_y),
    says label, then returns arm and head to neutral.
    """
    motion = robot.motion_service

    # Choose arm based on target side
    # target_y > 0 = robot's left side => use left arm
    effector = "L" if target_y >= 0 else "R"

    # -------------------------------------------------
    # Compute joint angles
    # -------------------------------------------------
    # ShoulderPitch: forward lift
    shoulder_pitch = 0.3

    # ShoulderRoll: lateral spread toward target
    # L arm: positive = away from body (left)
    # R arm: negative = away from body (right)
    if effector == "L":
        shoulder_roll = 0.3 + target_y * 0.5
        shoulder_roll = max(0.0, min(1.3, shoulder_roll))
    else:
        shoulder_roll = -0.3 + target_y * 0.5
        shoulder_roll = max(-1.3, min(0.0, shoulder_roll))

    elbow_yaw  =  1.5 if effector == "R" else -1.5
    elbow_roll =  1.2 if effector == "R" else -1.2
    wrist_yaw  = -1.5 if effector == "R" else  1.5

    # Head: yaw toward target, pitch slightly down
    head_yaw   = math.atan2(target_y, target_x)
    head_pitch = 0.25

    # -------------------------------------------------
    # 1. Raise arm + turn head together
    # -------------------------------------------------
    names = [
        effector + "ShoulderPitch",
        effector + "ShoulderRoll",
        effector + "ElbowYaw",
        effector + "ElbowRoll",
        effector + "WristYaw",
        "HeadYaw",
        "HeadPitch"
    ]

    angles = [
        [shoulder_pitch],
        [shoulder_roll],
        [elbow_yaw],
        [elbow_roll],
        [wrist_yaw],
        [head_yaw],
        [head_pitch]
    ]

    times = [[2.0]] * 7

    motion.angleInterpolation(names, angles, times, True)

    # 2. Open hand to pointing shape (mostly closed = finger point illusion)
    motion.angleInterpolation(
        [effector + "Hand"],
        [[0.3]],
        [[0.8]],
        True
    )

    # 3. Speak
    robot.tts.say(label)

    time.sleep(0.5)

    # -------------------------------------------------
    # 4. Return arm AND head to neutral (StandInit values)
    # -------------------------------------------------
    names_return = [
        effector + "ShoulderPitch",
        effector + "ShoulderRoll",
        effector + "ElbowYaw",
        effector + "ElbowRoll",
        effector + "WristYaw",
        effector + "Hand",
        "HeadYaw",
        "HeadPitch"
    ]

    if effector == "R":
        neutral = [1.45, -0.05,  1.2,  0.4, 0.0, 0.6, 0.0, 0.0]
    else:
        neutral = [1.45,  0.05, -1.2, -0.4, 0.0, 0.6, 0.0, 0.0]

    angles_return = [[v] for v in neutral]
    times_return  = [[2.0]] * len(names_return)

    motion.angleInterpolation(names_return, angles_return, times_return, True)
    time.sleep(0.3)


def point_table_precise(robot,
                        table_center_x,
                        table_center_y,
                        table_width,
                        direction,
                        arm="auto"):
    """
    Points to the specified region of the table and returns arm to neutral.
    direction: "left" | "middle" | "right"
    """
    if direction == "left":
        target_y = table_center_y + table_width / 2.0
        label = "I point left"
    elif direction == "right":
        target_y = table_center_y - table_width / 2.0
        label = "I point right"
    else:  # middle
        target_y = table_center_y
        label = "I point middle"

    _point_direction(robot, table_center_x, target_y, label)


def point_table_sequence(robot,
                         table_center_x,
                         table_center_y,
                         table_width):
    """
    Full demo sequence:
      1. Points left   -> says "I point left"
      2. Points middle -> says "I point middle"
      3. Points right  -> says "I point right"
    Returns arm and head to neutral after each point.
    """
    for direction in ["left", "middle", "right"]:
        point_table_precise(robot,
                            table_center_x=table_center_x,
                            table_center_y=table_center_y,
                            table_width=table_width,
                            direction=direction)
        time.sleep(0.5)
