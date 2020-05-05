import os
import numpy as np
import pandas as pd

import pytest

from skmultiflow.data.temporal_data_stream import TemporalDataStream


def test_temporal_data_stream(test_path, package_path):
    test_file = os.path.join(package_path, 'src/skmultiflow/data/datasets/sea_stream.csv')
    raw_data = pd.read_csv(test_file)
    stream = TemporalDataStream(raw_data, name='Test')

    assert stream.n_remaining_samples() == 40000

    expected_names = ['attrib1', 'attrib2', 'attrib3']
    assert stream.feature_names == expected_names

    expected_targets = [0, 1]
    assert stream.target_values == expected_targets

    assert stream.target_names == ['class']

    assert stream.n_features == 3

    assert stream.n_cat_features == 0

    assert stream.n_num_features == 3

    assert stream.n_targets == 1

    assert stream.get_data_info() == 'Test: 1 target(s), 2 classes'

    assert stream.has_more_samples() is True

    assert stream.is_restartable() is True

    # Load test data corresponding to first 10 instances
    test_file = os.path.join(test_path, 'sea_stream_file.npz')
    data = np.load(test_file)
    X_expected = data['X']
    y_expected = data['y']

    X, y, _, _, _ = stream.next_sample()
    assert np.alltrue(X[0] == X_expected[0])
    assert np.alltrue(y[0] == y_expected[0])

    X, y, _, _, _ = stream.last_sample()
    assert np.alltrue(X[0] == X_expected[0])
    assert np.alltrue(y[0] == y_expected[0])

    stream.restart()
    X, y, _, _, _ = stream.next_sample(10)
    assert np.alltrue(X == X_expected)
    assert np.alltrue(y == y_expected)

    assert stream.n_targets == np.array(y).ndim

    assert stream.n_features == X.shape[1]

    assert 'stream' == stream._estimator_type

    expected_info = "DataStream(n_targets=-1, target_idx=1, cat_features=None, name='Test')"
    assert stream.get_info() == expected_info


def test_temporal_data_stream_X_y(test_path, package_path):
    test_file = os.path.join(package_path, 'src/skmultiflow/data/datasets/sea_stream.csv')
    raw_data = pd.read_csv(test_file)
    y = raw_data.iloc[:, -1:]
    X = raw_data.iloc[:, :-1]
    stream = TemporalDataStream(X, y)

    assert stream._Y_is_defined

    assert stream.n_remaining_samples() == 40000

    expected_names = ['attrib1', 'attrib2', 'attrib3']
    assert stream.feature_names == expected_names

    expected_targets = [0, 1]
    assert stream.target_values == expected_targets

    assert stream.target_names == ['class']

    assert stream.n_features == 3

    assert stream.n_cat_features == 0

    assert stream.n_num_features == 3

    assert stream.n_targets == 1

    assert stream.get_data_info() == '1 target(s), 2 classes'

    assert stream.has_more_samples() is True

    assert stream.is_restartable() is True

    # Load test data corresponding to first 10 instances
    test_file = os.path.join(test_path, 'sea_stream_file.npz')
    data = np.load(test_file)
    X_expected = data['X']
    y_expected = data['y']

    X, y, _, _, _ = stream.next_sample()
    assert np.alltrue(X[0] == X_expected[0])
    assert np.alltrue(y[0] == y_expected[0])

    X, y, _, _, _ = stream.last_sample()
    assert np.alltrue(X[0] == X_expected[0])
    assert np.alltrue(y[0] == y_expected[0])

    stream.restart()
    X, y, _, _, _ = stream.next_sample(10)
    assert np.alltrue(X == X_expected)
    assert np.alltrue(y == y_expected)

    assert stream.n_targets == np.array(y).ndim

    assert stream.n_features == X.shape[1]


def test_check_data():
    # Test if data contains non-numeric values
    data = pd.DataFrame(np.array([[1, 2, 3, 4, 5],
                                  [6, 7, 8, 9, 10],
                                  [11, 'invalid', 13, 14, 15]]))

    with pytest.raises(ValueError):
        TemporalDataStream(data=data, allow_nan=False)

    # Test if data contains NaN values
    data = pd.DataFrame(np.array([[1, 2, 3, 4, 5],
                                  [6, 7, 8, 9, 10],
                                  [11, np.nan, 13, 14, 15]]))

    with pytest.raises(ValueError):
        TemporalDataStream(data=data, allow_nan=False)

    # Test warning for NaN values

    with pytest.warns(UserWarning):
        TemporalDataStream(data=data, allow_nan=True)