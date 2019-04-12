cmake_minimum_required(VERSION 3.5)
project(ml_cxx)

set(CMAKE_CXX_STANDARD 11)

if(NOT DEFINED CMAKE_LIBRARY_OUTPUT_DIRECTORY)
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR})
endif()

set(THIRD_PARTY_DIRS ${PROJECT_SOURCE_DIR}/third_party)

add_compile_options ("-fexceptions" "-g")
add_compile_options ("-O3")
add_definitions ("-DNDEBUG")

find_package(PythonInterp 2.7 REQUIRED)
find_package(PythonLibs 2.7 REQUIRED)

add_subdirectory(${THIRD_PARTY_DIRS}/pybind11)

file(GLOB_RECURSE SOURCES src/*.cpp src/*.hpp)
pybind11_add_module(ml_cxx ${SOURCES})

set_target_properties(ml_cxx PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}
)
