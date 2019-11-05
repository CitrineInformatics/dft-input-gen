import os
import json


__all__ = ['STANDARD_ATOMIC_WEIGHTS']


"""
Standard atomic weights from
https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses.

Filtered as follows:
- uncertainties in the `Standard Atomic Weight` column is ignored
- if the standard atomic weight is a range [a, b], the value used here is the
  mean. Note that the range encompasses atomic weight values of all normal
  materials, and does not imply any statistical distribution (i.e., the mean
  is not necessarily the most likely value).

"""
saw_file = os.path.join(os.path.dirname(__file__),
                        'standard_atomic_weights.json')
with open(saw_file) as fr:
    STANDARD_ATOMIC_WEIGHTS = json.load(fr)
