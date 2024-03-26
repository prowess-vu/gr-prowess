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

#ifndef INCLUDED_PROWESS_COPY_RAND_H
#define INCLUDED_PROWESS_COPY_RAND_H

#include <gnuradio/block.h>
#include <gnuradio/prowess/api.h>

namespace gr {
  namespace prowess {

    /*!
     * \brief <+description of block+>
     * \ingroup prowess
     *
     */
    class PROWESS_API copy_rand : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<copy_rand> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of prowess::copy_rand.
       *
       * To avoid accidental use of raw pointers, prowess::copy_rand's
       * constructor is in a private implementation
       * class. prowess::copy_rand::make is the public interface for
       * creating new instances.
       */
      static sptr make(size_t item_size, size_t max_copy = 0xffffffff);
    };

  } // namespace prowess
} // namespace gr

#endif /* INCLUDED_PROWESS_COPY_RAND_H */
