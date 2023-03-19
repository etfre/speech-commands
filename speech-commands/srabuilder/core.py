
import os.path
import os
import threading
import time
import logging
import sys
from io import BytesIO
from zipfile import ZipFile
import urllib.request
from pathlib import Path
import shutil

from dragonfly import RecognitionObserver, get_engine
from dragonfly.log import setup_log
from srabuilder import sleep, environment

MODELS_DIR = os.path.join(str(Path.home()), '.srabuilder', 'models')

# --------------------------------------------------------------------------
# Set up basic logging.

if False:
    # Debugging logging for reporting trouble
    logging.basicConfig(level=10)
    logging.getLogger("grammar.decode").setLevel(20)
    logging.getLogger("grammar.begin").setLevel(20)
    logging.getLogger("compound").setLevel(20)
    logging.getLogger("kaldi.compiler").setLevel(10)
else:
    setup_log()

def download_model(write_dir: str):
    model_url = 'https://github.com/daanzu/kaldi-active-grammar/releases/download/v1.8.0/kaldi_model_daanzu_20200905_1ep-biglm.zip'
    print(f'Downloading speech recognition model from {model_url}, this may take a few minutes...')
    url_open = urllib.request.urlopen(model_url)
    with ZipFile(BytesIO(url_open.read())) as my_zip_file:
        my_zip_file.extractall(write_dir)
    print('Done!')

def setup_engine(silence_timeout=500, models_dir=MODELS_DIR, expected_error_rate_threshold=0.05, lexicon_path=None):
    # use abspath for model dir, this may change with app freezing
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(models_dir, "kaldi_model")
    if not os.path.isdir(model_dir):
        download_model(models_dir)
    if lexicon_path is not None:
        dst = os.path.join(model_dir, "user_lexicon.txt")
        shutil.copyfile(lexicon_path, dst)
    # Set any configuration options here as keyword arguments.
    engine = get_engine(
        "kaldi",
        model_dir=model_dir,
        expected_error_rate_threshold=expected_error_rate_threshold,
        # tmp_dir='kaldi_tmp',  # default for temporary directory
        # vad_aggressiveness=3,  # default aggressiveness of VAD
        vad_padding_start_ms=0,  # default ms of required silence surrounding VAD
        vad_padding_end_ms=silence_timeout,  # default ms of required silence surrounding VAD
    )
    # Call connect() now that the engine configuration is set.
    engine.connect()
    return engine

def load_environment_grammars(map_contexts_to_builder):
    envs = environment.load_environments(map_contexts_to_builder)
    environment.load_grammars(envs)

def run_engine():
    engine = get_engine()
    engine.prepare_for_recognition()
    try:
        print("Listening...")
        engine.do_recognition()
    except KeyboardInterrupt:
        pass