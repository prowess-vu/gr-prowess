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

#include "ncopy_impl.h"
#include <gnuradio/io_signature.h>

namespace gr {
  namespace prowess {

    using input_type = float;
    using output_type = float;

    ncopy::sptr ncopy::make(int ntimes)
    {
      return gnuradio::make_block_sptr<ncopy_impl>(ntimes);
    }


    ncopy_impl::ncopy_impl(int ntimes)
        : gr::sync_block("ncopy",
              gr::io_signature::make(1, 1, sizeof(input_type)),
              gr::io_signature::make(1, 1, sizeof(output_type))),
              num_times(ntimes), buffers{}
    {
      if (ntimes > 99)
        throw std::bad_alloc();
    }

    ncopy_impl::~ncopy_impl()
    {
    }

    int ncopy_impl::work(int noutput_items,
                         gr_vector_const_void_star &input_items,
                         gr_vector_void_star &output_items)
    {
      auto in = static_cast<const input_type *>(input_items[0]);
      auto out = static_cast<output_type *>(output_items[0]);

      if (num_times < 2)
      {
        std::memcpy(out, in, noutput_items * sizeof(output_type));
        return noutput_items;
      }

      std::memcpy(buffers[0], in, noutput_items * sizeof(output_type));
      for (int i = 0; i < num_times - 2; ++i)
        std::memcpy(buffers[i+1], buffers[i], noutput_items * sizeof(output_type));
      std::memcpy(out, buffers[num_times-2], noutput_items * sizeof(output_type));
      return noutput_items;
    }

  } /* namespace prowess */
} /* namespace gr */
