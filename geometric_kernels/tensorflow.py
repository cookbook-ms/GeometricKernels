"""
Load TensorFlow backend in lab, spherical_harmonics and geometric_kernels using

.. code-block::

    import geometric_kernels.tensorflow
"""

import logging

import lab.tensorflow  # noqa
import spherical_harmonics.tensorflow  # noqa

import geometric_kernels.lab_extras.tensorflow  # noqa

logging.getLogger(__name__).info("Tensorflow backend enabled.")
