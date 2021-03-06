import clpy
from clpy import core


def column_stack(tup):
    """Stacks 1-D and 2-D arrays as columns into a 2-D array.

    A 1-D array is first converted to a 2-D column array. Then, the 2-D arrays
    are concatenated along the second axis.

    Args:
        tup (sequence of arrays): 1-D or 2-D arrays to be stacked.

    Returns:
        clpy.ndarray: A new 2-D array of stacked columns.

    .. seealso:: :func:`numpy.column_stack`

    """
    if any(not isinstance(a, clpy.ndarray) for a in tup):
        raise TypeError('Only clpy arrays can be column stacked')

    lst = list(tup)
    for i, a in enumerate(lst):
        if a.ndim == 1:
            a = a[:, clpy.newaxis]
            lst[i] = a
        elif a.ndim != 2:
            raise ValueError(
                'Only 1 or 2 dimensional arrays can be column stacked')

    return concatenate(lst, axis=1)


def concatenate(tup, axis=0):
    """Joins arrays along an axis.

    Args:
        tup (sequence of arrays): Arrays to be joined. All of these should have
            same dimensionalities except the specified axis.
        axis (int): The axis to join arrays along.

    Returns:
        clpy.ndarray: Joined array.

    .. seealso:: :func:`numpy.concatenate`

    """
    return core.concatenate_method(tup, axis)


def dstack(tup):
    """Stacks arrays along the third axis.

    Args:
        tup (sequence of arrays): Arrays to be stacked. Each array is converted
            by :func:`clpy.atleast_3d` before stacking.

    Returns:
        clpy.ndarray: Stacked array.

    .. seealso:: :func:`numpy.dstack`

    """
    return concatenate([clpy.atleast_3d(m) for m in tup], 2)


def hstack(tup):
    """Stacks arrays horizontally.

    If an input array has one dimension, then the array is treated as a
    horizontal vector and stacked along the first axis. Otherwise, the array is
    stacked along the second axis.

    Args:
        tup (sequence of arrays): Arrays to be stacked.

    Returns:
        clpy.ndarray: Stacked array.

    .. seealso:: :func:`numpy.hstack`

    """
    arrs = [clpy.atleast_1d(a) for a in tup]
    axis = 1
    if arrs[0].ndim == 1:
        axis = 0
    return concatenate(arrs, axis)


def vstack(tup):
    """Stacks arrays vertically.

    If an input array has one dimension, then the array is treated as a
    horizontal vector and stacked along the additional axis at the head.
    Otherwise, the array is stacked along the first axis.

    Args:
        tup (sequence of arrays): Arrays to be stacked. Each array is converted
            by :func:`clpy.atleast_2d` before stacking.

    Returns:
        clpy.ndarray: Stacked array.

    .. seealso:: :func:`numpy.dstack`

    """
    return concatenate([clpy.atleast_2d(m) for m in tup], 0)


def stack(tup, axis=0):
    """Stacks arrays along a new axis.

    Args:
        tup (sequence of arrays): Arrays to be stacked.
        axis (int): Axis along which the arrays are stacked.

    Returns:
        clpy.ndarray: Stacked array.

    .. seealso:: :func:`numpy.stack`
    """
    for x in tup:
        if not (-x.ndim <= axis < x.ndim):
            raise core.core._AxisError(
                'axis {} out of bounds [0, {})'.format(axis, x.ndim))
    return concatenate([clpy.expand_dims(x, axis) for x in tup], axis)


def _get_positive_axis(ndim, axis):
    a = axis
    if a < 0:
        a += ndim
    if a < 0 or a >= ndim:
        raise core.core._AxisError(
            'axis {} out of bounds [0, {})'.format(axis, ndim))
    return a
