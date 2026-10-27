"""Expose Keras 3 model metadata to the unchanged Kaggle Keras 2 checkers."""
from functools import wraps
import importlib
from types import SimpleNamespace


class LayerView:
    def __init__(self, layer):
        self._layer = layer

    @property
    def __class__(self):
        return self._layer.__class__

    @property
    def input_shape(self):
        try:
            return self._layer.input_shape
        except AttributeError:
            return tuple(self._layer.input.shape)

    def __getattr__(self, name):
        return getattr(self._layer, name)


class ModelView:
    def __init__(self, model):
        self._model = model

    @property
    def layers(self):
        return [LayerView(layer) for layer in self._model.layers]

    def _configuration(self):
        try:
            return self._model.get_compile_config() or {}
        except AttributeError:
            return {}

    @property
    def compiled_loss(self):
        config = self._configuration()
        if config:
            return SimpleNamespace(_losses=config.get('loss'))
        return self._model.compiled_loss

    @property
    def compiled_metrics(self):
        config = self._configuration()
        if config:
            return SimpleNamespace(_metrics=config.get('metrics'))
        return self._model.compiled_metrics

    def __getattr__(self, name):
        return getattr(self._model, name)


def _adapt_model_check(problem_class):
    original = problem_class.check
    if getattr(original, '_ai_lab_keras_compat', False):
        return

    @wraps(original)
    def check(self, model):
        return original(self, ModelView(model))

    check._ai_lab_keras_compat = True
    problem_class.check = check


def install():
    import tensorflow as tf

    checks = {'ex1': ['Q2'], 'ex2': ['Q2', 'Q3'], 'ex3': ['Q1'],
              'ex5': ['Q1', 'Q3'], 'ex6': ['Q1', 'Q2']}
    for name, classes in checks.items():
        module = importlib.import_module('learntools.deep_learning_intro.'+name)
        for class_name in classes:
            _adapt_model_check(getattr(module, class_name))

    module = importlib.import_module('learntools.deep_learning_intro.ex1')
    original = module.Q3.check
    if not getattr(original, '_ai_lab_keras_compat', False):
        @wraps(original)
        def check_weights(self, w, b):
            def tensor_value(value):
                if tf.is_tensor(value):
                    return value
                inner = getattr(value, 'value', value)
                return inner() if callable(inner) else inner
            return original(self, tensor_value(w), tensor_value(b))

        check_weights._ai_lab_keras_compat = True
        module.Q3.check = check_weights
