#!/usr/bin/env python3

from gnuradio import gr, eng_notation, blocks, analog, audio, filter
from gnuradio.eng_arg import eng_float
from gnuradio.filter import firdes
from gnuradio.fft import window
from argparse import ArgumentParser
import sys, time, pmt
import numpy as np
import pandas as pd
import pmt


class top(gr.top_block):

   def __init__(self, consume_amount, period, source_e, fir1_e, squelch_e, fir0_e, multiply_e):
      gr.top_block.__init__(self)

      default_samples = 32000
      parser = ArgumentParser("Profile GNU Radio Scheduler")
      parser.add_argument("-R", "--run", type=int, default=0, help="the run number (default=%(default)s)")
      parser.add_argument("-r", "--repetitions", type=int, default=100, help="the number of repetitions (default=%(default)s)")
      parser.add_argument("-N", "--samples", type=eng_float, default=default_samples, help=("the number of samples to be consumed by the tested block (default=%s)" % (eng_notation.num_to_str(default_samples))))
      parser.add_argument("-f", "--frequency", type=int, default=50, help="the frequency of the source node (default=%(default)s)")
      args = parser.parse_args()

      self.run_num = args.run
      self.repetitions = args.repetitions
      self.samp_rate = args.samples

      ##################################################
      # Variables
      ##################################################
      self.samp_rate = samp_rate = 576000
      self.rf_decim = rf_decim = 3
      self.low_pass_filter_taps = low_pass_filter_taps = firdes.low_pass(1.0, samp_rate/rf_decim, 2.7e3,0.5e3, window.WIN_HAMMING, 6.76)
      self.channel_filter = channel_filter = firdes.complex_band_pass(1.0, samp_rate, -3000, 3000, 200, window.WIN_HAMMING, 6.76)

      ##################################################
      # Blocks
      ##################################################

      self.fir_filter_xxx_0 = filter.fir_filter_ccc(4, low_pass_filter_taps)
      self.fir_filter_xxx_0.declare_sample_delay(0)
      self.fir_filter_xxx_1 = filter.fir_filter_ccc(rf_decim, channel_filter)
      self.fir_filter_xxx_1.declare_sample_delay(0)
      self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, 30720)
      self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, consume_amount)
      self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
      self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
      self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(0.05)
      self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc((-50), 1)
      self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1000, 1, 0, 0)


      ##################################################
      # Connections
      ##################################################
      self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle2_0, 0))
      self.connect((self.blocks_throttle2_0, 0), (self.blocks_head_0, 0))
      self.connect((self.analog_simple_squelch_cc_0, 0), (self.fir_filter_xxx_0, 0))
      self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_null_sink_0, 0))
      self.connect((self.blocks_head_0, 0), (self.blocks_null_sink_1, 0))
      self.connect((self.analog_sig_source_x_0, 0), (self.fir_filter_xxx_1, 0))
      #self.connect((self.blocks_head_0, 0), (self.fir_filter_xxx_1, 0))
      self.connect((self.fir_filter_xxx_1, 0), (self.analog_simple_squelch_cc_0, 0))
      self.connect((self.fir_filter_xxx_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))

      self.blocks_multiply_const_vxx_0_0.set_max_noutput_items(int(consume_amount/12))
      self.fir_filter_xxx_0.set_max_noutput_items(int(consume_amount/12))
      self.analog_simple_squelch_cc_0.set_max_noutput_items(int(consume_amount/3))
      self.fir_filter_xxx_1.set_max_noutput_items(int(consume_amount/3))

      ##################################################
      # EDF Parameters
      ##################################################
      #self.analog_sig_source_x_0.enable_edf(source_e, period, period, False)
      #self.fir_filter_xxx_1.enable_edf(fir1_e, period, period, False)
      #self.analog_simple_squelch_cc_0.enable_edf(squelch_e, period, period, False)
      #self.fir_filter_xxx_0.enable_edf(fir0_e, period, period, False)
      #self.blocks_multiply_const_vxx_0_0.enable_edf(multiply_e, period, period, False)

      #self.blocks_add_const_vxx_0.enable_edf(50 * 1000000, 50 * 1000000, 100 * 1000000, False)


def time_it(tb, lates, r):
   start = time.time_ns()
   tb.run()
   tb.wait()
   stop = time.time_ns()
   lates[r] = stop - start


if __name__ == "__main__":

   # Catch any user-initiated keyboard interrupts
   try:

      # Number of samples to process on each invocation
      sample_values = [12*2**i for i in range(3, 9)]
      periods = [166667, 333333, 666667, 1333333, 2666667, 5333333]
      source_e = [431, 736, 1358, 2601, 5059, 9925]
      fir1_e = [158149, 295266, 522922, 1016194, 1974288, 3893483]
      squelch_e = [4527, 5155, 4944, 5469, 6481, 7410]
      fir0_e = [13790, 20079, 26518, 42332, 74769, 138191]
      multiply_e = [4379, 5908, 4634, 4935, 5055, 5465]
      data = {
	 "samples_consumed": [],
         #"Utilization": [],
         "Latency(ms)": []
      }

      for j in range(len(sample_values)):

         # Run the top-level flowgraph r times with timing probes enabled
         r = 100
         lates = np.zeros(r)

         for i in range(r):
            flowgraph = top(sample_values[j], periods[j], source_e[j], fir1_e[j], squelch_e[j], fir0_e[j], multiply_e[j])
            time_it(flowgraph, lates, i)

         # Calculate stats for num. items processed and num. clock cycles for tested block
         avg_late = np.mean(lates)
         util = (1/periods[j])*(source_e[j] + fir1_e[j] + squelch_e[j] + fir0_e[j] + multiply_e[j])

         new_entry = [sample_values[j], (avg_late/2.4)/1000000]
         for key, value in zip(data.keys(), new_entry):
            data[key].append(value)

         #print("util        %20.15f" % (util,))
         print("avg_late    %20.15f" % (avg_late,))

      df = pd.DataFrame(data)
      print(df)
      df.to_csv("case_study.csv", index=False)

   except KeyboardInterrupt:
      sys.exit(2)
