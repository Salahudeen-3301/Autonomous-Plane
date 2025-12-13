# Autonomous-Plane
After a mountain rescue I experiences where I got lost from my hiking group, and eventually ran out of food and water, I thought having an autonomous plane that could locate lost hikers and deliver resources like food, and water, while communicating their location to rescue services could be a really cool project.

The resulting project is a culmination of 3 categories of work:
1. Developing and researching an object detection model and program optimized for human detection in search and rescue missions. This is the link to the research paper I'm writing about this: https://salahudeen.short.gy/evPQSI.
2. Creating the body of the plane from an online tutorial.
3. Designing the hardware and logical framework. I'm going to use my current Raspberry Pi for the processing.

The resulting project should create: An autonomous plane that "loiters" while following a pre-planned path until it detects a human. Once it detects a human, it tracks them, and delivers a small carepackage with water or a first aid kit. It can then send the co-ordinates back to the user.
