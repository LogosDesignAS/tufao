cmake_minimum_required(VERSION 3.18.1)
project(Tufao VERSION 1.4.5)
# Source files
set(tufao_SRC
    httpserver.cpp
    httpserverrequest.cpp
    httpserverresponse.cpp
    httpsserver.cpp
    priv/tcpserverwrapper.cpp
    priv/reasonphrase.cpp
    websocket.cpp
    abstractmessagesocket.cpp
    httpfileserver.cpp
    httpserverrequestrouter.cpp
    httppluginserver.cpp
    headers.cpp
    priv/rfc1123.cpp
    priv/rfc1036.cpp
    priv/asctime.cpp
    sessionstore.cpp
    simplesessionstore.cpp
    notfoundhandler.cpp
    urlrewriterhandler.cpp
    httpupgraderouter.cpp
	 classhandlermanager.cpp
    classhandler.cpp
        include/Tufao/urlrewriterhandler.h
        include/Tufao/httpserver.h
        include/Tufao/classhandlermanager.h
        include/Tufao/httpupgraderouter.h
        include/Tufao/simplesessionstore.h
        include/Tufao/websocket.h
        include/Tufao/httpsserver.h
        include/Tufao/sessionstore.h
        include/Tufao/notfoundhandler.h
        include/Tufao/httpserverresponse.h
        include/Tufao/abstractmessagesocket.h
        include/Tufao/httppluginserver.h
        include/Tufao/httpfileserver.h
        include/Tufao/httpserverrequest.h
        include/Tufao/httpserverrequestrouter.h
)

add_definitions(-DTUFAO_LIBRARY)
if(NOT MSVC)
    add_definitions(
        -Wall
        -Wextra
#        -Wpedantic
#        -Weffc++
    )
endif()

add_library("${TUFAO_LIBRARY}" SHARED ${tufao_SRC})

target_link_libraries("${TUFAO_LIBRARY}" PUBLIC boost::boost Qt6::Core Qt6::Network)

set_target_properties(
    "${TUFAO_LIBRARY}"
    PROPERTIES
    SOVERSION ${TUFAO_VERSION_MAJOR}
    VERSION ${TUFAO_VERSION}
    VS_KEYWORD Qt4VSv1.0
    AUTOMOC ON
    INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/${libdir}"
)

target_include_directories("${TUFAO_LIBRARY}"
  PRIVATE
  "${CMAKE_SOURCE_DIR}/3rd/boost.http/include" ${Boost_INCLUDE_DIR})

# CXX_STANDARD was introduced in CMake 3.1
if("${CMAKE_VERSION}" VERSION_GREATER "3.0")
    set_target_properties(
        "${TUFAO_LIBRARY}"
        PROPERTIES
        CXX_STANDARD 11
        CXX_STANDARD_REQUIRED ON
    )
endif()

set(LIB_NAME "${TUFAO_LIBRARY}")
target_include_directories(${LIB_NAME}
        PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include/Tufao>
        $<INSTALL_INTERFACE:include>
)
add_library("Tufao::${PROJECT_NAME}" ALIAS ${LIB_NAME})
install(TARGETS "${LIB_NAME}"
        EXPORT "${PROJECT_NAME}Targets"
        LIBRARY DESTINATION "lib"
        ARCHIVE DESTINATION "lib"
        RUNTIME DESTINATION "bin"
        INCLUDES DESTINATION "include"
)
install(DIRECTORY "include/" DESTINATION "include")

install(EXPORT "${PROJECT_NAME}Targets"
        FILE "${PROJECT_NAME}Targets.cmake"
        NAMESPACE Tufao::
        DESTINATION "lib/cmake/${PROJECT_NAME}"
)

include(CMakePackageConfigHelpers)

configure_package_config_file(
        "${CMAKE_CURRENT_SOURCE_DIR}/config.cmake.in"
        "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
        INSTALL_DESTINATION "lib/cmake/${PROJECT_NAME}"
)

write_basic_package_version_file(
        "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake"
        VERSION ${PROJECT_VERSION}
        COMPATIBILITY AnyNewerVersion
)

install(FILES
        "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
        "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake"
        DESTINATION "lib/cmake/${PROJECT_NAME}"
)
