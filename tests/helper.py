import lab as B
import numpy as np
from beartype.door import die_if_unbearable, is_bearable
from beartype.typing import Any, Callable, List, Optional, Union
from plum import ModuleType, resolve_type_hint

from geometric_kernels.lab_extras import SparseArray
from geometric_kernels.spaces import (
    Circle,
    DiscreteSpectrumSpace,
    Graph,
    HypercubeGraph,
    Hypersphere,
    Mesh,
    ProductDiscreteSpectrumSpace,
    SpecialOrthogonal,
    SpecialUnitary,
)

from .data import TEST_GRAPH_ADJACENCY, TEST_MESH_PATH

EagerTensor = ModuleType("tensorflow.python.framework.ops", "EagerTensor")


def discrete_spectrum_spaces() -> List[DiscreteSpectrumSpace]:
    return [
        Circle(),
        HypercubeGraph(1),
        HypercubeGraph(3),
        HypercubeGraph(6),
        Hypersphere(2),
        Hypersphere(3),
        Hypersphere(10),
        SpecialOrthogonal(3),
        SpecialOrthogonal(8),
        SpecialUnitary(2),
        SpecialUnitary(5),
        Mesh.load_mesh(TEST_MESH_PATH),
        Graph(TEST_GRAPH_ADJACENCY, normalize_laplacian=False),
        Graph(TEST_GRAPH_ADJACENCY, normalize_laplacian=True),
        ProductDiscreteSpectrumSpace(Circle(), Hypersphere(3), Circle()),
        ProductDiscreteSpectrumSpace(
            Circle(), Graph(np.kron(TEST_GRAPH_ADJACENCY, TEST_GRAPH_ADJACENCY))
        ),  # TEST_GRAPH_ADJACENCY is too small for default parameters of the ProductDiscreteSpectrumSpace
        ProductDiscreteSpectrumSpace(Mesh.load_mesh(TEST_MESH_PATH), Hypersphere(2)),
    ]


def np_to_backend(value: B.NPNumeric, backend: str):
    """
    Converts a numpy array to the desired backend.

    :param value:
        A numpy array.
    :param backend:
        The backend to use, one of the strings "tensorflow", "torch", "numpy", "jax".

    :raises ValueError:
        If the backend is not recognized.

    :return:
        The array `value` converted to the desired backend.
    """
    if backend == "tensorflow":
        import tensorflow as tf

        return tf.convert_to_tensor(value)
    elif backend in ["torch", "pytorch"]:
        import torch

        return torch.tensor(value)
    elif backend == "numpy":
        return value
    elif backend == "jax":
        import jax.numpy as jnp

        return jnp.array(value)
    elif backend == "scipy_sparse":
        import scipy.sparse as sp

        return sp.csr_array(value)
    else:
        raise ValueError("Unknown backend: {}".format(backend))


def array_type(backend: str):
    """
    Returns the array type corresponding to the given backend.

    :param backend:
        The backend to use, one of the strings "tensorflow", "torch", "numpy",
        "jax", "scipy_sparse".

    :return:
        The array type corresponding to the given backend.
    """
    if backend == "tensorflow":
        return resolve_type_hint(Union[B.TFNumeric, EagerTensor])
    elif backend in ["torch", "pytorch"]:
        return resolve_type_hint(B.TorchNumeric)
    elif backend == "numpy":
        return resolve_type_hint(B.NPNumeric)
    elif backend == "jax":
        return resolve_type_hint(B.JAXNumeric)
    elif backend == "scipy_sparse":
        return resolve_type_hint(SparseArray)
    else:
        raise ValueError(f"Unknown backend: {backend}")


def check_function_with_backend(
    backend: str,
    result: Any,
    f: Callable,
    *args: Any,
    compare_to_result: Optional[Callable] = None,
    atol=1e-4,
):
    """
    1. Casts the arguments `*args` to the backend `backend`.
    2. Runs the function `f` on the casted arguments.
    3. Checks that the result is of the backend `backend`.
    4. If no `compare_to_result` kwarg is provided, checks that the result,
       casted back to numpy backend, coincides with the given `result`.
       If `compare_to_result` is provided, checks if
       `compare_to_result(result, f_output)` is True.

    :param backend:
        The backend to use, one of the strings "tensorflow", "torch", "numpy", "jax".
    :param result:
        The expected result of the function, if no `compare_to_result` kwarg is
        provided, expected to be a numpy array. Otherwise, can be anything.
    :param f:
        The backend-independent function to run.
    :param args:
        The arguments to pass to the function `f`, expected to be numpy arrays
        or non-array arguments.
    :param compare_to_result:
        A function that takes two arguments, the computed result and the
        expected result, and returns a boolean.
    :param atol:
        The absolute tolerance to use when comparing the computed result with
        the expected result.
    """

    args_casted = []
    for arg in args:
        if is_bearable(arg, B.Numeric):
            # We only expect numpy arrays here
            die_if_unbearable(arg, B.NPNumeric)
            args_casted.append(np_to_backend(arg, backend))
        else:
            args_casted.append(arg)
    f_output = f(*args_casted)
    assert is_bearable(f_output, array_type(backend))
    if compare_to_result is None:
        # we convert `f_output` to numpy array to compare with `result``
        if is_bearable(f_output, SparseArray):
            f_output = f_output.toarray()
        else:
            f_output = B.to_numpy(f_output)
        np.testing.assert_allclose(f_output, result, atol=atol)
    else:
        assert compare_to_result(result, f_output)
