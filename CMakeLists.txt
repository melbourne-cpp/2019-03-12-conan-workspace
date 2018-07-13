cmake_minimum_required(VERSION 3.6)
project(Workspace)
include(ExternalProject)
include(DownloadProject.cmake)

set(CMAKE_DEBUG_POSTFIX "")
set(CMAKE_RELWITHDEBINFO_POSTFIX "")
set(CMAKE_MINSIZEREL_POSTFIX "")
set(CMAKE_STATIC_LIBRARY_PREFIX "")
set(CMAKE_SHARED_LIBRARY_PREFIX "")

if (MSVC)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /MP")
endif ()

# fmt
download_project(
  PROJ fmt
  PREFIX fmt
  URL "https://github.com/fmtlib/fmt/archive/5.1.0.tar.gz"
  URL_MD5 89863cfec1448aec409a2eecf62600a2
  UPDATE_DISCONNECTED 1
)
add_subdirectory(${fmt_SOURCE_DIR} ${fmt_BINARY_DIR})
# (fmt)

download_project(
  PROJ embed-resource
  PREFIX embed-resource
  GIT_REPOSITORY "https://github.com/lawrencem99/embed-resource.git"
  UPDATE_DISCONNECTED 1
)
add_subdirectory(${embed-resource_SOURCE_DIR} ${embed-resource_BINARY_DIR})

# tbb
if (MSVC)
  set(CMAKE_OLD_DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})
  set(CMAKE_DEBUG_POSTFIX _debug)
endif ()

set(TBB_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(TBB_BUILD_STATIC OFF CACHE BOOL "" FORCE)

download_project(
  PROJ tbb
  PREFIX tbb
  URL "https://github.com/lawrencem99/tbb/archive/lm-minimal.tar.gz"
  URL_MD5 9fb1401b3815b59e5d27927a9d0ee65d
  UPDATE_DISCONNECTED 1
)
add_subdirectory(${tbb_SOURCE_DIR} ${tbb_BINARY_DIR})
set(TBB_INCLUDE_DIR ${tbb_SOURCE_DIR}/include)

if (MSVC)
  set(CMAKE_DEBUG_POSTFIX ${CMAKE_OLD_DEBUG_POSTFIX})
endif ()
# (tbb)

# GoogleTest
if (MSVC)
  set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
endif ()

download_project(
  PROJ googletest
  PREFIX googletest
  GIT_REPOSITORY "https://github.com/google/googletest.git"
  GIT_TAG ba96d0b
  UPDATE_DISCONNECTED 1
)
add_subdirectory(${googletest_SOURCE_DIR} ${googletest_BINARY_DIR})
# (GoogleTest)

find_package(Vulkan REQUIRED)

if (UNIX)
  find_package(PkgConfig REQUIRED)
endif()

# Setup CMake to use GTK+, tell the compiler where to look for headers
# and to the linker where to look for libraries
INCLUDE_DIRECTORIES(${GTK3_INCLUDE_DIRS})
LINK_DIRECTORIES(${GTK3_LIBRARY_DIRS})

# Eigen
download_project(
  PROJ EIGEN
  PREFIX eigen
  URL https://github.com/eigenteam/eigen-git-mirror/archive/3.3.4.tar.gz
  URL_MD5 "1896a1f682e6cdcffd91b6e5ba8286a2"
  UPDATE_DISCONNECTED 1
)
# (eigen)

# OpenMesh
download_project(
  PROJ openmesh
  PREFIX openmesh
  URL "https://github.com/lawrencem99/openmesh/archive/lm-minimal.tar.gz"
  URL_MD5 6907271e86f0ff809c8d64e2e1abea4a
  UPDATE_DISCONNECTED 1
)
add_subdirectory(${openmesh_SOURCE_DIR} ${openmesh_BINARY_DIR})
# (OpenMesh)

macro(exe_properties name)
  if (WIN32)
    if (MSVC)
      set(CMAKE_EXE_LINKER_FLAGS
          "${CMAKE_EXE_LINKER_FLAGS} /subsystem:windows /entry:mainCRTStartup")
    elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
      set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mwindows")
    endif ()
  endif ()
endmacro()

macro(tbb_dll_copy name)
  add_custom_command(TARGET ${name} POST_BUILD
                     COMMAND ${CMAKE_COMMAND} -E copy_if_different
                     $<TARGET_FILE_DIR:tbb>/$<TARGET_FILE_NAME:tbb>
                     $<TARGET_FILE_DIR:${name}>)
  add_custom_command(TARGET ${name} POST_BUILD
                     COMMAND ${CMAKE_COMMAND} -E copy_if_different
                     $<TARGET_FILE_DIR:tbbmalloc>/$<TARGET_FILE_NAME:tbbmalloc>
                     $<TARGET_FILE_DIR:${name}>)
  add_custom_command(
      TARGET ${name} POST_BUILD
      COMMAND ${CMAKE_COMMAND} -E copy_if_different
      $<TARGET_FILE_DIR:tbbmalloc_proxy>/$<TARGET_FILE_NAME:tbbmalloc_proxy>
      $<TARGET_FILE_DIR:${name}>
  )
endmacro()

macro(SET_OPTION option value)
  set(${option} ${value} CACHE INTERNAL "" FORCE)
endmacro()

if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -Wno-error")
elseif (MSVC)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /std:c++17")
  add_definitions(-D_USE_MATH_DEFINES)
  add_compile_options(/wd4250)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")
endif ()

if (WIN32)
  add_definitions(-DUNICODE -D_UNICODE -D_AMD64_=100 -D_M_X64=100 -D_WIN64=1
                  -D_WIN32=1)
elseif(UNIX)

endif ()
add_subdirectory(lmlib)
add_subdirectory(lmengine)
add_subdirectory(lmeditor)