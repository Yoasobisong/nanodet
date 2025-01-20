cmake_minimum_required(VERSION 2.8.3)
set(CMAKE_CXX_STANDARD 17)

project(nanodet_demo)

# 查找 OpenMP 包
find_package(OpenMP REQUIRED)
if(OPENMP_FOUND)
    message("OPENMP FOUND")
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    message("OpenMP version: ${OpenMP_VERSION}")
    message("OpenMP libraries: ${OpenMP_LIBS}")
    message("OpenMP include path: ${OpenMP_INCLUDE_DIRS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
else()
    message("OPENMP NOT FOUND")
endif()

# 查找 OpenCV 包
find_package(OpenCV REQUIRED)
if(OpenCV_FOUND)
    message("OpenCV FOUND")
    message("OpenCV version: ${OpenCV_VERSION}")
    message("OpenCV libraries: ${OpenCV_LIBS}")
    message("OpenCV include path: ${OpenCV_INCLUDE_DIRS}")
else()
    message("OpenCV NOT FOUND")
endif()

# 查找 ncnn 包
find_package(ncnn REQUIRED)
if(NOT TARGET ncnn)
    message(WARNING "ncnn NOT FOUND!  Please set ncnn_DIR environment variable")
else()
    message("ncnn FOUND")
    message("ncnn include path: ${ncnn_INCLUDE_DIRS}")
    message("ncnn libraries: ${ncnn_LIBS}")
endif()

include_directories(
    ${OpenCV_INCLUDE_DIRS}
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_BINARY_DIR}
    # 如果 ncnn 提供了额外的 include 路径，也包含它们
    ${ncnn_INCLUDE_DIRS}
)

add_executable(nanodet_demo main.cpp nanodet.cpp)

target_link_libraries(
    nanodet_demo
    ncnn
    ${OpenCV_LIBS}
    # 如果 OpenMP 被找到，链接 OpenMP 库
    ${OpenMP_LIBRARIES}
)

# 打印出最终链接的库和标志
message("Linking nanodet_demo with libraries: ${OpenCV_LIBS} ${ncnn_LIBS} ${OpenMP_LIBRARIES}")
message("Using C flags: ${CMAKE_C_FLAGS}")
message("Using CXX flags: ${CMAKE_CXX_FLAGS}")
message("Using EXE linker flags: ${CMAKE_EXE_LINKER_FLAGS}")