cmake_minimum_required(VERSION 3.10)

project(workspace)

include(${CMAKE_BINARY_DIR}/conanworkspace.cmake)

if (MSVC)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /MP")
endif ()

conan_workspace_subdirectories()
