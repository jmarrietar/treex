from unittest import TestCase

import jax.numpy as jnp
import numpy as np
import pytest

import treex as tx


class LossTest(TestCase):
    def test_basic(self):
        class MAE(tx.Loss):
            def call(self, y_true, y_pred):
                return jnp.abs(y_true - y_pred)

        y_true = jnp.array([1.0, 2.0, 3.0])
        y_pred = jnp.array([2.0, 3.0, 4.0])

        mae = MAE()

        sample_loss = mae.call(y_true, y_pred)
        loss = mae(y_true, y_pred)

        assert jnp.alltrue(sample_loss == jnp.array([1.0, 1.0, 1.0]))
        assert loss == 1

    def test_slice(self):
        class MAE(tx.Loss):
            def call(self, y_true, y_pred):
                return jnp.abs(y_true - y_pred)

        y_true = dict(a=jnp.array([1.0, 2.0, 3.0]))
        y_pred = dict(a=jnp.array([2.0, 3.0, 4.0]))

        mae = MAE(on="a")

        # raises because it doesn't use kwargs
        with pytest.raises(BaseException):
            sample_loss = mae(y_true, y_pred)

        # raises because it doesn't use __call__ which filters
        with pytest.raises(BaseException):
            sample_loss = mae.call(y_true=y_true, y_pred=y_pred)

        loss = mae(y_true=y_true, y_pred=y_pred)

        assert loss == 1
