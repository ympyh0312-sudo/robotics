from glob import glob
from setuptools import find_packages, setup

package_name = 'my_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/config', ['config/params.yaml']),
        ('share/' + package_name + '/launch', glob('launch/*.py') + glob('launch/*.xml')),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yanghee',
    maintainer_email='ympyh0312@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "my_first_node = my_py_pkg.my_first_node:main",
            "news_robot_station = my_py_pkg.news_robot_station:main",
            "smartphone = my_py_pkg.smartphonenode:main",
            "number = my_py_pkg.number:main",
            "number_count = my_py_pkg.number_count:main",
            "addtwointserver = my_py_pkg.addtwointsserver:main",
            "addtwointclient = my_py_pkg.addtwointclient:main",
            "mynode = my_py_pkg.mynode:main",
            "led_panel_server = my_py_pkg.led_panel_server:main",
            "led_panel_client = my_py_pkg.led_panel_client:main",
            "static_frame_publisher = my_py_pkg.static_frame_publisher:main",
            "dynamic_frame_publisher = my_py_pkg.dynamic_frame_publisher:main",
            "tf_listener_node = my_py_pkg.tf_listener_node:main",
            "three_frame_publisher = my_py_pkg.three_frame_publisher:main",
            "three_tf_listener_node = my_py_pkg.three_tf_listener_node:main",
            "robot_state_publisher_node = my_py_pkg.robot_state_publisher_node:main",
        ],
    },
)