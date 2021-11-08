"""Entry for Dataflow."""

import argparse
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple
import pendulum
from pendulum.date import Date
import apache_beam as beam
from apache_beam import PCollection
from apache_beam.io.gcp.bigquery import (
    BigQueryDisposition,
    WriteToBigQuery,
)
from apache_beam.io.gcp.bigquery_tools import (
    parse_table_schema_from_json,
    RetryStrategy,
)
from apache_beam.options.pipeline_options import PipelineOptions

BQ_SCHEMA = parse_table_schema_from_json(
    """
    {"fields": [
        {"name": "word", "type": "STRING"},
        {"name": "count", "type": "INT64"}
    ]}
    """
)


@dataclass(frozen=True)
class Args:
    """Arguments for configuring Dataflow pipeline

    Attributes:
        date                 BigQuery table shard.
        input_file           Text file to read from.
        output_dataset       Output table dataset.
        output_table_prefix  Output table name prefix, table: `<output_table_prefix>_<datetime>`.
        project              Google Cloud project id.
    """

    date: Date
    input_file: str
    output_dataset: str
    output_table_prefix: str
    project: str


def run(argv: Optional[Sequence[str]] = None):
    """Create and run pipeline with provided cmd arguments."""
    args, pipeline_args = parse_args(argv)

    with beam.Pipeline(options=PipelineOptions(pipeline_args)) as p:
        text_rows = p | "ReadText" >> beam.io.ReadFromText(args.input_file)
        word_count = pipeline(text_rows=text_rows)
        word_count | "WriteToBQ" >> WriteToBigQuery(
            f"{args.output_table_prefix}_{args.date.strftime('%Y%m%d')}",
            dataset="dataflow",
            project=args.project,
            insert_retry_strategy=RetryStrategy.RETRY_NEVER,
            create_disposition=BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=BigQueryDisposition.WRITE_TRUNCATE,
            schema=BQ_SCHEMA,
        )


def pipeline(*, text_rows: PCollection[str]) -> PCollection[Dict[str, Any]]:
    """Count occurencies of words."""
    return (
        text_rows
        | "RowToWords" >> beam.FlatMap(lambda row: row.split(" "))
        | "CountWords" >> beam.combiners.Count.PerElement()
        | "TupleToDict"
        >> beam.MapTuple(lambda word, count: {"word": word, "count": count})
    )


def parse_args(
    argv: Optional[Sequence[str]] = None,
) -> Tuple[Args, List[str]]:
    """Parses command line arguments and asserts required values."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--stoix_scheduled", dest="stoix_scheduled", required=True)
    parser.add_argument("--input_file", dest="input_file", required=True)
    parser.add_argument("--output_dataset", dest="output_dataset", required=True)
    parser.add_argument(
        "--output_table_prefix", dest="output_table_prefix", required=True
    )
    parser.add_argument("--project", dest="project", required=True)
    args, pipeline_args = parser.parse_known_args(argv)
    pipeline_args.append("--project")
    pipeline_args.append(args.project)
    return (
        Args(
            date=pendulum.parse(args.stoix_scheduled),
            input_file=args.input_file,
            output_dataset=args.output_dataset,
            output_table_prefix=args.output_table_prefix,
            project=args.project,
        ),
        pipeline_args,
    )


if __name__ == "__main__":
    run()
