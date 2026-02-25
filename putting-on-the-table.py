def raise_and_release_object(self, table_height_cm):
    """
    Pepper raises right hand to (table_height + 40cm),
    says sentence,
    releases object,
    and returns to neutral.
    Fully safe for NAOqi + Python 2.7.
    """

    import time

    # -------------------------
    # Compute Target Height
    # -------------------------
    target_height = table_height_cm + 40.0

    if target_height < 95.0:
        target_height = 95.0
    if target_height > 135.0:
        target_height = 135.0

    shoulder_pitch = 1.45 - ((target_height - 90.0) * (0.7 / 30.0))

    if shoulder_pitch < 0.5:
        shoulder_pitch = 0.5
    if shoulder_pitch > 1.5:
        shoulder_pitch = 1.5

    # -------------------------
    # Prepare Robot
    # -------------------------
    self.motion_service.wakeUp()
    self.posture_service.goToPosture("StandInit", 0.5)
    time.sleep(1.0)

    # -------------------------
    # 1️⃣ Close Hand (joint control only)
    # -------------------------
    self.motion_service.angleInterpolation(
        ["RHand"],
        [[0.0]],          # 0 = closed
        [[1.0]],
        True
    )

    # -------------------------
    # 2️⃣ Raise Arm Smoothly
    # -------------------------
    names = [
        "HeadPitch", "HeadYaw",
        "RShoulderPitch", "RShoulderRoll",
        "RElbowYaw", "RElbowRoll"
    ]

    angleLists = [
        [0.15],               # HeadPitch (look slightly at hand)
        [-0.1],               # HeadYaw
        [shoulder_pitch],     # ShoulderPitch (height control)
        [-0.15],              # ShoulderRoll
        [1.2],                # ElbowYaw
        [1.1]                 # ElbowRoll
    ]

    timeLists = [
        [2.5],
        [2.5],
        [2.5],
        [2.5],
        [2.5],
        [2.5]
    ]

    self.motion_service.angleInterpolation(
        names,
        angleLists,
        timeLists,
        True
    )

    # -------------------------
    # 3️⃣ Rotate Wrist (Palm Down)
    # -------------------------
    self.motion_service.angleInterpolation(
        ["RWristYaw"],
        [[-1.3]],
        [[1.5]],
        True
    )

    time.sleep(0.3)

    # -------------------------
    # 4️⃣ Speak (SAFE – TextToSpeech only)
    # -------------------------
    self.tts.say("Here is what you asked to bring")

    # -------------------------
    # 5️⃣ Open Hand (Release)
    # -------------------------
    self.motion_service.angleInterpolation(
        ["RHand"],
        [[1.0]],          # 1 = open
        [[1.0]],
        True
    )

    time.sleep(0.8)

    # -------------------------
    # 6️⃣ Small Human Micro Lift
    # -------------------------
    self.motion_service.angleInterpolation(
        ["RShoulderPitch"],
        [[shoulder_pitch + 0.05]],
        [[1.0]],
        True
    )

    # Close hand again
    self.motion_service.angleInterpolation(
        ["RHand"],
        [[0.0]],
        [[1.0]],
        True
    )

    # -------------------------
    # 7️⃣ Return to Neutral
    # -------------------------
    names_return = [
        "HeadPitch", "HeadYaw",
        "RWristYaw",
        "RShoulderPitch",
        "RShoulderRoll",
        "RElbowRoll"
    ]

    angleLists_return = [
        [0.0],
        [0.0],
        [0.0],
        [1.45],
        [-0.05],
        [1.0]
    ]

    timeLists_return = [
        [2.5],
        [2.5],
        [2.5],
        [2.5],
        [2.5],
        [2.5]
    ]

    self.motion_service.angleInterpolation(
        names_return,
        angleLists_return,
        timeLists_return,
        True
    )

    time.sleep(1.0)
