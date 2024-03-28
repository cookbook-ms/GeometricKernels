"""
The library root. The kernel classes are contained within the
:py:mod:`kernels <geometric_kernels.kernels>` package. They need to be paired
with one of the space classes from the
:py:mod:`spaces <geometric_kernels.spaces>` package.

The :py:mod:`frontends <geometric_kernels.frontends>` package contains kernel
wrapper classes compatible with Gaussian process libraries like
`GPFlow <https://www.gpflow.org/>`_, `GPyTorch <https://gpytorch.ai/>`_,
and `GPJax <https://github.com/JaxGaussianProcesses/GPJax>`_.

The :py:mod:`sampling <geometric_kernels.sampling>` package contains routines
that allow efficient (approximate) sampling of functions from geometric Gaussian
process priors. It also contains utilities for sampling spectral densities.

The :py:mod:`lab_extras <geometric_kernels.lab_extras>` package contains our
custom additions to `LAB <https://github.com/wesselb/lab>`_, the framework that
allows our library to be backend-independent. This is an internal part of our
library.

"""
import logging

import geometric_kernels._logging  # noqa: F401
from geometric_kernels.lab_extras import *

logging.getLogger(__name__).info(
    "Numpy backend is enabled. To enable other backends, don't forget to `import geometric_kernels.*backend name*`."
)
logging.getLogger(__name__).info(
    "We may be suppressing some logging of external libraries. To override the logging policy, call `logging.basicConfig`."
)
