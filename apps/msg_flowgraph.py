#!/usr/bin/env python3

from gnuradio import gr, blocks
from gnuradio.eng_arg import intx
from argparse import ArgumentParser
import sys, time, pmt
import numpy as np
import pmt


class top(gr.top_block):

   def __init__(self):
      gr.top_block.__init__(self)

      parser = ArgumentParser("Profile GNU Radio Scheduler")
      parser.add_argument("-R", "--run", type=int, default=0, help="the run number (default=%(default)s)")
      parser.add_argument("-p", "--pipes", type=intx, default=1, help="the number of pipelines to create (default=%(default)s)")
      parser.add_argument("-s", "--stages", type=intx, default=1, help="the number of stages in each pipeline (default=%(default)s)")
      parser.add_argument("-r", "--repetitions", type=int, default=10, help="the number of repetitions (default=%(default)s)")
      parser.add_argument("-b", "--burst_size", type=int, default=10, help="the number of PDUs per burst (default=%(default)s)")
      parser.add_argument("-S", "--pdu_size", type=intx, default=8, help="size of PDUs in byte (default=%(default)s)")
      parser.add_argument("-c", "--config", default="fork", help=("the flow graph layout (default=%(default)s)"))
      parser.add_argument("-m", "--machine-readable", action="store_true", help="machine readable output")
      args = parser.parse_args()

      self.run_num = args.run
      self.pipes = args.pipes
      self.stages = args.stages
      self.config = args.config
      self.repetitions = args.repetitions
      self.burst_size = args.burst_size
      self.pdu_size = args.pdu_size
      self.machine_readable = args.machine_readable

      if self.config == "fork":
         self.create_fork()
      elif self.config == "diamond":
         self.create_diamond()
      else:
         print("Unknown config!")
         sys.exit(1)


   def create_fork(self):

      self.src = blocks.pdu_filter(pmt.intern("foo"), pmt.intern("bar"), False)

      for _ in range(self.pipes):
         prev = blocks.pdu_filter(pmt.intern("foo"), pmt.intern("bar"), False)
         self.msg_connect((self.src, 'pdus'), (prev, 'pdus'))

         for _ in range(1, self.stages):
               block = blocks.pdu_filter(pmt.intern("foo"), pmt.intern("bar"), False)
               self.msg_connect((prev, 'pdus'), (block, 'pdus'))
               prev = block


   def create_diamond(self):

      self.src = blocks.pdu_filter(pmt.intern("foo"), pmt.intern("bar"), False)
      snk = blocks.pdu_filter(pmt.intern("foo"), pmt.intern("bar"), False)

      for _ in range(self.pipes):
         prev = blocks.pdu_filter(pmt.intern("foo"), pmt.intern("bar"), False)
         self.msg_connect((self.src, 'pdus'), (prev, 'pdus'))

         for _ in range(1, self.stages):
               block = blocks.pdu_filter(pmt.intern("foo"), pmt.intern("bar"), False)
               self.msg_connect((prev, 'pdus'), (block, 'pdus'))
               prev = block

         self.msg_connect((prev, 'pdus'), (snk, 'pdus'))


def time_it(tb):

   port = pmt.intern('pdus')
   np_times = np.zeros(tb.repetitions)

   for r in range(tb.repetitions):
      for _ in range(tb.burst_size):
         msg = pmt.cons(pmt.PMT_NIL, pmt.make_u8vector(tb.pdu_size, 0x42))
         tb.src.to_basic_block()._post(port, msg)

      tb.src.to_basic_block()._post(
         pmt.intern("system"),
         pmt.cons(pmt.intern("done"), pmt.from_long(1)))

      start = time.time_ns()
      tb.run()
      stop = time.time_ns()

      np_times[r] = (stop-start)/1e9

      if tb.machine_readable:
         print("%s, %4d, %4d, %4d, %4d, %3d, %4d, %20.10f" % (
               tb.config, tb.run_num, tb.pipes, tb.stages, r, tb.burst_size,
               tb.pdu_size, np_times[r]))

   avg_time = np.mean(np_times)
   var_time = np.var(np_times)

   if not tb.machine_readable:
      print("config           %20s"   % (tb.config,))
      print("run              %20d"   % (tb.run_num,))
      print("pipes            %20d"   % (tb.pipes,))
      print("stages           %20d"   % (tb.stages,))
      print("repetitions      %20d"   % (tb.repetitions))
      print("burst_size       %20d"   % (tb.burst_size))
      print("pdu_size         %20d"   % (tb.pdu_size))
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
