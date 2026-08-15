import warnings

import numpy as np

from dm_control.mujoco import index


def test_multidimensional_named_index_does_not_mutate_array_shape() -> None:
  axis = index.RegularNamedAxis(['a', 'b', 'c', 'd'])
  names = np.array([['a', 'b'], ['c', 'd']])

  with warnings.catch_warnings():
    warnings.simplefilter('error', DeprecationWarning)
    converted = axis.convert_key_item(names)

  np.testing.assert_array_equal(converted, np.array([[0, 1], [2, 3]]))
