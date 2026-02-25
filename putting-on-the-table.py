def raise_and_release_object(self, table_height_cm):
    """
    Raises right hand to (table_height_cm + 40cm),
    rotates palm downward, releases object,
    then returns smoothly to neutral.

    Uses angleInterpolation for smooth biomechanics.
    """

    import math
    import time

    # -------------------------
    # 1️⃣ Compute Target Height
    # -------------------------
    target_height = table_height_cm + 40.0

    # Clamp reasonable human-like range
    target_height = max(95.0, min(target_height, 135.0))

    # Linear mapping to ShoulderPitch
    # 90cm → 1.45
    # 120cm → 0.75
    shoulder_pitch = 1.45 - ((target_height - 90.0) * (0.7 / 30.0))

    # Safety clamp
    shoulder_pitch = max(0.5, min(1.5, shoulder_pitch))

    # -------------------------
    # 2️⃣ Prepare Robot
    # -------------------------
    self.motion_service.wakeUp()
    self.posture_service.goToPosture("StandInit", 0.5)
    time.sleep(1.0)

    # Close hand first
    self.hand("right", False)
    time.sleep(0.5)

    # -------------------------
    # 3️⃣ Smooth Raise Motion
    # -------------------------

    names = [
        "HeadPitch", "HeadYaw",
        "RShoulderPitch", "RShoulderRoll",
        "RElbowYaw", "RElbowRoll"
    ]

    angleLists = [
        [0.0, 0.15],                 # HeadPitch (look at hand)
        [0.0, -0.1],                 # HeadYaw
        [1.45, shoulder_pitch],      # Shoulder lift
        [-0.05, -0.15],              # ShoulderRoll
        [1.2, 1.2],                  # ElbowYaw stable
        [1.0, 1.1]                   # ElbowRoll slight adjust
    ]

    timeLists = [
        [0.0, 2.0],
        [0.0, 2.0],
        [0.0, 2.0],
        [0.0, 2.0],
        [0.0, 2.0],
        [0.0, 2.0]
    ]

    self.motion_service.angleInterpolation(
        names, angleLists, timeLists, True
    )

    # -------------------------
    # 4️⃣ Rotate Wrist (Palm Down)
    # -------------------------

    self.motion_service.angleInterpolation(
        ["RWristYaw"],
        [[0.0, -1.3]],
        [[0.0, 1.2]],
        True
    )

    time.sleep(0.5)

    # -------------------------
    # 5️⃣ Release Object
    # -------------------------
    self.hand("right", True)
    time.sleep(0.8)

    # -------------------------
    # 6️⃣ Micro Human Adjustment
    # -------------------------
    self.motion_service.angleInterpolation(
        ["RShoulderPitch"],
        [[shoulder_pitch, shoulder_pitch + 0.05]],
        [[0.0, 0.6]],
        True
    )

    # Close hand again
    self.hand("right", False)
    time.sleep(0.5)

    # -------------------------
    # 7️⃣ Smooth Return to Neutral
    # -------------------------

    names_return = [
        "HeadPitch", "HeadYaw",
        "RWristYaw",
        "RShoulderPitch",
        "RShoulderRoll",
        "RElbowRoll"
    ]

    angleLists_return = [
        [0.15, 0.0],
        [-0.1, 0.0],
        [-1.3, 0.0],
        [shoulder_pitch + 0.05, 1.45],
        [-0.15, -0.05],
        [1.1, 1.0]
    ]

    timeLists_return = [
        [0.0, 2.0],
        [0.0, 2.0],
        [0.0, 2.0],
        [0.0, 2.0],
        [0.0, 2.0],
        [0.0, 2.0]
    ]

    self.motion_service.angleInterpolation(
        names_return, angleLists_return, timeLists_return, True
    )
