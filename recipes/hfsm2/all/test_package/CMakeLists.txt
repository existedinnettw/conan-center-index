cmake_minimum_required(VERSION 3.14)

project(test_package LANGUAGES CXX)

find_package(hfsm2 REQUIRED CONFIG)

add_executable(${CMAKE_PROJECT_NAME} test_package.cpp)
target_link_libraries(${CMAKE_PROJECT_NAME} PRIVATE hfsm2::hfsm2)
