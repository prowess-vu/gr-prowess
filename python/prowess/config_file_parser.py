#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2024 Vanderbilt University, Will Hedgecock.
#
# Use of this source code is governed by an MIT-style license that can be
# found in the LICENSE file or at https://opensource.org/licenses/MIT.
#
# SPDX-License-Identifier: MIT
#

import json, os, random, sys, uuid
from collections import defaultdict

# See https://arxiv.org/pdf/2207.09918.pdf for explanation of modulation schemes and impairments
required_emitter_keys = set(['name', 'centerFrequencyMHz', 'bandwidthkHz', 'modulationScheme', 'events'])
required_event_keys = set(['onSec', 'offSec', 'gaindB', 'impairments'])
valid_modulation_schemes = ['4ask', '8ask', '16ask', '32ask', '64ask', 'ook', '4pam', '8pam', '16pam', '32pam', '64pam',
                            'bpsk', 'qpsk', '8psk', '16psk', '32psk', '64psk', '16qam', '32qam', '32qam_cross', '64qam',
                            '128qam_cross', '256am', '512am_cross', '1024am', '2fsk', '2gfsk', '2msk', '2gmsk',
                            '4fsk', '4gfsk', '4msk', '4gmsk', '8fsk', '8gfsk', '8msk', '8gmsk', '16fsk', '16gfsk',
                            '16msk', '16gmsk', 'ofdm-64', 'ofdm-72', 'ofdm-128', 'ofdm-180', 'ofdm-256', 'ofdm-300',
                            'ofdm-512', 'ofdm-600', 'ofdm-900', 'ofdm-1024', 'ofdm-1200', 'ofdm-2048']
valid_impairments = ['TargetSNR', 'RandomPulseShaping', 'AddNoise', 'RandomPhaseShift', 'RandomTimeShift',
                     'RandomFrequencyShift', 'RayleighFadingChannel', 'IQImbalance', 'RandomResample',
                     'TimeReversal', 'SpectralInversion', 'ChannelSwap', 'AmplitudeReversal', 'RandomDropSamples',
                     'Quantize', 'RandomMagRescale', 'CutOut', 'PatchShuffle', 'RollOff', 'LocalOscillatorDrift',
                     'TimeVaryingNoise', 'Clip', 'AddSlope', 'RandomConvolve', 'GainDrift', 'AutomaticGainControl']


def parse_config(config_file_path):

  # Validate configuration file existence
  if not config_file_path:
    raise RuntimeError('Parameter "configuration" must be specified')
  elif not os.path.isfile(config_file_path):
    raise RuntimeError(f'Configuration file {config_file_path} does not exist')

  # Read data from the configuration file
  with open(config_file_path) as config_file:
    config_data = json.load(config_file)
  if 'emitters' not in config_data:
    raise RuntimeError('No "emitters" found in configuration file')
  seed = config_data['randomizerSeed'] \
         if 'randomizerSeed' in config_data and config_data['randomizerSeed'] is not None \
         else int.from_bytes(random.SystemRandom().randbytes(4))

  # Validate configuration data
  for emitter in config_data['emitters']:
    if required_emitter_keys.difference(emitter.keys()):
      raise RuntimeError(f'Emitter missing required parameter(s): {required_emitter_keys.difference(emitter.keys())}')
    elif emitter['modulationScheme'].lower() not in valid_modulation_schemes:
      raise RuntimeError(f'Modulation scheme "{emitter['modulationScheme']}" for emitter "{emitter['name']}" is invalid. Must be one of: {valid_modulation_schemes}')
    for event in emitter['events']:
      if required_event_keys.difference(event.keys()):
        raise RuntimeError(f'Event for emitter "{emitter['name']}" missing required parameter(s): {required_event_keys.difference(event.keys())}')
      invalid_impairments = [impairment for impairment in event['impairments'] if impairment not in valid_impairments]
      if invalid_impairments:
        raise RuntimeError(f'Impairment(s) for event in emitter "{emitter['name']}" are invalid: {invalid_impairments}')

  # Return a time-based configuration data structure
  config = defaultdict(list)
  for emitter in config_data['emitters']:
    for event in emitter['events']:
      event_id = uuid.uuid4().hex
      config[float(event['onSec'])].append({
        'type': 'on',
        'id': event_id,
        'emitter': emitter['name'],
        'freq': emitter['centerFrequencyMHz'],
        'bw': emitter['bandwidthkHz'],
        'mod': emitter['modulationScheme'],
        'gain': event['gaindB'],
        'impairments': event['impairments']
        })
      config[float(event['offSec'])].append({
        'type': 'off',
        'id': event_id
      })
  return seed, dict(sorted(config.items()))


# Make command-line runnable
if __name__ == '__main__':

  # Validate command-line parameters
  if len(sys.argv) != 2:
    print('\nUsage: ./config_file_parser.py [CONFIG_FILE.py]\n')
    os._exit(1)

  # Validate configuration file
  seed, config = parse_config(sys.argv[1])
  if seed:
    print('Randomization Seed:', seed)
  print('Configuration:', json.dumps(config, indent=2))
  print('Validation Test: PASSED')
