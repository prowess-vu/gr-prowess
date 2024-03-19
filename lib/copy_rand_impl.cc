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

#include "copy_rand_impl.h"
#include <gnuradio/io_signature.h>

namespace gr {
  namespace prowess {

    using input_type = uint8_t;
    using output_type = uint8_t;

    copy_rand::sptr copy_rand::make(size_t item_size, size_t max_copy)
    {
      return gnuradio::make_block_sptr<copy_rand_impl>(item_size, max_copy);
    }

    copy_rand_impl::copy_rand_impl(size_t item_size, size_t max_copy)
        : gr::block("copy_rand",
                    gr::io_signature::make(1, 1, sizeof(input_type)),
                    gr::io_signature::make(1, 1, sizeof(output_type))),
          max_copies(max_copy), item_size(item_size),
          randomizer(std::random_device{}())
    {}

    copy_rand_impl::~copy_rand_impl()
    {}

    void copy_rand_impl::forecast(int noutput_items,
                                  gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items;
    }

    int copy_rand_impl::general_work(int noutput_items,
                                    gr_vector_int &ninput_items,
                                    gr_vector_const_void_star &input_items,
                                    gr_vector_void_star &output_items)
    {
      auto in = static_cast<const input_type *>(input_items[0]);
      auto out = static_cast<output_type *>(output_items[0]);

      size_t m = std::min(std::min(noutput_items, ninput_items[0]), (int)max_copies);
      if (m > 0)
      {
        std::uniform_int_distribution<> distrib(1, m);
        m = distrib(randomizer);
        std::memcpy(out, in, m * item_size);
      }
      consume_each(m);
      return m;
    }

  } /* namespace prowess */
} /* namespace gr */
