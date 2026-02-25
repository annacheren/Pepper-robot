def raise_and_release_object(self, table_height_cm):
    """
    Safe NAOqi version.
    Raises hand 40cm above table.
    Says sentence at release moment.
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
    # Close Hand (via joint)
    # -------------------------
    self.motion_service.angleInterpolation(
        ["RHand"],
        [[0.0]],
        [[1.0]],
        True
    )

    # -------------------------
    # Raise Arm Smoothly
    # -------------------------
    names = [
        "HeadPitch", "HeadYaw",
        "RShoulderPitch", "RShoulderRoll",
        "RElbowYaw", "RElbowRoll"
    ]

    angleLists = [
        [0.15],
        [-0.1],
        [shoulder_pitch],
        [-0.15],
        [1.2],
        [1.1]
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
        names, angleLists, timeLists, True
    )

    # -------------------------
    # Rotate Wrist (Palm Down)
    # -------------------------
    self.motion_service.angleInterpolation(
        ["RWristYaw"],
        [[-1.3]],
        [[1.5]],
        True
    )

    time.sleep(0.3)

    # -------------------------
    # Speech BEFORE release
    # -------------------------
    self.tts_service.say("Here is what you asked to bring")
    time.sleep(0.3)

    # -------------------------
    # Open Hand (Release)
    # -------------------------
    self.motion_service.angleInterpolation(
        ["RHand"],
        [[1.0]],
        [[1.0]],
        True
    )

    time.sleep(0.8)

    # -------------------------
    # Micro Lift
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
    # Return to Neutral
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
        names_return, angleLists_return, timeLists_return, True
    )

    time.sleep(1.0)
