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

import os, json
import numpy as np
from gnuradio import gr
import torchsig

class signal_generator(gr.sync_block):
    """
    docstring for block signal_generator
    """
    def __init__(self, configuration):
        if not configuration:
            raise RuntimeError('Parameter "configuration" must be specified')
        elif not os.path.isfile(configuration):
            raise RuntimeError(f'Configuration file {configuration} does not exist')
        gr.sync_block.__init__(self,
            name="Signal Generator",
            in_sig=None,
            out_sig=[np.float32])

        # TODO: Parse the configuration JSON file
        self.config = []
        with open(configuration) as configFile:
            configData = json.load(configFile)


    def work(self, input_items, output_items):
        # TODO: Actually generate the signal in realtime
        out = output_items[0]
        startnr = self.nitems_written(0)
        out[:] = np.sin(2 * np.pi * np.arange(startnr, startnr+len(output_items[0])))
        return len(output_items[0])
