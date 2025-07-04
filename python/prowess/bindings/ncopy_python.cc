/*
 * Copyright 2024 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(ncopy.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(e7556332da023a37b4c9a27e1c4a5092)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/prowess/ncopy.h>
// pydoc.h is automatically generated in the build directory
#include <ncopy_pydoc.h>

void bind_ncopy(py::module& m)
{

    using ncopy    = gr::prowess::ncopy;


    py::class_<ncopy, gr::sync_block, gr::block, gr::basic_block,
        std::shared_ptr<ncopy>>(m, "ncopy", D(ncopy))

        .def(py::init(&ncopy::make),
           D(ncopy,make)
        )
        



        ;




}








