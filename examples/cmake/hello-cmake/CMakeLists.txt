cmake_minimum_required(VERSION 3.18.1)
project(hello-world)

set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake/modules" ${CMAKE_MODULE_PATH})
message(STATUS ${CMAKE_MODULE_PATH})
find_package(Qt6Core REQUIRED)
find_package(Qt6Network REQUIRED)


find_package(CXX11 REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CXX11_FLAGS}")

add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME} ${TUFAO_LIBRARIES} Qt6::Core Qt6::Network Tufao::Tufao)
