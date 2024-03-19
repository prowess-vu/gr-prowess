# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: MIT
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT prowess_sources)
    message(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT prowess_sources)

########################################################################
# Check for pygccxml
########################################################################
gr_python_check_module_raw("pygccxml" "import pygccxml" PYGCCXML_FOUND)

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND prowess_python_files
    message_forward_python.cc
    ncopy_python.cc
    copy_rand_python.cc
    null_sink_latency_python.cc
    null_source_latency_python.cc python_bindings.cc)

gr_pybind_make_oot(prowess ../../.. gr::prowess "${prowess_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(
    TARGET prowess_python
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:prowess_python>
            ${PROJECT_BINARY_DIR}/test_modules/gnuradio/prowess/)

install(
    TARGETS prowess_python
    DESTINATION ${GR_PYTHON_DIR}/gnuradio/prowess
    COMPONENT pythonapi)
