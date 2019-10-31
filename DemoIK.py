#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  DemoIK.py - York Hack Space May 2014
#  Simple demo of meArm library to walk through some points defined in Cartesian coordinates

import meArm

def main():
    arm = meArm.meArm()
	
    while True:
        arm.openGripper()
        arm.closeGripper()
        arm.openGripper()
        arm.closeGripper()
        arm.openGripper()

        arm.gotoPoint(0, 10, 20)
        arm.gotoPoint(0, 20, 50)
        arm.gotoPoint(0, 50, 70)
        arm.gotoPoint(0, 20, 100)
        arm.gotoPoint(1, 1, 1)
        arm.gotoPoint(50, 50, 100)
        arm.gotoPoint(20, 30, 50)
        arm.gotoPoint(10, 10, 20)

        arm.gotoPoint(0, 10, 20)
        arm.gotoPoint(0, 20, 50)
        arm.gotoPoint(0, 50, 70)
        arm.gotoPoint(0, 20, 100)
        arm.gotoPoint(1, 1, 1)
        arm.gotoPoint(50, 50, 100)
        arm.gotoPoint(20, 30, 50)
        arm.gotoPoint(10, 10, 20)


if __name__ == '__main__':
    main()
