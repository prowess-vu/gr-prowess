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

#ifndef INCLUDED_PROWESS_COPY_RAND_IMPL_H
#define INCLUDED_PROWESS_COPY_RAND_IMPL_H

#include <random>
#include <gnuradio/prowess/copy_rand.h>

namespace gr {
  namespace prowess {

    class copy_rand_impl : public copy_rand {
     private:
      size_t max_copies;
      size_t item_size;
      std::mt19937 randomizer;

     public:
      copy_rand_impl(size_t item_size, size_t max_copy);
      ~copy_rand_impl();

      // Where all the action really happens
      void forecast(int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
                      gr_vector_int &ninput_items,
                      gr_vector_const_void_star &input_items,
                      gr_vector_void_star &output_items);
    };

  } // namespace prowess
} // namespace gr

#endif /* INCLUDED_PROWESS_COPY_RAND_IMPL_H */
