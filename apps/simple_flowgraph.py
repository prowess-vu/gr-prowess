#!/usr/bin/env python3

from gnuradio import gr, blocks
from argparse import ArgumentParser
import sys, time, pmt
import numpy as np
import pmt


class top(gr.top_block):

   def __init__(self):
      gr.top_block.__init__(self)

      parser = ArgumentParser("Profile GNU Radio Scheduler")
      parser.add_argument("-R", "--run", type=int, default=0, help="the run number (default=%(default)s)")
      parser.add_argument("-r", "--repetitions", type=int, default=10, help="the number of repetitions (default=%(default)s)")
      args = parser.parse_args()

      self.run_num = args.run
      self.repetitions = args.repetitions

      self.src = blocks.null_source(gr.sizeof_float)
      self.sink = blocks.null_sink(gr.sizeof_float)
      self.connect(self.src, self.sink)


def time_it(tb):

   np_times = np.zeros(tb.repetitions)
   for r in range(tb.repetitions):
      start = time.time_ns()
      tb.run()
      stop = time.time_ns()
      np_times[r] = (stop-start)/1e9
      print("%4d, %20.10f" % (tb.run_num, np_times[r]))

   avg_time = np.mean(np_times)
   var_time = np.var(np_times)
   print("run              %20d"   % (tb.run_num,))
   print("repetitions      %20d"   % (tb.repetitions))
   print("avg_time         %20.15f" % (avg_time,))
   print("var_time         %20.15f" % (var_time,))


if __name__ == "__main__":

   # Catch any user-initiated keyboard interrupts
   try:

      # Enable FIFO-based scheduling in the OS for this flowgraph
      if gr.enable_realtime_scheduling(gr.RT_SCHED_FIFO) != gr.RT_OK:
         print("Error: Failed to enable FIFO scheduling")
         sys.exit(1)

      # Run the top-level flowgraph with timing probes enabled
      flowgraph = top()
      time_it(flowgraph)

   except KeyboardInterrupt:
      sys.exit(2)
