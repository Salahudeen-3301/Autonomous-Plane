# Autonomous-Plane
After a mountain rescue I experiences where I got lost from my hiking group, and eventually ran out of food and water, I thought having an autonomous plane that could locate lost hikers and deliver resources like food, and water, while communicating their location to rescue services could be a really cool project.

The resulting project is a culmination of 3 categories of work:
1. Developing and researching an object detection model and program optimized for human detection in search and rescue missions. This is the link to the research paper I'm writing about this: https://salahudeen.short.gy/evPQSI.
2. Creating the body of the plane from an online tutorial.
3. Designing the hardware and logical framework. I'm going to use my current Raspberry Pi for the processing.

The resulting project should create: An autonomous plane that "loiters" while following a pre-planned path until it detects a human. Once it detects a human, it tracks them, and delivers a small carepackage with water or a first aid kit. It can then send the co-ordinates back to the user.

[RC Plane Parts - Sheet1 (1).csv](https://github.com/user-attachments/files/24149360/RC.Plane.Parts.-.Sheet1.1.csv)
PARTS:,Owned,COST,RUNNING COST (dirhams with tax),LINK,Number of Units,Description
NAVIO2 ,No,dh800.00,dh928.00,link,1,Raspberry Pi HAT with necessary sensors + I/O protocols
Raspberry Pi 4,Yes,dh284.00,dh299.00,link,1,Small computer used for electrical engineering/CS progjects
MOTOR: DXW 3536 1200kv,Yes,dh174.00,dh174.00,link,1,Plane's motor
9G Servos x 8,Yes,dh65.00,dh65.00,link,1,Small motor that can turn to a specific angle depending on voltage. This is used to steer the plane by moving the flaps
50A ESC,Yes,dh94.00,dh94.00,link,1,Electronic speed controller. Controls the speed of the motor by varying current
CONTROLLER + RECIEVER,Yes,dh612.00,dh612.00,link,1,Controller sends radio signals to the reciever in order to control the plane by changing the current given to the motor and servos
106 propellor x 2,Yes,dh17.00,dh17.00,link,1,Propellor for the motor 
4S Lipo,Yes,dh224.00,dh224.00,link,1,A Lithium polymer battery used to power the plane. It is useful due it's versatility and being lighte-weight; this is essential for a plane.
Total,,,"dh2,413.00",,,
