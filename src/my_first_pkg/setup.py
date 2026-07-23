from setuptools import find_packages, setup
import os
from glob import glob
from setuptools import find_packages, setup


package_name = 'my_first_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "urdf"), glob("urdf/*.urdf")),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='leeji',
    maintainer_email='gidwjd2022@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "move_turtle = my_first_pkg.move_turtle:main",
            # "turtle_move_launch = my_first_pkg.launch.turtle_move_launch:main",
            "sub_pose = my_first_pkg.sub_pose:main",
            "camera_viewer = my_first_pkg.camera_viewer:main",
            "color_tracker = my_first_pkg.color_tracker:main",
            "my_publisher = my_first_pkg.my_publisher:main",
            "my_subscriber = my_first_pkg.my_subscriber:main",
            "my_server = my_first_pkg.my_server:main",
            "my_client = my_first_pkg.my_client:main",
            "my_action_server = my_first_pkg.my_action_server:main",
            "my_action_client = my_first_pkg.my_action_client:main",
        ],
    },
)
