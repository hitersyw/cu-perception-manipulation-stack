#!/usr/bin/env python

import rospy
import numpy as np
import tf
import action_database
import smach
from pap.jaco import JacoGripper

def main():
    rospy.init_node("test")
    jg = JacoGripper()
    jg.set_position([50.0,50.0,0.0])
    sm = smach.StateMachine(outcomes=['Done','hi'])
    with sm:

        smach.StateMachine.add('CalibrateFingers1',
                                action_database.CalibrateFingers(pos=[50.0,50.0,0.0]),
                                transitions={'calibrated':'GotoObject1',
                                            'not_calibrated':'CalibrateFingers1'})

        smach.StateMachine.add('GotoObject1',
                                action_database.GotoObject('/cube_0_grasp'),
                                transitions={'there':'GraspObject1',
                                            'no_tf_found':'GotoObject1'})

        smach.StateMachine.add('SearchObject1',
                                action_database.SearchObject([0,1]),
                                transitions={'found':'GraspObject1',
                                            'not_found': 'GraspObject1'})

        smach.StateMachine.add('GraspObject1',
                        action_database.GraspObject([50.0,50.0,0.0],third_finger=False),
                        transitions={'grasped':'GotoObject2',
                                    'not_grasped': 'CalibrateFingers2'})

        smach.StateMachine.add('GotoObject2',
                                action_database.GotoObject('/cube_1_grasp'),
                                transitions={'there':'CalibrateFingers3',
                                            'no_tf_found':'GotoObject2'})

        smach.StateMachine.add('CalibrateFingers2',
                                action_database.CalibrateFingers(pos=[50.0,50.0,0.0]),
                                transitions={'calibrated':'SearchObject1',
                                            'not_calibrated':'CalibrateFingers2'})

        smach.StateMachine.add('CalibrateFingers3',
                                action_database.CalibrateFingers(),
                                transitions={'calibrated':'SearchObject2',
                                            'not_calibrated':'CalibrateFingers3'})


        smach.StateMachine.add('SearchObject2',
                                action_database.SearchObject([0,1],search='down_z'),
                                transitions={'found':'Done',
                                            'not_found': 'Done'})


    outcome = sm.execute()

    jg.set_position([50.0,50.0,0.0])


if __name__ == '__main__':
    main()
