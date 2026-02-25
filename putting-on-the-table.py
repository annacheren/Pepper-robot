def place_object_on_table(self):
    """
    Pepper carefully places an object on a table (~80cm height).
    Starts from StandInit and performs smooth, natural motion.
    """

    # 1️⃣ Ensure stable neutral posture
    self.posture_service.goToPosture("StandInit", 0.5)
    time.sleep(1.0)

    # 2️⃣ Look slightly down at the table
    self.move_joint_by_angle(["HeadPitch"], [0.2], 0.1)
    time.sleep(0.5)

    # 3️⃣ Reach forward with object
    self.move_joint_by_angle(
        ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"],
        [1.15, -0.1, 1.2, 1.35, -0.2],
        0.12
    )
    time.sleep(1.2)

    # 4️⃣ Lower gently toward table surface
    self.move_joint_by_angle(
        ["RShoulderPitch", "RElbowRoll"],
        [1.30, 1.50],
        0.08
    )
    time.sleep(1.0)

    # 5️⃣ Small intentional pause before release (adds realism)
    time.sleep(0.5)

    # 6️⃣ Open hand to release object
    self.hand("right", True)
    time.sleep(0.8)

    # 7️⃣ Slight upward micro-adjustment after release (natural human behavior)
    self.move_joint_by_angle(
        ["RShoulderPitch"],
        [1.25],
        0.1
    )
    time.sleep(0.5)

    # 8️⃣ Retract arm smoothly to relaxed position
    self.move_joint_by_angle(
        ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw"],
        [1.45, -0.05, 1.0, 0.0],
        0.18
    )
    time.sleep(1.0)

    # 9️⃣ Return head to neutral
    self.move_joint_by_angle(["HeadPitch"], [0.0], 0.1)
