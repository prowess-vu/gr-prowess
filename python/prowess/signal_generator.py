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

from gnuradio import gr
import random, numpy as np
from .config_file_parser import parse_config
import torchsig

class signal_generator(gr.sync_block):
    """
    Generate a wideband RF signal using details from a specified JSON
    configuration file
    """

    def __init__(self, configuration):
        """
        Parse a time-based configuration object and seed a random number generator
        to allow for reproducibility between runs
        """
        gr.sync_block.__init__(self,
            name="Signal Generator",
            in_sig=None,
            out_sig=[np.float32])
        seed, self.config = parse_config(configuration)
        random.seed(seed)


    def work(self, input_items, output_items):
        # TODO: Actually generate the signal in realtime
        out = output_items[0]
        startnr = self.nitems_written(0)
        out[:] = np.sin(2 * np.pi * np.arange(startnr, startnr+len(output_items[0])))
        return len(output_items[0])
