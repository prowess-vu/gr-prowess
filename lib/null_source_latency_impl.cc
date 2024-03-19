/* -*- c++ -*- */
/* MIT License
 *
 * Copyright (c) 2024 prowess-vu
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#include "null_source_latency_impl.h"
#include <gnuradio/io_signature.h>
#include "tracepoint.h"

namespace gr {
  namespace prowess {

    null_source_latency::sptr null_source_latency::make(size_t item_size, uint64_t granularity)
    {
      return gnuradio::make_block_sptr<null_source_latency_impl>(item_size, granularity);
    }

    null_source_latency_impl::null_source_latency_impl(size_t item_size, uint64_t granularity)
        : gr::sync_block("null_source_latency",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(1, 1, sizeof(item_size))),
          granularity(granularity), item_size(item_size)
    {}

    null_source_latency_impl::~null_source_latency_impl()
    {}

    int null_source_latency_impl::work(int noutput_items,
                                      gr_vector_const_void_star &input_items,
                                      gr_vector_void_star &output_items)
    {
      void* out = static_cast<void *>(output_items[0]);
      std::memset(out, 0, noutput_items * item_size);
      uint64_t items = nitems_written(0);
      uint64_t before = items / granularity;
      uint64_t after = (items + noutput_items) / granularity;
      for(int i = 1; i <= (int)(before - after); ++i)
        tracepoint(null_rand_latency, tx, unique_id(), before + i * granularity);
      return noutput_items;
    }

  } /* namespace prowess */
} /* namespace gr */
