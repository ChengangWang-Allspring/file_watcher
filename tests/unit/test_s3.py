import pytest

from file_watch.common import s3_helper


@pytest.mark.s3_test
@pytest.mark.parametrize(
    'txt_input, expected',
    [
        ('s3://mybucket/mypath/', ['mybucket', 'mypath/']),
        ('s3://another_bucket/test/inbound/', ['another_bucket', 'test/inbound/']),
    ],
)
def test_get_s3_bucket_prefix_by_uri(txt_input, expected):
    assert s3_helper.get_s3_bucket_prefix_by_uri(txt_input) == expected
