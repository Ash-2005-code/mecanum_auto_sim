cmake_minimum_required(VERSION 3.5)
project(nexus_4wd_mecanum_description)

find_package(ament_cmake REQUIRED)

# Install everything inside these directories
install(DIRECTORY
  launch
  meshes
  urdf
  worlds
  config
  DESTINATION share/${PROJECT_NAME}
)

# Install the RViz config
install(FILES
  urdf.rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
