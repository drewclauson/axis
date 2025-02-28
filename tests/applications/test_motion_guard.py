"""Test Axis Motion Guard API.

pytest --cov-report term-missing --cov=axis.applications.motion_guard tests/applications/test_motion_guard.py
"""

import json
import pytest

import respx

from axis.applications.motion_guard import MotionGuard

from ..conftest import HOST


@pytest.fixture
def motion_guard(axis_device) -> MotionGuard:
    """Returns the motion guard mock object."""
    return MotionGuard(axis_device.vapix.request)


@respx.mock
@pytest.mark.asyncio
async def test_get_empty_configuration(motion_guard):
    """Test empty get_configuration"""
    route = respx.post(f"http://{HOST}:80/local/motionguard/control.cgi").respond(
        json=response_get_configuration_empty,
    )
    await motion_guard.update()

    assert route.called
    assert route.calls.last.request.method == "POST"
    assert route.calls.last.request.url.path == "/local/motionguard/control.cgi"
    assert json.loads(route.calls.last.request.content) == {
        "method": "getConfiguration",
        "apiVersion": "1.3",
        "context": "Axis library",
    }

    assert len(motion_guard.values()) == 0


@respx.mock
@pytest.mark.asyncio
async def test_get_configuration(motion_guard):
    """Test get_configuration"""
    respx.post(f"http://{HOST}:80/local/motionguard/control.cgi").respond(
        json=response_get_configuration,
    )
    await motion_guard.update()

    assert len(motion_guard.values()) == 1

    profile1 = motion_guard["Camera1Profile1"]
    assert profile1.id == "Camera1Profile1"
    assert profile1.name == "Profile 1"
    assert profile1.camera == 1
    assert profile1.uid == 1
    assert profile1.filters == [
        {"active": True, "data": 1, "type": "timeShortLivedLimit"},
        {"active": True, "data": 5, "type": "distanceSwayingObject"},
        {"active": True, "data": [5, 5], "type": "sizePercentage"},
        {
            "type": "sizePerspective",
            "data": [75, 75],
            "active": False,
            "areHumansSelected": True,
        },
    ]
    assert profile1.perspective == [
        {"data": [[-0.7715, -0.1182], [-0.7715, 0.0824]], "height": 65, "type": "bar"},
        {"data": [[0.2833, -0.8853], [0.2833, 0.5287]], "height": 193, "type": "bar"},
    ]
    assert profile1.triggers == [
        {
            "data": [
                [-0.5544, -0.7951],
                [-0.4444, 0.288],
                [0.5767, 0.4835],
                [0.3933, -0.6547],
            ],
            "type": "includeArea",
        }
    ]


response_get_configuration_empty = {
    "data": {
        "cameras": [{"id": 1, "active": True, "rotation": 0}],
        "profiles": [],
        "configurationStatus": 9,
    },
    "apiVersion": "1.4",
    "method": "getConfiguration",
    "context": "Axis library",
}

response_get_configuration = {
    "data": {
        "cameras": [{"id": 1, "active": True, "rotation": 0}],
        "profiles": [
            {
                "filters": [
                    {"active": True, "data": 1, "type": "timeShortLivedLimit"},
                    {"active": True, "data": 5, "type": "distanceSwayingObject"},
                    {"active": True, "data": [5, 5], "type": "sizePercentage"},
                    {
                        "type": "sizePerspective",
                        "data": [75, 75],
                        "active": False,
                        "areHumansSelected": True,
                    },
                ],
                "triggers": [
                    {
                        "type": "includeArea",
                        "data": [
                            [-0.5544, -0.7951],
                            [-0.4444, 0.288],
                            [0.5767, 0.4835],
                            [0.3933, -0.6547],
                        ],
                    }
                ],
                "perspective": [
                    {
                        "type": "bar",
                        "data": [[-0.7715, -0.1182], [-0.7715, 0.0824]],
                        "height": 65,
                    },
                    {
                        "type": "bar",
                        "data": [[0.2833, -0.8853], [0.2833, 0.5287]],
                        "height": 193,
                    },
                ],
                "name": "Profile 1",
                "uid": 1,
                "camera": 1,
            }
        ],
        "configurationStatus": 8,
    },
    "apiVersion": "1.4",
    "method": "getConfiguration",
    "context": "Axis library",
}
