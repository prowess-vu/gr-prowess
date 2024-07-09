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

   def __init__(self, consume_amount):
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
      self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, consume_amount*1000)
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

def time_it(tb, np_times_avg, np_items, r):

   tb.run()
   tb.wait()
   np_times_avg[r] = tb.analog_sig_source_x_0.pc_work_time_avg()
   np_items[r] = tb.analog_sig_source_x_0.pc_nproduced_avg()

if __name__ == "__main__":

   # Catch any user-initiated keyboard interrupts
   try:

      # Enable FIFO-based scheduling in the OS for this flowgraph
      if gr.enable_realtime_scheduling(gr.RT_SCHED_FIFO) != gr.RT_OK:
         print("Error: Failed to enable FIFO scheduling")
         sys.exit(1)

      # Number of samples to process on each invocation
      sample_values = [12*2**i for i in range(1, 9)]
      data = {
        #"Num Items": [], 
	"Samples Consumed": [],
         #"Work Time Total": [],
	"Work Time": []
      }

      for consume_amount in sample_values:

         # Run the top-level flowgraph r times with timing probes enabled
         r = 10
         #np_times_total = np.zeros(r)
         np_times_avg = np.zeros(r)
         np_items = np.zeros(r)

         for i in range(r):
            flowgraph = top(consume_amount)
            time_it(flowgraph, np_times_avg, np_items, i)

         # Calculate stats for num. items processed and num. clock cycles for tested block
         avg_items = np.mean(np_items)
         var_items = np.var(np_items)
         avg_time_avg = np.mean(np_times_avg)
         #avg_time_total = np.mean(np_times_total)
         var_time = np.var(np_times_avg)

         new_entry = [avg_items, avg_time_avg]
         for key, value in zip(data.keys(), new_entry):
            data[key].append(value)

         print("avg_items   %20.15f" % (3*avg_items,))
         print("avg_time    %20.15f" % (avg_time_avg,))

      df = pd.DataFrame(data)
      print(df)
      df.to_csv("cs_source.csv", index=False)

   except KeyboardInterrupt:
      sys.exit(2)
