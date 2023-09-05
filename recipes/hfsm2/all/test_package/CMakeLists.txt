cmake_minimum_required(VERSION 3.15)

project(PackageTest LANGUAGES CXX)

find_package(hfsm2 REQUIRED CONFIG)

add_executable(example example.cpp)
target_link_libraries(example hfsm2::hfsm2)
