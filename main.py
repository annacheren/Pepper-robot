# -*- coding: utf-8 -*-
from pepper.robot import Pepper
from pepper_functions import point_table_sequence

if __name__ == "__main__":
    # Press Pepper's chest button once and he will tell you his IP address
    ip_address = "192.168.0.200"
    port = 9559

    robot = Pepper(ip_address, port)
    robot.set_security_distance(0.01)

    # 1. Turn OFF autonomous life
    robot.autonomous_life_off()

    # 2. Disable breathing
    robot.motion_service.setBreathEnabled("Body", False)

    # 3. Disable idle posture
    robot.motion_service.setIdlePostureEnabled("Body", False)

    # 4. Initialize TextToSpeech
    robot.tts = robot.session.service("ALTextToSpeech")

    # 5. Disable awareness
    awareness = robot.session.service("ALBasicAwareness")
    awareness.stopAwareness()
    awareness.setEngagementMode("Unengaged")

    # 6. Run full pointing sequence: left -> middle -> right
    point_table_sequence(
        robot,
        table_center_x=1.0,
        table_center_y=0.0,
        table_width=0.36
    )
