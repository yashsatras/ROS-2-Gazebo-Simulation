#!/usr/bin/env python3

import math
import time
import pygame

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped


class OmniDriveTeleop(Node):

    def __init__(self):
        super().__init__('omni_drive_teleop')

        # =========================================================
        # PUBLISHER
        # =========================================================

        self.publisher = self.create_publisher(
            TwistStamped,
            '/omni_drive_controller/cmd_vel',
            10
        )

        # =========================================================
        # SPEED
        # =========================================================

        self.linear_speed = 1.0
        self.angular_speed = 1.0

        # =========================================================
        # ROBOT DIRECTION
        #
        # +X = FRONT
        # +Y = LEFT
        #
        # Wheel positions:
        #
        # Link 8 = Front Left
        # Link 7 = Front Right
        # Link 5 = Rear Left
        # Link 6 = Rear Right
        #
        # =========================================================

        self.forward_sign = 1.0
        self.strafe_sign = 1.0
        self.rotate_sign = 1.0

        # =========================================================
        # CURRENT VELOCITY
        # =========================================================

        self.vx = 0.0
        self.vy = 0.0
        self.wz = 0.0

        # =========================================================
        # KEY STATES
        #
        # True only while key is physically held down.
        # =========================================================

        self.forward = False
        self.backward = False

        self.left = False
        self.right = False

        self.rotate_left = False
        self.rotate_right = False

        # =========================================================
        # TIMER
        #
        # Publish at 50 Hz
        # =========================================================

        self.timer = self.create_timer(
            0.02,
            self.publish_velocity
        )

    # =============================================================
    # CALCULATE VELOCITY
    # =============================================================

    def calculate_velocity(self):

        vx = 0.0
        vy = 0.0
        wz = 0.0

        # =========================================================
        # FORWARD / BACKWARD
        # =========================================================

        if self.forward:
            vx += self.forward_sign * self.linear_speed

        if self.backward:
            vx -= self.forward_sign * self.linear_speed

        # =========================================================
        # LEFT / RIGHT
        # =========================================================

        if self.left:
            vy += self.strafe_sign * self.linear_speed

        if self.right:
            vy -= self.strafe_sign * self.linear_speed

        # =========================================================
        # ROTATION
        # =========================================================

        if self.rotate_left:
            wz += self.rotate_sign * self.angular_speed

        if self.rotate_right:
            wz -= self.rotate_sign * self.angular_speed

        # =========================================================
        # DIAGONAL NORMALIZATION
        # =========================================================

        magnitude = math.sqrt(
            vx * vx +
            vy * vy
        )

        if magnitude > self.linear_speed:

            scale = self.linear_speed / magnitude

            vx *= scale
            vy *= scale

        # =========================================================
        # STORE
        # =========================================================

        self.vx = float(vx)
        self.vy = float(vy)
        self.wz = float(wz)

    # =============================================================
    # PUBLISH VELOCITY
    # =============================================================

    def publish_velocity(self):

        self.calculate_velocity()

        msg = TwistStamped()

        # =========================================================
        # HEADER
        # =========================================================

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'

        # =========================================================
        # LINEAR
        # =========================================================

        msg.twist.linear.x = float(self.vx)
        msg.twist.linear.y = float(self.vy)
        msg.twist.linear.z = 0.0

        # =========================================================
        # ANGULAR
        # =========================================================

        msg.twist.angular.x = 0.0
        msg.twist.angular.y = 0.0
        msg.twist.angular.z = float(self.wz)

        # =========================================================
        # PUBLISH
        # =========================================================

        self.publisher.publish(msg)

    # =============================================================
    # STOP
    # =============================================================

    def stop(self):

        self.forward = False
        self.backward = False

        self.left = False
        self.right = False

        self.rotate_left = False
        self.rotate_right = False

        self.vx = 0.0
        self.vy = 0.0
        self.wz = 0.0


# =================================================================
# MAIN
# =================================================================

def main():

    rclpy.init()

    node = OmniDriveTeleop()

    # =============================================================
    # INITIALIZE PYGAME
    # =============================================================

    pygame.init()

    screen = pygame.display.set_mode((600, 400))

    pygame.display.set_caption(
        "ROS 2 Omni Drive Teleop"
    )

    clock = pygame.time.Clock()

    # =============================================================
    # FONT
    # =============================================================

    font_large = pygame.font.Font(None, 42)
    font_small = pygame.font.Font(None, 28)

    running = True

    print()
    print("================================================")
    print("             OMNI DRIVE TELEOP")
    print("================================================")
    print()
    print("HOLD W  = Forward")
    print("HOLD S  = Backward")
    print()
    print("HOLD A  = Strafe Left")
    print("HOLD D  = Strafe Right")
    print()
    print("HOLD Q  = Rotate Left")
    print("HOLD E  = Rotate Right")
    print()
    print("RELEASE KEY = STOP THAT MOTION")
    print()
    print("ESC = Exit")
    print()
    print("================================================")
    print()
    print("Wheel layout:")
    print()
    print("       FRONT")
    print()
    print(" Link 8       Link 7")
    print(" Front L      Front R")
    print()
    print(" Link 5       Link 6")
    print(" Rear L       Rear R")
    print()
    print("       REAR")
    print()
    print("================================================")
    print()

    try:

        while running:

            # =====================================================
            # PROCESS EVENTS
            # =====================================================

            for event in pygame.event.get():

                # -------------------------------------------------
                # CLOSE WINDOW
                # -------------------------------------------------

                if event.type == pygame.QUIT:

                    running = False

                # -------------------------------------------------
                # KEY DOWN
                # -------------------------------------------------

                elif event.type == pygame.KEYDOWN:

                    # ESC
                    if event.key == pygame.K_ESCAPE:

                        running = False

                    # W
                    elif event.key == pygame.K_w:

                        node.forward = True
                        node.backward = False

                    # S
                    elif event.key == pygame.K_s:

                        node.backward = True
                        node.forward = False

                    # A
                    elif event.key == pygame.K_a:

                        node.left = True
                        node.right = False

                    # D
                    elif event.key == pygame.K_d:

                        node.right = True
                        node.left = False

                    # Q
                    elif event.key == pygame.K_q:

                        node.rotate_left = True
                        node.rotate_right = False

                    # E
                    elif event.key == pygame.K_e:

                        node.rotate_right = True
                        node.rotate_left = False

                # -------------------------------------------------
                # KEY UP
                # -------------------------------------------------

                elif event.type == pygame.KEYUP:

                    # W released
                    if event.key == pygame.K_w:

                        node.forward = False

                    # S released
                    elif event.key == pygame.K_s:

                        node.backward = False

                    # A released
                    elif event.key == pygame.K_a:

                        node.left = False

                    # D released
                    elif event.key == pygame.K_d:

                        node.right = False

                    # Q released
                    elif event.key == pygame.K_q:

                        node.rotate_left = False

                    # E released
                    elif event.key == pygame.K_e:

                        node.rotate_right = False

            # =====================================================
            # ROS CALLBACKS
            # =====================================================

            rclpy.spin_once(
                node,
                timeout_sec=0.0
            )

            # =====================================================
            # DISPLAY
            # =====================================================

            screen.fill((30, 30, 30))

            title = font_large.render(
                "OMNI DRIVE TELEOP",
                True,
                (255, 255, 255)
            )

            screen.blit(
                title,
                (150, 30)
            )

            # -----------------------------------------------------
            # CURRENT COMMAND
            # -----------------------------------------------------

            commands = []

            if node.forward:
                commands.append("FORWARD")

            if node.backward:
                commands.append("BACKWARD")

            if node.left:
                commands.append("LEFT")

            if node.right:
                commands.append("RIGHT")

            if node.rotate_left:
                commands.append("ROTATE LEFT")

            if node.rotate_right:
                commands.append("ROTATE RIGHT")

            if not commands:
                commands.append("STOPPED")

            y = 100

            for command in commands:

                text = font_large.render(
                    command,
                    True,
                    (255, 255, 255)
                )

                screen.blit(
                    text,
                    (210, y)
                )

                y += 50

            # -----------------------------------------------------
            # VELOCITY DISPLAY
            # -----------------------------------------------------

            velocity_text = font_small.render(
                f"VX: {node.vx:.2f}   "
                f"VY: {node.vy:.2f}   "
                f"WZ: {node.wz:.2f}",
                True,
                (255, 255, 255)
            )

            screen.blit(
                velocity_text,
                (120, 300)
            )

            help_text = font_small.render(
                "Hold W/A/S/D/Q/E   |   ESC = Exit",
                True,
                (255, 255, 255)
            )

            screen.blit(
                help_text,
                (130, 350)
            )

            pygame.display.flip()

            # =====================================================
            # 50 Hz
            # =====================================================

            clock.tick(50)

    except KeyboardInterrupt:

        pass

    finally:

        # =========================================================
        # STOP ROBOT
        # =========================================================

        node.stop()

        # Send zero several times
        for _ in range(10):

            node.publish_velocity()

            rclpy.spin_once(
                node,
                timeout_sec=0.01
            )

            time.sleep(0.02)

        pygame.quit()

        node.destroy_node()

        rclpy.shutdown()

        print()
        print("Robot stopped.")
        print("Teleop exited.")


# =================================================================
# ENTRY POINT
# =================================================================

if __name__ == '__main__':
    main()