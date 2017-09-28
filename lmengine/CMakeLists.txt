project(lmengine)

add_library(
        lmengine

        src/world.cpp
)

target_include_directories(
        lmengine

        PUBLIC

        include
)