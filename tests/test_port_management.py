"""Test Axis I/O port management API.

pytest --cov-report term-missing --cov=axis.port_management tests/test_port_management.py
"""

import json
import pytest

import respx

from axis.port_management import (
    IoPortManagement,
    PortSequence,
    Sequence,
    SetPort,
)

from .conftest import HOST


@pytest.fixture
def io_port_management(axis_device) -> IoPortManagement:
    """Returns the io_port_management mock object."""
    return IoPortManagement(axis_device.vapix.request)


@respx.mock
@pytest.mark.asyncio
async def test_get_ports(io_port_management):
    """Test get_ports call."""
    route = respx.post(f"http://{HOST}:80/axis-cgi/io/portmanagement.cgi").respond(
        json=response_getPorts,
    )

    await io_port_management.update()

    assert route.called
    assert route.calls.last.request.method == "POST"
    assert route.calls.last.request.url.path == "/axis-cgi/io/portmanagement.cgi"
    assert json.loads(route.calls.last.request.content) == {
        "apiVersion": "1.0",
        "context": "Axis library",
        "method": "getPorts",
    }

    assert len(io_port_management.values()) == 1

    item = io_port_management["0"]
    assert item.id == "0"
    assert item.port == "0"
    assert item.name == "PIR sensor"
    assert item.configurable is False
    assert item.usage == ""
    assert item.direction == "input"
    assert item.state == "open"
    assert item.normalState == "open"

    await item.open()

    assert route.called
    assert route.calls.last.request.method == "POST"
    assert route.calls.last.request.url.path == "/axis-cgi/io/portmanagement.cgi"
    assert json.loads(route.calls.last.request.content) == {
        "method": "setPorts",
        "apiVersion": "1.0",
        "context": "Axis library",
        "params": [{"port": "0", "state": "open"}],
    }

    await item.close()

    assert route.called
    assert route.calls.last.request.method == "POST"
    assert route.calls.last.request.url.path == "/axis-cgi/io/portmanagement.cgi"
    assert json.loads(route.calls.last.request.content) == {
        "method": "setPorts",
        "apiVersion": "1.0",
        "context": "Axis library",
        "params": [{"port": "0", "state": "closed"}],
    }


@respx.mock
@pytest.mark.asyncio
async def test_set_ports(io_port_management):
    """Test set_ports call."""
    route = respx.post(f"http://{HOST}:80/axis-cgi/io/portmanagement.cgi")

    await io_port_management.set_ports([SetPort("0", state="closed")])

    assert route.called
    assert route.calls.last.request.method == "POST"
    assert route.calls.last.request.url.path == "/axis-cgi/io/portmanagement.cgi"
    assert json.loads(route.calls.last.request.content) == {
        "method": "setPorts",
        "apiVersion": "1.0",
        "context": "Axis library",
        "params": [{"port": "0", "state": "closed"}],
    }


@respx.mock
@pytest.mark.asyncio
async def test_set_state_sequence(io_port_management):
    """Test setting state sequence call."""
    route = respx.post(f"http://{HOST}:80/axis-cgi/io/portmanagement.cgi")

    await io_port_management.set_state_sequence(
        PortSequence("0", [Sequence("open", 3000), Sequence("closed", 5000)])
    )

    assert route.called
    assert route.calls.last.request.method == "POST"
    assert route.calls.last.request.url.path == "/axis-cgi/io/portmanagement.cgi"
    assert json.loads(route.calls.last.request.content) == {
        "method": "setStateSequence",
        "apiVersion": "1.0",
        "context": "Axis library",
        "params": {
            "port": "0",
            "sequence": [
                {"state": "open", "time": 3000},
                {"state": "closed", "time": 5000},
            ],
        },
    }


@respx.mock
@pytest.mark.asyncio
async def test_get_supported_versions(io_port_management):
    """Test get_supported_versions."""
    route = respx.post(f"http://{HOST}:80/axis-cgi/io/portmanagement.cgi").respond(
        json=response_getSupportedVersions,
    )

    response = await io_port_management.get_supported_versions()

    assert route.called
    assert route.calls.last.request.method == "POST"
    assert route.calls.last.request.url.path == "/axis-cgi/io/portmanagement.cgi"
    assert json.loads(route.calls.last.request.content) == {
        "method": "getSupportedVersions"
    }
    assert response["data"] == {"apiVersions": ["1.0"]}


response_getPorts = {
    "apiVersion": "1.0",
    "context": "Retrieve all properties of available ports",
    "method": "getPorts",
    "data": {
        "numberOfPorts": 1,
        "items": [
            {
                "port": "0",
                "configurable": False,
                "usage": "",
                "name": "PIR sensor",
                "direction": "input",
                "state": "open",
                "normalState": "open",
            }
        ],
    },
}

response_getSupportedVersions = {
    "method": "getSupportedVersions",
    "data": {"apiVersions": ["1.0"]},
}
