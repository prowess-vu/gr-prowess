#!/usr/bin/env python3

from gnuradio import gr, eng_notation, blocks, analog
from gnuradio.eng_arg import eng_float
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
      # Blocks
      ##################################################

      self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, self.samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
      self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
      self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, consume_amount)
      self.blocks_add_const_vxx_0 = blocks.add_const_cc(5)
      self.analog_sig_source_x_0 = analog.sig_source_c(self.samp_rate, analog.GR_COS_WAVE, 1000, 1, 0, 0)


      ##################################################
      # Connections
      ##################################################
      self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle2_0, 0))
      self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_null_sink_0, 0))
      self.connect((self.blocks_head_0, 0), (self.blocks_add_const_vxx_0, 0))
      self.connect((self.blocks_throttle2_0, 0), (self.blocks_head_0, 0))

      self.blocks_head_0.set_max_output_buffer(8192)
      self.blocks_head_0.set_max_noutput_items(consume_amount)

def time_it(tb, np_times_avg, np_items, r):

   tb.run()
   print(str(tb.blocks_head_0.max_output_buffer(0)))
   tb.wait()
   #np_times_total[r] = tb.blocks_add_const_vxx_0.pc_work_time_total()
   np_times_avg[r] = tb.blocks_add_const_vxx_0.pc_work_time_avg()
   np_items[r] = tb.blocks_add_const_vxx_0.pc_nproduced_avg()
   #print("%d - %d: Items Produced: %.10f, Work Time (CPU ticks): %d" % (tb.run_num, r, tb.blocks_add_const_vxx_0.pc_nproduced_avg(), tb.blocks_add_const_vxx_0.pc_work_time_avg()))


if __name__ == "__main__":

   # Catch any user-initiated keyboard interrupts
   try:

      # Enable FIFO-based scheduling in the OS for this flowgraph
      if gr.enable_realtime_scheduling(gr.RT_SCHED_FIFO) != gr.RT_OK:
         print("Error: Failed to enable FIFO scheduling")
         sys.exit(1)

      # Number of samples to process on each invocation
      sample_values = [i*40 for i in range(1, 50)]
      #sample_values = [2**i for i in range(2, 12)]
      data = {
        #"Num Items": [], 
	"Samples Consumed": [],
         #"Work Time Total": [],
	"Work Time": []
      }

      for consume_amount in sample_values:

         # Run the top-level flowgraph r times with timing probes enabled
         r = 100
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

         if consume_amount > 40:
             new_entry = [avg_items, avg_time_avg]
             for key, value in zip(data.keys(), new_entry):
                data[key].append(value)

         print("avg_items        %20.15f" % (avg_items,))
         print("avg_time    %20.15f" % (avg_time_avg,))

      df = pd.DataFrame(data)
      print(df)
      df.to_csv("add_const.csv", index=False)

   except KeyboardInterrupt:
      sys.exit(2)
