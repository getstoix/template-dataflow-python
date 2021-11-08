"""Test pipeline module."""

from unittest import TestCase
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline as Pipeline
from apache_beam.testing.util import assert_that, is_empty, equal_to
from main import pipeline


class TestPipeline(TestCase):
    """Test pipeline method."""

    def test_pipeline_empty(self):
        """Given no rows it should return empty list."""
        with Pipeline() as p:
            text_rows = p | beam.Create([])
            word_count = pipeline(text_rows=text_rows)
            assert_that(word_count, is_empty())

    def test_pipeline_words(self):
        """Given rows it should return word count."""
        with Pipeline() as p:
            text_rows = p | beam.Create(["a b c", "b c", "c"])
            word_count = pipeline(text_rows=text_rows)
            assert_that(
                word_count,
                equal_to(
                    [
                        {"word": "a", "count": 1},
                        {"word": "b", "count": 2},
                        {"word": "c", "count": 3},
                    ]
                ),
            )
