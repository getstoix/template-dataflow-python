# Dataflow Flex Template in Python

This repository contains a template for a Dataflow Flex Template written in Python that can easily be used to build Dataflow jobs to run in [STOIX](https://getstoix.com/) using [Dataflow runner](https://hub.docker.com/r/stoix/dataflow-runner/).

The code is based on the same example data as [Google Cloud Python Quickstart](https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python/), "King Lear" which is a tragedy written by William Shakespeare.

The Dataflow job reads the file content, count occurencies of each word and inserts it to a BigQuery table. The schedule date is also added to the table name producing a sharded table for the output.

Source data:

* https://storage.cloud.google.com/dataflow-samples/shakespeare/kinglear.txt
* gs://dataflow-samples/shakespeare/kinglear.txt

Template maintained by [STOIX](https://getstoix.com/).

## Configuration

The job is configured with the following pipeline options:

* `stoix_scheduled` - Scheduled datetime as RFC3339
* `input_file` - Text to read
* `output_dataset` - BigQuery dataset for output table
* `output_table_prefix` - BigQuery output table name prefix
* `project` - Google Cloud project id

When using [Dataflow runner](https://hub.docker.com/r/stoix/dataflow-runner/), `stoix_scheduled` is automatically set and other pipeline options can be added as described in the [Dataflow runner](https://hub.docker.com/r/stoix/dataflow-runner/) README.

## Test the code

[Tox](https://tox.wiki/en/latest/index.html) is used to format, test and lint the code. Make sure to install it with `pip install tox` and then just run `tox` within the project folder.

## Run pipeline

In order to work with the code locally, you can use Python virtual environments. Make sure to use Python version `3.7.10` as it is the version supported by Google Dataflow.

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -e .
```

**Run on local machine**

See [quickstart python](https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python#run-the-pipeline-on-the-dataflow-service) for further description of arguments.

```
python -m main \
    --region europe-north1 \
    --runner DirectRunner \
    --stoix_scheduled 2021-01-01T00:00:00Z \
    --input_file gs://dataflow-samples/shakespeare/kinglear.txt \
    --output_table_prefix kinglear \
    --output_dataset <DATASET> \
    --project <PROJECT ID> \
    --temp_location gs://<BUCKET>/tmp/
```

## Build Docker image for STOIX

In order to run the pipeline the Flex Template needs to be packaged in a Docker image and pushed to a Docker image repository. In this example Docker Hub is used.

Set the tag to the name and version of your pipeline, e.g: `stoix/count-words:1.0.0`.

```
$ docker build --tag stoix/count-words:1.0.0 .
```

Then upload the image to the Docker image repository.

```
$ docker push stoix/count-words:1.0.0
```

## Run Dataflow on STOIX

Now the Dataflow Flex Template job can be ran using [Dataflow runner](https://hub.docker.com/r/stoix/dataflow-runner/). Add a new job with the image `stoix/dataflow-runner` and the following environment variables:

* GCP_PROJECT_ID: `<PROJECT ID>`
* GCP_REGION: europe-north1
* GCP_SERVICE_ACCOUNT: `BASE64 encoded service account JSON`
* JOB_IMAGE: stoix/count-words:1.0.0
* JOB_NAME_PREFIX: count-words
* JOB_PARAM_INPUT_FILE: gs://dataflow-samples/shakespeare/kinglear.txt
* JOB_PARAM_OUTPUT_DATASET: dataflow
* JOB_PARAM_OUTPUT_TABLE_PREFIX: kinglear
* JOB_SDK_LANGUAGE: python

Note: When running this in production, set `GCP_SERVICE_ACCOUNT` as a secret instead of environment variable.

## License

[MIT](./LICENSE)
