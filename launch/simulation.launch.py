import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command

def generate_launch_description():
    pkg_share = get_package_share_directory('nexus_4wd_mecanum_description')
    
    # Force Gazebo to see your meshes
    gazebo_models_path = os.path.join(pkg_share, '..')
    set_gazebo_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=gazebo_models_path
    )

    xacro_file = os.path.join(pkg_share, 'urdf', 'nexus_4wd_mecanum.xacro')
    world_file = os.path.join(pkg_share, 'worlds', 'enclosed_room.world')

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': Command(['xacro ', xacro_file]),
            'use_sim_time': True
        }]
    )

    # 1. NEW: Joint State Publisher (Fixes the missing wheel TF frames)
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'use_sim_time': True}]
    )

    # Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'
        )]),
        launch_arguments={'world': world_file}.items()
    )

    # Spawn the Nexus bot
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'nexus_bot', '-topic', 'robot_description', '-z', '0.15'],
        output='screen'
    )

    # 2. NEW: Auto-launch RViz (Ensures it can find the .STL files)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        set_gazebo_model_path,
        robot_state_publisher,
        joint_state_publisher,
        gazebo,
        spawn_entity,
        rviz_node
    ])
