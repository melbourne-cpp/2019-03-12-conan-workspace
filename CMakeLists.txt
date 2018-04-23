cmake_minimum_required(VERSION 3.6)
project(Workspace)
set(CMAKE_DEBUG_POSTFIX "")
set(CMAKE_RELWITHDEBINFO_POSTFIX "")
set(CMAKE_MINSIZEREL_POSTFIX "")
set(CMAKE_STATIC_LIBRARY_PREFIX "")
set(CMAKE_SHARED_LIBRARY_PREFIX "")

add_subdirectory(glslang)
add_subdirectory(openmesh)
add_subdirectory(embed-resource)

include_directories(embed-resource)

set(OPENMESH_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/openmesh/src)

if (MSVC)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /MP")
endif ()

if (MSVC)
  set(CMAKE_OLD_DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})
  set(CMAKE_DEBUG_POSTFIX _debug)
endif ()

set(TBB_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(TBB_BUILD_STATIC OFF CACHE BOOL "" FORCE)

add_subdirectory(tbb)

if (MSVC)
  set(CMAKE_DEBUG_POSTFIX ${CMAKE_OLD_DEBUG_POSTFIX})
endif ()

add_subdirectory(freetype2)

if (MSVC)
  set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
endif ()

add_subdirectory(googletest)

find_package(Vulkan REQUIRED)

if (UNIX)
  find_package(PkgConfig REQUIRED)
endif()

# Setup CMake to use GTK+, tell the compiler where to look for headers
# and to the linker where to look for libraries
INCLUDE_DIRECTORIES(${GTK3_INCLUDE_DIRS})
LINK_DIRECTORIES(${GTK3_LIBRARY_DIRS})

set(EIGEN_DIR ${CMAKE_CURRENT_SOURCE_DIR}/eigen)
set(EIGEN_INCLUDE_DIR ${EIGEN_DIR})

set(FREETYPE_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/freetype2/include)

set(TBB_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/tbb)

set(TBB_INCLUDE_DIR ${TBB_ROOT}/include)
set(TBB_BUILD_DIR ${TBB_DIR}/build)

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