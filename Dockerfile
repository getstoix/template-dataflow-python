FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

WORKDIR /dataflow/template

COPY setup.py .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install -e /dataflow/template
# Indicate that we already have pre-installed the dependencies to speed up runtime.
ENV PIP_NO_DEPS=True

COPY . .

# Required by flex template
# https://cloud.google.com/dataflow/docs/guides/templates/configuring-flex-templates#setting_required_dockerfile_environment_variables
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="/dataflow/template/main.py"
ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="/dataflow/template/setup.py"
