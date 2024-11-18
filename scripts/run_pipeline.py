import os
from pipeline import create_pipeline
from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner

PIPELINE_NAME = 'house_price_pipeline'
PIPELINE_ROOT = os.path.join(os.getcwd(), 'pipeline_output')
DATA_ROOT = os.path.join(os.getcwd(), 'data')
MODULE_FILE = os.path.join(os.getcwd(), 'preprocessing.py')
METADATA_PATH = os.path.join(os.getcwd(), 'metadata.db')

pipeline = create_pipeline(
    pipeline_name=PIPELINE_NAME,
    pipeline_root=PIPELINE_ROOT,
    data_root=DATA_ROOT,
    module_file=MODULE_FILE,
    metadata_path=METADATA_PATH
)

BeamDagRunner().run(pipeline)
