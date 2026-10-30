"""Check runtime downloads, integrity and Keras checker compatibility without training."""
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import sys
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT/'ai_lab'
sys.path.insert(0, str(LAB/'tools'))
sys.path.insert(0, str(ROOT))
from colab_runtime import download_runtime
from keras_compat import LayerView, ModelView


def expect_failure(function):
    try:
        function()
    except (AssertionError, ValueError, AttributeError, TypeError):
        return
    raise AssertionError('An invalid answer unexpectedly passed the checker')


def check_downloads():
    manifest_path = LAB/'colab/runtime.json'
    manifest = json.loads(manifest_path.read_text())
    with tempfile.TemporaryDirectory(prefix='ai-lab-colab-') as temporary:
        root = Path(temporary)/'runtime'
        download_runtime(manifest_path.as_uri(), ROOT.as_uri(), root)
        for item in manifest['files']:
            assert hashlib.sha256((root/item['path']).read_bytes()).hexdigest() == item['sha256']
        assert (root/'ai_lab/input/train.csv').read_bytes() == (root/'ai_lab/input/home-data-for-ml-course/train.csv').read_bytes()
        assert (root/'ai_lab/input/test.csv').read_bytes() == (root/'ai_lab/input/home-data-for-ml-course/test.csv').read_bytes()
        # Use a fresh interpreter outside the checkout: repository imports would
        # hide missing files in the partial Colab download.
        subprocess.run([sys.executable, '-I', '-c', '''
import importlib.util
from pathlib import Path
import sys

root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('bootstrap', root/'ai_lab/tools/colab_runtime.py')
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)
namespace = {}
bootstrap.setup(root, namespace)
import learntools
from learntools.core import binder, tracking
assert binder.g is namespace
assert list(learntools.__path__) == [str(root/'learntools')]
assert learntools.__version__ == '0.3.5'
assert not (root/'learntools/data_viz_to_coder').exists()
assert 'learntools.data_viz_to_coder' not in sys.modules
tracking.track({})
import pandas as pd
from learntools.machine_learning.ex2 import LoadHomeData
home_data = pd.read_csv(root/'ai_lab/input/home-data-for-ml-course/train.csv')
LoadHomeData().check(home_data)
try:
    LoadHomeData().check(home_data.head())
except AssertionError:
    pass
else:
    raise AssertionError('The downloaded checker accepted incomplete data')
bootstrap.setup(root, namespace)
assert binder.g is namespace
assert Path.cwd() == root/'ai_lab/runtime'
''', str(root)], cwd=temporary, check=True)
        damaged = root/manifest['files'][0]['path']
        damaged.write_bytes(b'incomplete download')
        download_runtime(manifest_path.as_uri(), ROOT.as_uri(), root)
        assert hashlib.sha256(damaged.read_bytes()).hexdigest() == manifest['files'][0]['sha256']
        download_runtime(manifest_path.as_uri(), 'file:///missing-cached-source', root)
        bad_manifest = Path(temporary)/'unsafe.json'
        bad_manifest.write_text(json.dumps({'schema': 1, 'files': [
            {'path': '../outside', 'bytes': 0, 'sha256': 'invalid'}]}))
        expect_failure(lambda: download_runtime(bad_manifest.as_uri(), ROOT.as_uri(), root))
        bad_manifest.write_text(json.dumps({'schema': 1, 'files': [
            {**manifest['files'][0], 'sha256': '0'*64}]}))
        expect_failure(lambda: download_runtime(bad_manifest.as_uri(), ROOT.as_uri(), root))
    return len(manifest['files'])


def check_views():
    class Dense:
        units = 1
        input = type('Input', (), {'shape': (None, 11)})()
    class Model:
        layers = [Dense()]
        optimizer = object()
        def get_compile_config(self):
            return {'loss': 'binary_crossentropy', 'metrics': ['binary_accuracy']}
    view = ModelView(Model())
    assert view.layers[0].__class__.__name__ == 'Dense'
    assert view.layers[0].input_shape == (None, 11)
    assert view.layers[0].units == 1
    assert view.compiled_loss._losses == 'binary_crossentropy'
    assert view.compiled_metrics._metrics == ['binary_accuracy']
    assert LayerView(Dense()).input_shape == (None, 11)


def check_keras():
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    from learntools.core import binder, tracking
    from keras_compat import install

    tracking.track = lambda event: None
    if not binder.bound:
        binder.bind({})
    install()
    modules = {i: importlib.import_module(f'learntools.deep_learning_intro.ex{i}') for i in (1, 2, 3, 5, 6)}
    assertions = 0

    def check(question, good, bad):
        nonlocal assertions
        question.check(good)
        expect_failure(lambda: question.check(bad))
        assertions += 2

    single = keras.Sequential([layers.Dense(1, input_shape=[11])])
    check(modules[1].Q2(), single, keras.Sequential([layers.Dense(2, input_shape=[11])]))
    check(modules[1].Q2(), single, keras.Sequential([layers.Dense(1, input_shape=[10])]))
    modules[1].Q3().check(*single.weights)
    expect_failure(lambda: modules[1].Q3().check(*single.get_weights()))
    assertions += 2

    def deep_model(units):
        return keras.Sequential([layers.Dense(units, activation='relu', input_shape=[8]),
                                 layers.Dense(512, activation='relu'),
                                 layers.Dense(512, activation='relu'), layers.Dense(1)])
    check(modules[2].Q2(), deep_model(512), deep_model(64))
    explicit = keras.Sequential([layers.Dense(32, input_shape=[8]), layers.Activation('relu'),
                                 layers.Dense(32), layers.Activation('relu'), layers.Dense(1)])
    check(modules[2].Q3(), explicit, deep_model(512))

    good = keras.Sequential([layers.Dense(1, input_shape=[50])])
    good.compile(optimizer='adam', loss='mae')
    bad = keras.Sequential([layers.Dense(1, input_shape=[50])])
    bad.compile(optimizer='adam', loss='mse')
    check(modules[3].Q1(), good, bad)
    bad.compile(optimizer='sgd', loss='mae')
    expect_failure(lambda: modules[3].Q1().check(bad))
    assertions += 1

    def dropout_model(rate):
        return keras.Sequential([layers.Dense(128, activation='relu', input_shape=[5]),
                                 layers.Dropout(rate), layers.Dense(64, activation='relu'),
                                 layers.Dropout(rate), layers.Dense(1)])
    check(modules[5].Q1(), dropout_model(.3), dropout_model(.5))
    normalized = keras.Sequential([layers.BatchNormalization(input_shape=[5]),
                                  layers.Dense(512, activation='relu'), layers.BatchNormalization(),
                                  layers.Dense(512, activation='relu'), layers.BatchNormalization(),
                                  layers.Dense(512, activation='relu'), layers.BatchNormalization(), layers.Dense(1)])
    check(modules[5].Q3(), normalized, dropout_model(.3))
    binary = keras.Sequential([layers.BatchNormalization(input_shape=[5]),
                              layers.Dense(256, activation='relu'), layers.BatchNormalization(), layers.Dropout(.3),
                              layers.Dense(256, activation='relu'), layers.BatchNormalization(), layers.Dropout(.3),
                              layers.Dense(1, activation='sigmoid')])
    check(modules[6].Q1(), binary, normalized)
    binary.compile(optimizer='adam', loss='binary_crossentropy', metrics=['binary_accuracy'])
    wrong_metrics = keras.Sequential([layers.Dense(1, input_shape=[5])])
    wrong_metrics.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    check(modules[6].Q2(), binary, wrong_metrics)
    first = modules[1].Q2.check
    install()
    assert modules[1].Q2.check is first
    return {'tensorflow': tf.__version__, 'keras': getattr(keras, '__version__', 'unknown'),
            'assertions': assertions, 'training': 'not performed'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--keras', action='store_true', help='Require and check real TensorFlow/Keras')
    arguments = parser.parse_args()
    count = check_downloads()
    check_views()
    result = {'runtime_files': count, 'downloads_cache_integrity': 'passed',
              'downloaded_runtime_setup': 'passed',
              'metadata_adapter': 'passed', 'cloud_session': 'not_run',
              'tensorflow_checks': check_keras() if arguments.keras else 'not_run: use --keras in a TensorFlow environment'}
    (LAB/'reports/colab-checks.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
