\* Problem: SPS *\

Minimize
 totalLoadGap: + parkingSpaceLoad(p1) + parkingSpaceLoad(p2)
 + parkingSpaceLoad(p3) + parkingSpaceLoad(p4) + parkingSpaceLoad(p5)
 - 5 minLoad

Subject To
 AssignmentConstraint(Car1): + isCarAssigned(Car1,p1)
 + isCarAssigned(Car1,p2) + isCarAssigned(Car1,p3)
 + isCarAssigned(Car1,p4) + isCarAssigned(Car1,p5) = 1
 AssignmentConstraint(Car2): + isCarAssigned(Car2,p1)
 + isCarAssigned(Car2,p2) + isCarAssigned(Car2,p3)
 + isCarAssigned(Car2,p4) + isCarAssigned(Car2,p5) = 1
 AssignmentConstraint(Car3): + isCarAssigned(Car3,p1)
 + isCarAssigned(Car3,p2) + isCarAssigned(Car3,p3)
 + isCarAssigned(Car3,p4) + isCarAssigned(Car3,p5) = 1
 AssignmentConstraint(Car4): + isCarAssigned(Car4,p1)
 + isCarAssigned(Car4,p2) + isCarAssigned(Car4,p3)
 + isCarAssigned(Car4,p4) + isCarAssigned(Car4,p5) = 1
 AssignmentConstraint(Car5): + isCarAssigned(Car5,p1)
 + isCarAssigned(Car5,p2) + isCarAssigned(Car5,p3)
 + isCarAssigned(Car5,p4) + isCarAssigned(Car5,p5) = 1
 CapacityConstraint(p1): + isCarAssigned(Car1,p1)
 + isCarAssigned(Car2,p1) + isCarAssigned(Car3,p1)
 + isCarAssigned(Car4,p1) + isCarAssigned(Car5,p1) <= 10
 CapacityConstraint(p2): + isCarAssigned(Car1,p2)
 + isCarAssigned(Car2,p2) + isCarAssigned(Car3,p2)
 + isCarAssigned(Car4,p2) + isCarAssigned(Car5,p2) <= 10
 CapacityConstraint(p3): + isCarAssigned(Car1,p3)
 + isCarAssigned(Car2,p3) + isCarAssigned(Car3,p3)
 + isCarAssigned(Car4,p3) + isCarAssigned(Car5,p3) <= 10
 CapacityConstraint(p4): + isCarAssigned(Car1,p4)
 + isCarAssigned(Car2,p4) + isCarAssigned(Car3,p4)
 + isCarAssigned(Car4,p4) + isCarAssigned(Car5,p4) <= 10
 CapacityConstraint(p5): + isCarAssigned(Car1,p5)
 + isCarAssigned(Car2,p5) + isCarAssigned(Car3,p5)
 + isCarAssigned(Car4,p5) + isCarAssigned(Car5,p5) <= 10
 minLoadConstraint(p1): + 2 isCarAssigned(Car1,p1)
 + isCarAssigned(Car2,p1) + isCarAssigned(Car3,p1)
 + 3 isCarAssigned(Car4,p1) + 4 isCarAssigned(Car5,p1) - minLoad >= -0
 minLoadConstraint(p2): + 2 isCarAssigned(Car1,p2)
 + isCarAssigned(Car2,p2) + isCarAssigned(Car3,p2)
 + 3 isCarAssigned(Car4,p2) + 4 isCarAssigned(Car5,p2) - minLoad >= -0
 minLoadConstraint(p3): + 2 isCarAssigned(Car1,p3)
 + isCarAssigned(Car2,p3) + isCarAssigned(Car3,p3)
 + 3 isCarAssigned(Car4,p3) + 4 isCarAssigned(Car5,p3) - minLoad >= -0
 minLoadConstraint(p4): + 2 isCarAssigned(Car1,p4)
 + isCarAssigned(Car2,p4) + isCarAssigned(Car3,p4)
 + 3 isCarAssigned(Car4,p4) + 4 isCarAssigned(Car5,p4) - minLoad >= -0
 minLoadConstraint(p5): + 2 isCarAssigned(Car1,p5)
 + isCarAssigned(Car2,p5) + isCarAssigned(Car3,p5)
 + 3 isCarAssigned(Car4,p5) + 4 isCarAssigned(Car5,p5) - minLoad >= -0
 loadConstraint1(p1): - 2 isCarAssigned(Car1,p1)
 - isCarAssigned(Car2,p1) - isCarAssigned(Car3,p1)
 - 3 isCarAssigned(Car4,p1) - 4 isCarAssigned(Car5,p1)
 + parkingSpaceLoad(p1) >= -0
 loadConstraint1(p2): - 2 isCarAssigned(Car1,p2)
 - isCarAssigned(Car2,p2) - isCarAssigned(Car3,p2)
 - 3 isCarAssigned(Car4,p2) - 4 isCarAssigned(Car5,p2)
 + parkingSpaceLoad(p2) >= -0
 loadConstraint1(p3): - 2 isCarAssigned(Car1,p3)
 - isCarAssigned(Car2,p3) - isCarAssigned(Car3,p3)
 - 3 isCarAssigned(Car4,p3) - 4 isCarAssigned(Car5,p3)
 + parkingSpaceLoad(p3) >= -0
 loadConstraint1(p4): - 2 isCarAssigned(Car1,p4)
 - isCarAssigned(Car2,p4) - isCarAssigned(Car3,p4)
 - 3 isCarAssigned(Car4,p4) - 4 isCarAssigned(Car5,p4)
 + parkingSpaceLoad(p4) >= -0
 loadConstraint1(p5): - 2 isCarAssigned(Car1,p5)
 - isCarAssigned(Car2,p5) - isCarAssigned(Car3,p5)
 - 3 isCarAssigned(Car4,p5) - 4 isCarAssigned(Car5,p5)
 + parkingSpaceLoad(p5) >= -0
 loadConstraint2(p1): - 2 isCarAssigned(Car1,p1)
 - isCarAssigned(Car2,p1) - isCarAssigned(Car3,p1)
 - 3 isCarAssigned(Car4,p1) - 4 isCarAssigned(Car5,p1)
 + parkingSpaceLoad(p1) <= -0
 loadConstraint2(p2): - 2 isCarAssigned(Car1,p2)
 - isCarAssigned(Car2,p2) - isCarAssigned(Car3,p2)
 - 3 isCarAssigned(Car4,p2) - 4 isCarAssigned(Car5,p2)
 + parkingSpaceLoad(p2) <= -0
 loadConstraint2(p3): - 2 isCarAssigned(Car1,p3)
 - isCarAssigned(Car2,p3) - isCarAssigned(Car3,p3)
 - 3 isCarAssigned(Car4,p3) - 4 isCarAssigned(Car5,p3)
 + parkingSpaceLoad(p3) <= -0
 loadConstraint2(p4): - 2 isCarAssigned(Car1,p4)
 - isCarAssigned(Car2,p4) - isCarAssigned(Car3,p4)
 - 3 isCarAssigned(Car4,p4) - 4 isCarAssigned(Car5,p4)
 + parkingSpaceLoad(p4) <= -0
 loadConstraint2(p5): - 2 isCarAssigned(Car1,p5)
 - isCarAssigned(Car2,p5) - isCarAssigned(Car3,p5)
 - 3 isCarAssigned(Car4,p5) - 4 isCarAssigned(Car5,p5)
 + parkingSpaceLoad(p5) <= -0

Bounds
 0 <= isCarAssigned(Car1,p1) <= 1
 0 <= isCarAssigned(Car1,p2) <= 1
 0 <= isCarAssigned(Car1,p3) <= 1
 0 <= isCarAssigned(Car1,p4) <= 1
 0 <= isCarAssigned(Car1,p5) <= 1
 0 <= isCarAssigned(Car2,p1) <= 1
 0 <= isCarAssigned(Car2,p2) <= 1
 0 <= isCarAssigned(Car2,p3) <= 1
 0 <= isCarAssigned(Car2,p4) <= 1
 0 <= isCarAssigned(Car2,p5) <= 1
 0 <= isCarAssigned(Car3,p1) <= 1
 0 <= isCarAssigned(Car3,p2) <= 1
 0 <= isCarAssigned(Car3,p3) <= 1
 0 <= isCarAssigned(Car3,p4) <= 1
 0 <= isCarAssigned(Car3,p5) <= 1
 0 <= isCarAssigned(Car4,p1) <= 1
 0 <= isCarAssigned(Car4,p2) <= 1
 0 <= isCarAssigned(Car4,p3) <= 1
 0 <= isCarAssigned(Car4,p4) <= 1
 0 <= isCarAssigned(Car4,p5) <= 1
 0 <= isCarAssigned(Car5,p1) <= 1
 0 <= isCarAssigned(Car5,p2) <= 1
 0 <= isCarAssigned(Car5,p3) <= 1
 0 <= isCarAssigned(Car5,p4) <= 1
 0 <= isCarAssigned(Car5,p5) <= 1
 parkingSpaceLoad(p1) free
 parkingSpaceLoad(p2) free
 parkingSpaceLoad(p3) free
 parkingSpaceLoad(p4) free
 parkingSpaceLoad(p5) free
 minLoad free

Generals
 isCarAssigned(Car1,p1)
 isCarAssigned(Car1,p2)
 isCarAssigned(Car1,p3)
 isCarAssigned(Car1,p4)
 isCarAssigned(Car1,p5)
 isCarAssigned(Car2,p1)
 isCarAssigned(Car2,p2)
 isCarAssigned(Car2,p3)
 isCarAssigned(Car2,p4)
 isCarAssigned(Car2,p5)
 isCarAssigned(Car3,p1)
 isCarAssigned(Car3,p2)
 isCarAssigned(Car3,p3)
 isCarAssigned(Car3,p4)
 isCarAssigned(Car3,p5)
 isCarAssigned(Car4,p1)
 isCarAssigned(Car4,p2)
 isCarAssigned(Car4,p3)
 isCarAssigned(Car4,p4)
 isCarAssigned(Car4,p5)
 isCarAssigned(Car5,p1)
 isCarAssigned(Car5,p2)
 isCarAssigned(Car5,p3)
 isCarAssigned(Car5,p4)
 isCarAssigned(Car5,p5)

End
