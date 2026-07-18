import os
import sys
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from advanced_timer import main, parse_time


def test_parse_time_valid():
    # Relative time parsing
    t = parse_time("in 2 hours")
    assert t is not None
    now = datetime.now()
    # Check that t is approximately now + 2 hours
    diff = t - now
    assert 7100 < diff.total_seconds() < 7300


def test_parse_time_invalid():
    assert parse_time("invalid time string") is None


@patch("advanced_timer.parse_time")
@patch("advanced_timer.datetime")
@patch("time.sleep")
@patch("sys.exit", side_effect=SystemExit)
@patch("sys.argv")
def test_main_cli_success(mock_argv, mock_exit, mock_sleep, mock_datetime, mock_parse_time):
    # Setup mocks
    mock_argv.__getitem__.side_effect = lambda x: [
        "advanced-timer",
        "--time",
        "in 5 seconds",
        "--message",
        "Wake up!",
    ][x]
    mock_argv.__len__.return_value = 5

    now = datetime(2026, 7, 18, 12, 0, 0)
    target = datetime(2026, 7, 18, 12, 0, 5)

    # Mock datetime.now()
    mock_datetime.now.return_value = now
    mock_parse_time.return_value = target

    # Run main CLI with parsed args mock
    with patch("argparse.ArgumentParser.parse_args") as mock_args:
        mock_args.return_value = MagicMock(time="in 5 seconds", message="Wake up!")
        main()

    # Verify sleep was called for ~5 seconds
    mock_sleep.assert_called_once_with(5.0)
    mock_exit.assert_not_called()


@patch("argparse.ArgumentParser.parse_args")
@patch("advanced_timer.parse_time", return_value=None)
@patch("sys.exit", side_effect=SystemExit)
def test_main_cli_parse_error(mock_exit, mock_parse_time, mock_args):
    mock_args.return_value = MagicMock(time="invalid", message="Wake up!")

    with pytest.raises(SystemExit):
        main()

    mock_exit.assert_called_once_with(1)


@patch("argparse.ArgumentParser.parse_args")
@patch("advanced_timer.parse_time")
@patch("sys.exit", side_effect=SystemExit)
def test_main_cli_past_error(mock_exit, mock_parse_time, mock_args):
    # Target time in the past
    past_time = datetime.now() - timedelta(hours=1)
    mock_parse_time.return_value = past_time
    mock_args.return_value = MagicMock(time="1 hour ago", message="Wake up!")

    with pytest.raises(SystemExit):
        main()

    mock_exit.assert_called_once_with(1)
