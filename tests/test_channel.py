import pytest
import src.channel


@pytest.fixture
def channel_instance():
    return src.channel.Channel('UCdOUvNFp8y6KTkswzeu7naQ')


def test_print_info(channel_instance):
    assert channel_instance.print_info() is None
