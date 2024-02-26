find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_PROWESS gnuradio-prowess)

FIND_PATH(
    GR_PROWESS_INCLUDE_DIRS
    NAMES gnuradio/prowess/api.h
    HINTS $ENV{PROWESS_DIR}/include
        ${PC_PROWESS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_PROWESS_LIBRARIES
    NAMES gnuradio-prowess
    HINTS $ENV{PROWESS_DIR}/lib
        ${PC_PROWESS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-prowessTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_PROWESS DEFAULT_MSG GR_PROWESS_LIBRARIES GR_PROWESS_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_PROWESS_LIBRARIES GR_PROWESS_INCLUDE_DIRS)
