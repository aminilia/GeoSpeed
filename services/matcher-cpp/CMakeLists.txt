cmake_minimum_required(VERSION 3.20)
project(geospeed_matcher VERSION 0.1.0 LANGUAGES CXX)

include(FetchContent)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(geospeed_matcher src/matcher.cpp)
target_include_directories(geospeed_matcher PUBLIC include)

add_executable(matcher_demo src/demo.cpp)
target_link_libraries(matcher_demo PRIVATE geospeed_matcher)

enable_testing()
FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/refs/tags/v1.15.2.zip
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_executable(matcher_tests tests/matcher_tests.cpp)
target_link_libraries(matcher_tests PRIVATE geospeed_matcher GTest::gtest_main)
include(GoogleTest)
gtest_discover_tests(matcher_tests)
