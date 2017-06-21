import numpy as np
previous_steer = 0

def forward_is_clean(Rover):
    return np.sum(Rover.terrain[120:130, 130:160]) > 100

def left_is_clean(Rover):
    return np.sum(Rover.terrain[120:130, 120:150]) > 100

def right_is_clean(Rover):
    return np.sum(Rover.terrain[120:130, 160:190]) > 100

def drive_toward_sample(Rover):
    global previous_steer
    # If not stopped yet but still moving keep braking
    if not Rover.fully_stopped:
        if Rover.vel > 0:
            Rover.throttle = 0
            Rover.brake = 3
        else:
            Rover.fully_stopped = True
    elif Rover.near_sample:
        # print("Picking up the sample")
        Rover.pick_up = True
        Rover.mode = 'forward'
        Rover.detected = False
        Rover.brake = 0
        Rover.steer = 0
        Rover.fully_stopped = False
    else:
        # print("Moving towards sample")
        sample_x = Rover.measured_samples_pos[0]
        sample_y = Rover.measured_samples_pos[1]
        angles = np.arctan2(sample_y, sample_x)
        Rover.steer = np.clip(np.mean(angles * 180/np.pi), -15, 15)
        Rover.brake = 0
        if abs(Rover.steer) - previous_steer > 0:
            Rover.throttle = 0
        else:
            Rover.throttle = 0.1
        previous_steer = Rover.steer



def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    left_clean = left_is_clean(Rover)
    right_clean = right_is_clean(Rover)
    forward_clean = forward_is_clean(Rover)

    print("left_clean", np.sum(Rover.terrain[120:130, 120:150]),\
         "right_clean", np.sum(Rover.terrain[120:130, 160:190]), \
         "forward_clean", np.sum(Rover.terrain[120:130, 130:160]))
    if Rover.nav_angles is not None:
        if Rover.detected:
            Rover.mode = 'pickup'
        # Check for Rover.mode status
        if Rover.mode == 'forward':
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:
                # If mode is forward, navigable terrain looks good
                # and velocity is below max, then throttle
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
                # Set steering to average angle clipped to the range +/- 15
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)

                if not (left_clean or right_clean or forward_clean):
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'
                else:
                    if Rover.steer < -10:
                        if not left_clean: Rover.steer = -10
                    elif Rover.steer > 10:
                        if not right_clean: Rover.steer = 10

            # If there's a lack of navigable terrain pixels or found a rocket then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'

        elif Rover.mode == 'pickup':
            drive_toward_sample(Rover)
        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                Rover.throttle = 0
                # Release the brake to allow turning
                Rover.brake = 0
                # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                if len(Rover.nav_angles) >= Rover.go_forward:
                    if left_clean:
                        Rover.steer = -10 # Could be more clever here about which way to turn
                        Rover.mode = 'forward'
                    elif right_clean:
                        Rover.steer = 10
                        Rover.mode = 'forward'
                else:
                    Rover.steer = -20
                # # Now we're stopped and we have vision data to see if there's a path forward
                # if len(Rover.nav_angles) < Rover.go_forward:
                #     Rover.throttle = 0
                #     # Release the brake to allow turning
                #     Rover.brake = 0
                #     # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                #     if left_clean:
                #         Rover.steer = -10 # Could be more clever here about which way to turn

                #     elif right_clean:
                #         Rover.steer = 10

                #     else:
                #         Rover.steer = -20

                # # If we're stopped but see sufficient navigable terrain in front then go!
                # if len(Rover.nav_angles) >= Rover.go_forward:
                #     # Set throttle back to stored value
                #     Rover.throttle = Rover.throttle_set
                #     # Release the brake
                #     Rover.brake = 0
                #     # Set steer to mean angle
                #     Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                #     Rover.mode = 'forward'
    # Just to make the rover do something
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0

    return Rover

