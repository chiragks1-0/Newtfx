import os
from tfx.components import CsvExampleGen, StatisticsGen, SchemaGen, ExampleValidator, Transform, Trainer, Evaluator, Pusher
from tfx.proto import trainer_pb2, pusher_pb2
from tfx.orchestration import pipeline
from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner
from tfx.orchestration.metadata import sqlite_metadata_connection_config

def create_pipeline(pipeline_name, pipeline_root, data_root, module_file, metadata_path):
    # CSV ExampleGen
    example_gen = CsvExampleGen(input_base=data_root)
    
    # StatisticsGen
    statistics_gen = StatisticsGen(examples=example_gen.outputs['examples'])
    
    # SchemaGen
    schema_gen = SchemaGen(statistics=statistics_gen.outputs['statistics'])
    
    # ExampleValidator
    example_validator = ExampleValidator(
        statistics=statistics_gen.outputs['statistics'],
        schema=schema_gen.outputs['schema']
    )
    
    # Transform
    transform = Transform(
        examples=example_gen.outputs['examples'],
        schema=schema_gen.outputs['schema'],
        module_file=module_file
    )
    
    # Trainer
    trainer = Trainer(
        module_file=module_file,
        examples=transform.outputs['transformed_examples'],
        transform_graph=transform.outputs['transform_graph'],
        schema=schema_gen.outputs['schema'],
        train_args=trainer_pb2.TrainArgs(num_steps=200),
        eval_args=trainer_pb2.EvalArgs(num_steps=50)
    )
    
    # Evaluator
    evaluator = Evaluator(
        examples=example_gen.outputs['examples'],
        model=trainer.outputs['model']
    )
    
    # Pusher
    pusher = Pusher(
        model=trainer.outputs['model'],
        push_destination=pusher_pb2.PushDestination(
            filesystem=pusher_pb2.PushDestination.Filesystem(
                base_directory=os.path.join(pipeline_root, 'serving_model')
            )
        )
    )
    
    return pipeline.Pipeline(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        metadata_connection_config=sqlite_metadata_connection_config(metadata_path),
        components=[
            example_gen, statistics_gen, schema_gen, example_validator,
            transform, trainer, evaluator, pusher
        ]
    )