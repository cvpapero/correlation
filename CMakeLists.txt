cmake_minimum_required(VERSION 2.8.3)
project(rqt_correlation)

find_package(catkin REQUIRED COMPONENTS
  rqt_gui
  rqt_gui_cpp
  rqt_gui_py
)

find_package(Qt4 COMPONENTS QtCore QtGui REQUIRED)

include(${QT_USE_FILE})

set(rqt_correlation_SRCS
  src/rqt_correlation/correlation.cpp
)

set(rqt_correlation_HDRS
  include/rqt_correlation/correlation.h
)

#set(rqt_image_view_UIS
#  src/rqt_image_view/image_view.ui
#)

set(rqt_correlation_INCLUDE_DIRECTORIES
  include
  ${CMAKE_CURRENT_BINARY_DIR}
)

catkin_package(
  INCLUDE_DIRS ${rqt_correlation_INCLUDE_DIRECTORIES}
  LIBRARIES ${PROJECT_NAME}
  CATKIN_DEPENDS rqt_gui rqt_gui_cpp 
)
#catkin_python_setup()

qt4_wrap_cpp(rqt_correlation_MOCS ${rqt_correlation_HDRS})
#qt4_wrap_ui(rqt_image_view_UIS_H ${rqt_image_view_UIS})

#include_directories(${rqt_correlation_INCLUDE_DIRECTORIES} ${catkin_INCLUDE_DIRS})
#add_library(${PROJECT_NAME} ${rqt_correlation_SRCS} ${rqt_correlation_MOCS} )
#target_link_libraries(${PROJECT_NAME} ${catkin_LIBRARIES} ${QT_QTCORE_LIBRARY} ${QT_QTGUI_LIBRARY})

#add_executable(okao_client src/okao_client.cpp)
#target_link_libraries(okao_client ${catkin_LIBRARIES} ${OpenCV_LIBS} ${ZMQ_LIBRARIE} msgpack)

add_executable(test_qt src/test_qt.cpp)
target_link_libraries(test_qt ${catkin_LIBRARIES} ${QT_QTCORE_LIBRARY} ${QT_QTGUI_LIBRARY})

#find_package(class_loader)
#class_loader_hide_library_symbols(${PROJECT_NAME})

#install(FILES plugin.xml
#  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
#)

#install(TARGETS ${PROJECT_NAME}
#  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
#  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
#  RUNTIME DESTINATION ${CATKIN_GLOBAL_BIN_DESTINATION}
#)

#install(PROGRAMS scripts/rqt_correlation
#  DESTINATION ${CATKIN_GLOBAL_BIN_DESTINATION}
#)
#install(PROGRAMS scripts/rqt_correlation
#  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
#)

#install(DIRECTORY include/${PROJECT_NAME}/
#  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
#)
