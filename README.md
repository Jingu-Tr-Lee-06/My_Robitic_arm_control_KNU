---
July 23, 2026

Today was another exhausting day dealing with TurtleBots and robotic arms. Starting from the morning, the Gazebo simulator drove me crazy as the play/pause button flashed continuously at light speed. It turned out that the inertia value specified in the base_link caused the physics engine to blow up. With my brain barely functioning, I decided to temporarily set aside the simulator and focus back on clean code.

I completely rewrote the files and successfully built an OpenCV-based color tracking node (color_tracker.py) without any errors. Seeing it initialize cleanly gave me a huge sense of relief.

Riding that momentum, I dove into the core ROS 2 communication architecture:

Topics: Created Publisher and Subscriber nodes for asynchronous streaming communication (/my_message), seeing counts tick smoothly every 0.5 seconds.

Services: Implemented a synchronous 1:1 request/response server and client using AddTwoInts.

Actions: Mastered asynchronous long-running tasks with feedback and result handling using the Fibonacci action interface.

Finally, to avoid managing multiple terminals, I wrote a Launch file (my_first.launch.py). Of course, a minor mismatch with the .launch.py extension threw a path error initially, but once corrected and rebuilt, launching both publisher and subscriber with a single command worked like magic.

I was about to apply namespaces to handle multiple robots, but my brain reached its absolute limit. I'm wrapping up for today to get some proper rest. Despite all the hurdles, writing and running topics, services, actions, and launch files with my own hands made it a truly rewarding day. Ready to tackle the rest tomorrow!

Author: Jingu Tr.Lee (KNU)
---