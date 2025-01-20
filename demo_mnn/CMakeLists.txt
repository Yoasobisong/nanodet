cmake_minimum_required(VERSION 3.9)
project(nanodet-mnn)

set(CMAKE_CXX_STANDARD 17)

# find_package(OpenCV REQUIRED PATHS "/work/dependence/opencv/opencv-3.4.3/build")
find_package(OpenCV REQUIRED)
include_directories(
        mnn/include
        .
)

link_directories(mnn/lib)

add_executable(nanodet-mnn main.cpp nanodet_mnn.cpp)
target_link_libraries(nanodet-mnn MNN ${OpenCV_LIBS})

message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
message(STATUS "OpenCV include dirs: ${OpenCV_INCLUDE_DIRS}")

message(STATUS "MNN include dir: ${CMAKE_CURRENT_SOURCE_DIR}/mnn/include")
message(STATUS "Project source dir: ${CMAKE_CURRENT_SOURCE_DIR}")

message(STATUS "MNN library dir: ${CMAKE_CURRENT_SOURCE_DIR}/mnn/lib")

message(STATUS "Libraries for nanodet-mnn: ${OPENCV_LIBS}")