#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Vanderbilt University, Will Hedgecock.
#
# Use of this source code is governed by an MIT-style license that can be
# found in the LICENSE file or at https://opensource.org/licenses/MIT.
#
# SPDX-License-Identifier: MIT
#

from gnuradio import gr, gr_unittest
from gnuradio.prowess import signal_generator

class qa_signal_generator(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_instance(self):
        # FIXME: Test will fail until you pass sensible arguments to the constructor
        instance = signal_generator()

    def test_001_descriptive_test_name(self):
        # set up fg
        self.tb.run()
        # check data


if __name__ == '__main__':
    gr_unittest.run(qa_signal_generator)
