"""Test Axis parameter management.

pytest --cov-report term-missing --cov=axis.param_cgi tests/test_param_cgi.py
"""

import pytest

import respx

from axis.param_cgi import Params

from .conftest import HOST


@pytest.fixture
def params(axis_device) -> Params:
    """Returns the param cgi mock object."""
    return Params(axis_device.vapix.request)


@respx.mock
@pytest.mark.asyncio
async def test_params(params):
    """Verify that you can list parameters."""
    route = respx.get(f"http://{HOST}:80/axis-cgi/param.cgi?action=list").respond(
        text=response_param_cgi,
        headers={"Content-Type": "text/plain"},
    )
    await params.update()

    assert route.called
    assert route.calls.last.request.method == "GET"
    assert route.calls.last.request.url.path == "/axis-cgi/param.cgi"

    # Brand
    assert params.brand == "AXIS"
    assert params.prodfullname == "AXIS M1065-LW Network Camera"
    assert params.prodnbr == "M1065-LW"
    assert params.prodshortname == "AXIS M1065-LW"
    assert params.prodtype == "Network Camera"
    assert params.prodvariant == ""
    assert params.weburl == "http://www.axis.com"

    # Image
    assert params.image_sources == {
        0: {
            "Enabled": True,
            "Name": "View Area 1",
            "Source": 0,
            "Appearance.ColorEnabled": True,
            "Appearance.Compression": 30,
            "Appearance.MirrorEnabled": False,
            "Appearance.Resolution": "1920x1080",
            "Appearance.Rotation": 0,
            "MPEG.Complexity": 50,
            "MPEG.ConfigHeaderInterval": 1,
            "MPEG.FrameSkipMode": "drop",
            "MPEG.ICount": 1,
            "MPEG.PCount": 31,
            "MPEG.UserDataEnabled": False,
            "MPEG.UserDataInterval": 1,
            "MPEG.ZChromaQPMode": "off",
            "MPEG.ZFpsMode": "fixed",
            "MPEG.ZGopMode": "fixed",
            "MPEG.ZMaxGopLength": 300,
            "MPEG.ZMinFps": 0,
            "MPEG.ZStrength": 10,
            "MPEG.H264.Profile": "high",
            "MPEG.H264.PSEnabled": False,
            "Overlay.Enabled": False,
            "Overlay.XPos": 0,
            "Overlay.YPos": 0,
            "Overlay.MaskWindows.Color": "black",
            "RateControl.MaxBitrate": 0,
            "RateControl.Mode": "vbr",
            "RateControl.Priority": "framerate",
            "RateControl.TargetBitrate": 0,
            "SizeControl.MaxFrameSize": 0,
            "Stream.Duration": 0,
            "Stream.FPS": 0,
            "Stream.NbrOfFrames": 0,
            "Text.BGColor": "black",
            "Text.ClockEnabled": False,
            "Text.Color": "white",
            "Text.DateEnabled": False,
            "Text.Position": "top",
            "Text.String": "",
            "Text.TextEnabled": False,
            "Text.TextSize": "medium",
        },
        1: {
            "Enabled": False,
            "Name": "View Area 2",
            "Source": 0,
            "Appearance.ColorEnabled": True,
            "Appearance.Compression": 30,
            "Appearance.MirrorEnabled": False,
            "Appearance.Resolution": "1920x1080",
            "Appearance.Rotation": 0,
            "MPEG.Complexity": 50,
            "MPEG.ConfigHeaderInterval": 1,
            "MPEG.FrameSkipMode": "drop",
            "MPEG.ICount": 1,
            "MPEG.PCount": 31,
            "MPEG.UserDataEnabled": False,
            "MPEG.UserDataInterval": 1,
            "MPEG.ZChromaQPMode": "off",
            "MPEG.ZFpsMode": "fixed",
            "MPEG.ZGopMode": "fixed",
            "MPEG.ZMaxGopLength": 300,
            "MPEG.ZMinFps": 0,
            "MPEG.ZStrength": 10,
            "MPEG.H264.Profile": "high",
            "MPEG.H264.PSEnabled": False,
            "Overlay.Enabled": False,
            "Overlay.XPos": 0,
            "Overlay.YPos": 0,
            "RateControl.MaxBitrate": 0,
            "RateControl.Mode": "vbr",
            "RateControl.Priority": "framerate",
            "RateControl.TargetBitrate": 0,
            "SizeControl.MaxFrameSize": 0,
            "Stream.Duration": 0,
            "Stream.FPS": 0,
            "Stream.NbrOfFrames": 0,
            "Text.BGColor": "black",
            "Text.ClockEnabled": False,
            "Text.Color": "white",
            "Text.DateEnabled": False,
            "Text.Position": "top",
            "Text.String": "",
            "Text.TextEnabled": False,
            "Text.TextSize": "medium",
        },
    }

    # Ports
    assert params.nbrofinput == 1
    assert params.nbrofoutput == 0
    assert params.ports == {
        0: {
            "Configurable": False,
            "Direction": "input",
            "Input.Name": "PIR sensor",
            "Input.Trig": "closed",
        }
    }

    # Properties
    assert params.api_http_version == "3"
    assert params.api_metadata == "yes"
    assert params.api_metadata_version == "1.0"
    assert params.api_ptz_presets_version == "2.00"
    assert params.embedded_development == "2.16"
    assert params.firmware_builddate == "Feb 15 2019 09:42"
    assert params.firmware_buildnumber == "26"
    assert params.firmware_version == "9.10.1"
    assert params.image_format == "jpeg,mjpeg,h264"
    assert params.image_nbrofviews == 2
    assert (
        params.image_resolution
        == "1920x1080,1280x960,1280x720,1024x768,1024x576,800x600,640x480,640x360,352x240,320x240"
    )
    assert params.image_rotation == "0,180"
    assert params.light_control is True
    assert params.ptz is True
    assert params.digital_ptz is True
    assert params.system_serialnumber == "ACCC12345678"


@pytest.mark.asyncio
async def test_params_empty_raw(params):
    """Verify that params can take an empty raw on creation."""
    assert len(params) == 0

    assert params.image_sources == {}


@respx.mock
@pytest.mark.asyncio
async def test_update_brand(params):
    """Verify that update brand works."""
    route = respx.get(
        f"http://{HOST}:80/axis-cgi/param.cgi?action=list&group=root.Brand"
    ).respond(
        text=response_param_cgi_brand,
        headers={"Content-Type": "text/plain"},
    )
    await params.update_brand()

    assert route.called
    assert route.calls.last.request.method == "GET"
    assert route.calls.last.request.url.path == "/axis-cgi/param.cgi"

    assert params.brand == "AXIS"
    assert params.prodfullname == "AXIS M1065-LW Network Camera"
    assert params.prodnbr == "M1065-LW"
    assert params.prodshortname == "AXIS M1065-LW"
    assert params.prodtype == "Network Camera"
    assert params.prodvariant == ""
    assert params.weburl == "http://www.axis.com"


@respx.mock
@pytest.mark.asyncio
async def test_update_image(params):
    """Verify that update brand works."""
    route = respx.get(
        f"http://{HOST}:80/axis-cgi/param.cgi?action=list&group=root.Image"
    ).respond(
        text=response_param_cgi,
        headers={"Content-Type": "text/plain"},
    )
    await params.update_image()

    assert route.called
    assert route.calls.last.request.method == "GET"
    assert route.calls.last.request.url.path == "/axis-cgi/param.cgi"

    assert params.image_nbrofviews == 2
    assert params.image_sources == {
        0: {
            "Enabled": True,
            "Name": "View Area 1",
            "Source": 0,
            "Appearance.ColorEnabled": True,
            "Appearance.Compression": 30,
            "Appearance.MirrorEnabled": False,
            "Appearance.Resolution": "1920x1080",
            "Appearance.Rotation": 0,
            "MPEG.Complexity": 50,
            "MPEG.ConfigHeaderInterval": 1,
            "MPEG.FrameSkipMode": "drop",
            "MPEG.ICount": 1,
            "MPEG.PCount": 31,
            "MPEG.UserDataEnabled": False,
            "MPEG.UserDataInterval": 1,
            "MPEG.ZChromaQPMode": "off",
            "MPEG.ZFpsMode": "fixed",
            "MPEG.ZGopMode": "fixed",
            "MPEG.ZMaxGopLength": 300,
            "MPEG.ZMinFps": 0,
            "MPEG.ZStrength": 10,
            "MPEG.H264.Profile": "high",
            "MPEG.H264.PSEnabled": False,
            "Overlay.Enabled": False,
            "Overlay.XPos": 0,
            "Overlay.YPos": 0,
            "Overlay.MaskWindows.Color": "black",
            "RateControl.MaxBitrate": 0,
            "RateControl.Mode": "vbr",
            "RateControl.Priority": "framerate",
            "RateControl.TargetBitrate": 0,
            "SizeControl.MaxFrameSize": 0,
            "Stream.Duration": 0,
            "Stream.FPS": 0,
            "Stream.NbrOfFrames": 0,
            "Text.BGColor": "black",
            "Text.ClockEnabled": False,
            "Text.Color": "white",
            "Text.DateEnabled": False,
            "Text.Position": "top",
            "Text.String": "",
            "Text.TextEnabled": False,
            "Text.TextSize": "medium",
        },
        1: {
            "Enabled": False,
            "Name": "View Area 2",
            "Source": 0,
            "Appearance.ColorEnabled": True,
            "Appearance.Compression": 30,
            "Appearance.MirrorEnabled": False,
            "Appearance.Resolution": "1920x1080",
            "Appearance.Rotation": 0,
            "MPEG.Complexity": 50,
            "MPEG.ConfigHeaderInterval": 1,
            "MPEG.FrameSkipMode": "drop",
            "MPEG.ICount": 1,
            "MPEG.PCount": 31,
            "MPEG.UserDataEnabled": False,
            "MPEG.UserDataInterval": 1,
            "MPEG.ZChromaQPMode": "off",
            "MPEG.ZFpsMode": "fixed",
            "MPEG.ZGopMode": "fixed",
            "MPEG.ZMaxGopLength": 300,
            "MPEG.ZMinFps": 0,
            "MPEG.ZStrength": 10,
            "MPEG.H264.Profile": "high",
            "MPEG.H264.PSEnabled": False,
            "Overlay.Enabled": False,
            "Overlay.XPos": 0,
            "Overlay.YPos": 0,
            "RateControl.MaxBitrate": 0,
            "RateControl.Mode": "vbr",
            "RateControl.Priority": "framerate",
            "RateControl.TargetBitrate": 0,
            "SizeControl.MaxFrameSize": 0,
            "Stream.Duration": 0,
            "Stream.FPS": 0,
            "Stream.NbrOfFrames": 0,
            "Text.BGColor": "black",
            "Text.ClockEnabled": False,
            "Text.Color": "white",
            "Text.DateEnabled": False,
            "Text.Position": "top",
            "Text.String": "",
            "Text.TextEnabled": False,
            "Text.TextSize": "medium",
        },
    }


@respx.mock
@pytest.mark.asyncio
async def test_update_ports(params):
    """Verify that update brand works."""
    input_route = respx.get(
        f"http://{HOST}:80/axis-cgi/param.cgi?action=list&group=root.Input"
    ).respond(
        text="root.Input.NbrOfInputs=1",
        headers={"Content-Type": "text/plain"},
    )
    io_port_route = respx.get(
        f"http://{HOST}:80/axis-cgi/param.cgi?action=list&group=root.IOPort"
    ).respond(
        text="""root.IOPort.I0.Configurable=no
root.IOPort.I0.Direction=input
root.IOPort.I0.Input.Name=PIR sensor
root.IOPort.I0.Input.Trig=closed
""",
        headers={"Content-Type": "text/plain"},
    )
    output_route = respx.get(
        f"http://{HOST}:80/axis-cgi/param.cgi?action=list&group=root.Output"
    ).respond(
        text="root.Output.NbrOfOutputs=0",
        headers={"Content-Type": "text/plain"},
    )

    await params.update_ports()

    assert input_route.called
    assert input_route.calls.last.request.method == "GET"
    assert input_route.calls.last.request.url.path == "/axis-cgi/param.cgi"

    assert io_port_route.called
    assert io_port_route.calls.last.request.method == "GET"
    assert io_port_route.calls.last.request.url.path == "/axis-cgi/param.cgi"

    assert output_route.called
    assert output_route.calls.last.request.method == "GET"
    assert output_route.calls.last.request.url.path == "/axis-cgi/param.cgi"

    assert params.nbrofinput == 1
    assert params.ports == {
        0: {
            "Configurable": False,
            "Direction": "input",
            "Input.Name": "PIR sensor",
            "Input.Trig": "closed",
        }
    }
    assert params.nbrofoutput == 0


@respx.mock
@pytest.mark.asyncio
async def test_update_properties(params):
    """Verify that update properties works."""
    route = respx.get(
        f"http://{HOST}:80/axis-cgi/param.cgi?action=list&group=root.Properties"
    ).respond(
        text=response_param_cgi_properties,
        headers={"Content-Type": "text/plain"},
    )

    await params.update_properties()

    assert route.called
    assert route.calls.last.request.method == "GET"
    assert route.calls.last.request.url.path == "/axis-cgi/param.cgi"

    assert params.api_http_version == "3"
    assert params.api_metadata == "yes"
    assert params.api_metadata_version == "1.0"
    # assert params[f"{PROPERTIES}.API.OnScreenControls.OnScreenControls"] == "yes"
    assert params.api_ptz_presets_version == "2.00"
    # assert params[f"{PROPERTIES}.API.RTSP.RTSPAuth"] == "yes"
    # assert params[f"{PROPERTIES}.API.RTSP.Version"] == "2.01"
    # assert params[f"{PROPERTIES}.ApiDiscovery.ApiDiscovery"] == "yes"
    # assert params[f"{PROPERTIES}.EmbeddedDevelopment.EmbeddedDevelopment"] == "yes"
    assert params.embedded_development == "2.16"
    assert params.firmware_builddate == "Feb 15 2019 09:42"
    assert params.firmware_buildnumber == "26"
    assert params.firmware_version == "9.10.1"
    assert params.image_format == "jpeg,mjpeg,h264"
    assert params.image_nbrofviews == 2
    assert (
        params.image_resolution
        == "1920x1080,1280x960,1280x720,1024x768,1024x576,800x600,640x480,640x360,352x240,320x240"
    )
    assert params.image_rotation == "0,180"
    # assert params[f"{PROPERTIES}.LEDControl.LEDControl"] == "yes"
    assert params.light_control is True
    # assert params[f"{PROPERTIES}.LightControl.LightControlAvailable"] == "yes"
    # assert params[f"{PROPERTIES}.LocalStorage.AutoRepair"] == "yes"
    # assert params[f"{PROPERTIES}.LocalStorage.ContinuousRecording"] == "yes"
    # assert params[f"{PROPERTIES}.LocalStorage.DiskEncryption"] == "yes"
    # assert params[f"{PROPERTIES}.LocalStorage.DiskHealth"] == "yes"
    # assert params[f"{PROPERTIES}.LocalStorage.ExportRecording"] == "yes"
    # assert params[f"{PROPERTIES}.LocalStorage.FailOverRecording"] == "yes"
    # assert params[f"{PROPERTIES}.LocalStorage.LocalStorage"] == "yes"
    # assert params[f"{PROPERTIES}.LocalStorage.NbrOfContinuousRecordingProfiles"] == "1"
    # assert params[f"{PROPERTIES}.LocalStorage.RequiredFileSystem"] == "yes"
    # assert params[f"{PROPERTIES}.LocalStorage.SDCard"] == "yes"
    # assert params[f"{PROPERTIES}.LocalStorage.StorageLimit"] == "yes"
    # assert params[f"{PROPERTIES}.LocalStorage.Version"] == "1.00"
    assert params.digital_ptz is True
    assert params.ptz is True
    # assert params[f"{PROPERTIES}.Sensor.PIR"] == "yes"
    assert params.system_serialnumber == "ACCC12345678"


@respx.mock
@pytest.mark.asyncio
async def test_update_ptz(params):
    """Verify that update ptz works."""
    route = respx.get(
        f"http://{HOST}:80/axis-cgi/param.cgi?action=list&group=root.PTZ"
    ).respond(
        text=response_param_cgi_ptz,
        headers={"Content-Type": "text/plain"},
    )

    await params.update_ptz()

    assert route.called
    assert route.calls.last.request.method == "GET"
    assert route.calls.last.request.url.path == "/axis-cgi/param.cgi"

    assert params.ptz_camera_default == 1
    assert params.ptz_number_of_cameras == 1
    assert params.ptz_number_of_serial_ports == 1
    assert params.ptz_limits == {
        1: {
            "MaxBrightness": 9999,
            "MaxFieldAngle": 623,
            "MaxFocus": 9999,
            "MaxIris": 9999,
            "MaxPan": 170,
            "MaxTilt": 90,
            "MaxZoom": 9999,
            "MinBrightness": 1,
            "MinFieldAngle": 22,
            "MinFocus": 770,
            "MinIris": 1,
            "MinPan": -170,
            "MinTilt": -20,
            "MinZoom": 1,
        }
    }
    assert params.ptz_support == {
        1: {
            "AbsoluteBrightness": True,
            "AbsoluteFocus": True,
            "AbsoluteIris": True,
            "AbsolutePan": True,
            "AbsoluteTilt": True,
            "AbsoluteZoom": True,
            "ActionNotification": True,
            "AreaZoom": True,
            "AutoFocus": True,
            "AutoIrCutFilter": True,
            "AutoIris": True,
            "Auxiliary": True,
            "BackLight": True,
            "ContinuousBrightness": False,
            "ContinuousFocus": True,
            "ContinuousIris": False,
            "ContinuousPan": True,
            "ContinuousTilt": True,
            "ContinuousZoom": True,
            "DevicePreset": False,
            "DigitalZoom": True,
            "GenericHTTP": False,
            "IrCutFilter": True,
            "JoyStickEmulation": True,
            "LensOffset": False,
            "OSDMenu": False,
            "ProportionalSpeed": True,
            "RelativeBrightness": True,
            "RelativeFocus": True,
            "RelativeIris": True,
            "RelativePan": True,
            "RelativeTilt": True,
            "RelativeZoom": True,
            "ServerPreset": True,
            "SpeedCtl": True,
        }
    }
    assert params.ptz_various == {
        1: {
            "AutoFocus": True,
            "AutoIris": True,
            "BackLight": False,
            "BackLightEnabled": True,
            "BrightnessEnabled": True,
            "CtlQueueing": False,
            "CtlQueueLimit": 20,
            "CtlQueuePollTime": 20,
            "FocusEnabled": True,
            "HomePresetSet": True,
            "IrCutFilter": "auto",
            "IrCutFilterEnabled": True,
            "IrisEnabled": True,
            "MaxProportionalSpeed": 200,
            "PanEnabled": True,
            "ProportionalSpeedEnabled": True,
            "PTZCounter": 8,
            "ReturnToOverview": 0,
            "SpeedCtlEnabled": True,
            "TiltEnabled": True,
            "ZoomEnabled": True,
        }
    }


@respx.mock
@pytest.mark.asyncio
async def test_update_stream_profiles(params):
    """Verify that update properties works."""
    route = respx.get(
        f"http://{HOST}:80/axis-cgi/param.cgi?action=list&group=root.StreamProfile"
    ).respond(
        text=response_param_cgi,
        headers={"Content-Type": "text/plain"},
    )

    await params.update_stream_profiles()

    assert route.called
    assert route.calls.last.request.method == "GET"
    assert route.calls.last.request.url.path == "/axis-cgi/param.cgi"

    profiles = params.stream_profiles

    assert params.stream_profiles_max_groups == 26
    assert len(profiles) == 2
    assert profiles[0].name == "profile_1"
    assert profiles[0].description == "profile_1_description"
    assert profiles[0].parameters == "videocodec=h264"
    assert profiles[1].name == "profile_2"
    assert profiles[1].description == "profile_2_description"
    assert profiles[1].parameters == "videocodec=h265"


@respx.mock
@pytest.mark.asyncio
async def test_stream_profiles_empty_response(params):
    """Verify that update properties works."""
    respx.get(
        f"http://{HOST}:80/axis-cgi/param.cgi?action=list&group=root.StreamProfile"
    ).respond(
        text="",
        headers={"Content-Type": "text/plain"},
    )

    await params.update_stream_profiles()

    profiles = params.stream_profiles

    assert params.stream_profiles_max_groups == 0
    assert len(profiles) == 0


response_param_cgi = """root.Audio.DSCP=0
root.Audio.DuplexMode=half
root.Audio.MaxListeners=20
root.Audio.NbrOfConfigs=2
root.Audio.ReceiverBuffer=120
root.Audio.ReceiverTimeout=1000
root.Audio.A0.Enabled=no
root.Audio.A0.HTTPMessageType=singlepart
root.Audio.A0.Name=
root.Audio.A0.NbrOfChannels=1
root.Audio.A0.Source=0
root.Audio.A1.Enabled=no
root.Audio.A1.HTTPMessageType=singlepart
root.Audio.A1.Name=
root.Audio.A1.NbrOfChannels=1
root.Audio.A1.Source=0
root.AudioSource.NbrOfSources=1
root.AudioSource.A0.AlarmLevel=88
root.AudioSource.A0.AudioEncoding=aac
root.AudioSource.A0.AudioSupport=yes
root.AudioSource.A0.BitRate=32000
root.AudioSource.A0.InputGain=10
root.AudioSource.A0.InputType=mic
root.AudioSource.A0.Name=Audio
root.AudioSource.A0.NbrOfChannels=1
root.AudioSource.A0.OutputGain=0
root.AudioSource.A0.SampleRate=8000
root.Bandwidth.Limit=0
root.BasicDeviceInfo.BasicDeviceInfo=yes
root.Brand.Brand=AXIS
root.Brand.ProdFullName=AXIS M1065-LW Network Camera
root.Brand.ProdNbr=M1065-LW
root.Brand.ProdShortName=AXIS M1065-LW
root.Brand.ProdType=Network Camera
root.Brand.ProdVariant=
root.Brand.WebURL=http://www.axis.com
root.HTTPS.AllowSSLV3=no
root.HTTPS.AllowTLS1=yes
root.HTTPS.AllowTLS11=yes
root.HTTPS.Ciphers=DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:AES128-SHA:AES256-SHA
root.HTTPS.Enabled=yes
root.HTTPS.Port=443
root.Image.DateFormat=YYYY-MM-DD
root.Image.MaxViewers=20
root.Image.MotionDetection=no
root.Image.NbrOfConfigs=2
root.Image.OverlayPath=/etc/overlays/axis(128x44).ovl
root.Image.OwnDateFormat=%F
root.Image.OwnDateFormatEnabled=no
root.Image.OwnTimeFormat=%T
root.Image.OwnTimeFormatEnabled=no
root.Image.PrivacyMaskType=none
root.Image.Referrers=
root.Image.ReferrersEnabled=no
root.Image.RFCCompliantMultipartEnabled=yes
root.Image.TimeFormat=24
root.Image.TimeResolution=1
root.Image.TriggerDataEnabled=no
root.Image.I0.Enabled=yes
root.Image.I0.Name=View Area 1
root.Image.I0.Source=0
root.Image.I0.Appearance.ColorEnabled=yes
root.Image.I0.Appearance.Compression=30
root.Image.I0.Appearance.MirrorEnabled=no
root.Image.I0.Appearance.Resolution=1920x1080
root.Image.I0.Appearance.Rotation=0
root.Image.I0.MPEG.Complexity=50
root.Image.I0.MPEG.ConfigHeaderInterval=1
root.Image.I0.MPEG.FrameSkipMode=drop
root.Image.I0.MPEG.ICount=1
root.Image.I0.MPEG.PCount=31
root.Image.I0.MPEG.UserDataEnabled=no
root.Image.I0.MPEG.UserDataInterval=1
root.Image.I0.MPEG.ZChromaQPMode=off
root.Image.I0.MPEG.ZFpsMode=fixed
root.Image.I0.MPEG.ZGopMode=fixed
root.Image.I0.MPEG.ZMaxGopLength=300
root.Image.I0.MPEG.ZMinFps=0
root.Image.I0.MPEG.ZStrength=10
root.Image.I0.MPEG.H264.Profile=high
root.Image.I0.MPEG.H264.PSEnabled=no
root.Image.I0.Overlay.Enabled=no
root.Image.I0.Overlay.XPos=0
root.Image.I0.Overlay.YPos=0
root.Image.I0.Overlay.MaskWindows.Color=black
root.Image.I0.RateControl.MaxBitrate=0
root.Image.I0.RateControl.Mode=vbr
root.Image.I0.RateControl.Priority=framerate
root.Image.I0.RateControl.TargetBitrate=0
root.Image.I0.SizeControl.MaxFrameSize=0
root.Image.I0.Stream.Duration=0
root.Image.I0.Stream.FPS=0
root.Image.I0.Stream.NbrOfFrames=0
root.Image.I0.Text.BGColor=black
root.Image.I0.Text.ClockEnabled=no
root.Image.I0.Text.Color=white
root.Image.I0.Text.DateEnabled=no
root.Image.I0.Text.Position=top
root.Image.I0.Text.String=
root.Image.I0.Text.TextEnabled=no
root.Image.I0.Text.TextSize=medium
root.Image.I0.TriggerData.AudioEnabled=yes
root.Image.I0.TriggerData.MotionDetectionEnabled=yes
root.Image.I0.TriggerData.MotionLevelEnabled=no
root.Image.I0.TriggerData.TamperingEnabled=yes
root.Image.I0.TriggerData.UserTriggers=
root.Image.I1.Enabled=no
root.Image.I1.Name=View Area 2
root.Image.I1.Source=0
root.Image.I1.Appearance.ColorEnabled=yes
root.Image.I1.Appearance.Compression=30
root.Image.I1.Appearance.MirrorEnabled=no
root.Image.I1.Appearance.Resolution=1920x1080
root.Image.I1.Appearance.Rotation=0
root.Image.I1.MPEG.Complexity=50
root.Image.I1.MPEG.ConfigHeaderInterval=1
root.Image.I1.MPEG.FrameSkipMode=drop
root.Image.I1.MPEG.ICount=1
root.Image.I1.MPEG.PCount=31
root.Image.I1.MPEG.UserDataEnabled=no
root.Image.I1.MPEG.UserDataInterval=1
root.Image.I1.MPEG.ZChromaQPMode=off
root.Image.I1.MPEG.ZFpsMode=fixed
root.Image.I1.MPEG.ZGopMode=fixed
root.Image.I1.MPEG.ZMaxGopLength=300
root.Image.I1.MPEG.ZMinFps=0
root.Image.I1.MPEG.ZStrength=10
root.Image.I1.MPEG.H264.Profile=high
root.Image.I1.MPEG.H264.PSEnabled=no
root.Image.I1.Overlay.Enabled=no
root.Image.I1.Overlay.XPos=0
root.Image.I1.Overlay.YPos=0
root.Image.I1.RateControl.MaxBitrate=0
root.Image.I1.RateControl.Mode=vbr
root.Image.I1.RateControl.Priority=framerate
root.Image.I1.RateControl.TargetBitrate=0
root.Image.I1.SizeControl.MaxFrameSize=0
root.Image.I1.Stream.Duration=0
root.Image.I1.Stream.FPS=0
root.Image.I1.Stream.NbrOfFrames=0
root.Image.I1.Text.BGColor=black
root.Image.I1.Text.ClockEnabled=no
root.Image.I1.Text.Color=white
root.Image.I1.Text.DateEnabled=no
root.Image.I1.Text.Position=top
root.Image.I1.Text.String=
root.Image.I1.Text.TextEnabled=no
root.Image.I1.Text.TextSize=medium
root.Image.I1.TriggerData.AudioEnabled=yes
root.Image.I1.TriggerData.MotionDetectionEnabled=yes
root.Image.I1.TriggerData.MotionLevelEnabled=no
root.Image.I1.TriggerData.TamperingEnabled=yes
root.Image.I1.TriggerData.UserTriggers=
root.ImageSource.MotionDetection=yes
root.ImageSource.NbrOfSources=1
root.ImageSource.I0.CaptureFrequency=50Hz
root.ImageSource.I0.Name=Camera
root.ImageSource.I0.DayNight.IrCutFilter=auto
root.ImageSource.I0.DayNight.ShiftLevel=100
root.ImageSource.I0.Sensor.AspectRatio=16:9
root.ImageSource.I0.Sensor.Brightness=50
root.ImageSource.I0.Sensor.ColorLevel=50
root.ImageSource.I0.Sensor.Contrast=50
root.ImageSource.I0.Sensor.CoordX=5000
root.ImageSource.I0.Sensor.CoordY=5000
root.ImageSource.I0.Sensor.Exposure=auto
root.ImageSource.I0.Sensor.ExposurePriority=50
root.ImageSource.I0.Sensor.ExposurePriorityLowlight=100
root.ImageSource.I0.Sensor.ExposurePriorityNormal=0
root.ImageSource.I0.Sensor.ExposureValue=50
root.ImageSource.I0.Sensor.ManualGain=100
root.ImageSource.I0.Sensor.ManualGainControl=no
root.ImageSource.I0.Sensor.ManualShutter=33333
root.ImageSource.I0.Sensor.ManualShutterControl=no
root.ImageSource.I0.Sensor.MaxAutoGainControlLowlight=100
root.ImageSource.I0.Sensor.MaxAutoGainControlNormal=50
root.ImageSource.I0.Sensor.MaxExposureTime=-1
root.ImageSource.I0.Sensor.MaxFastShutter=1000
root.ImageSource.I0.Sensor.MaxGain=100
root.ImageSource.I0.Sensor.MaxSlowShutter=166667
root.ImageSource.I0.Sensor.MinExposureTime=31
root.ImageSource.I0.Sensor.MinGain=0
root.ImageSource.I0.Sensor.Sharpness=50
root.ImageSource.I0.Sensor.WDR=on
root.ImageSource.I0.Sensor.WhiteBalance=auto
root.Input.NbrOfInputs=1
root.IOPort.I0.Configurable=no
root.IOPort.I0.Direction=input
root.IOPort.I0.Input.Name=PIR sensor
root.IOPort.I0.Input.Trig=closed
root.Layout.AACInstallationEnabled=yes
root.Layout.AMCRecordMedia=0
root.Layout.Axis=yes
root.Layout.DefaultJoystickMode=no
root.Layout.DefaultStreamProfile=
root.Layout.DefaultVideoFormat=mjpeg
root.Layout.EnableBasicSetup=yes
root.Layout.H264InstallationEnabled=yes
root.Layout.InstantReplayEnabled=no
root.Layout.InstantReplayTimeOffset=30
root.Layout.IRIlluminationEnabled=yes
root.Layout.LiveViewVideo=1
root.Layout.ManualIRIlluminationOverride=no
root.Layout.OwnHomePageEnabled=no
root.Layout.OwnHomePagePath=dummy
root.Layout.PlainConfigEnabled=no
root.Layout.PlayAudioClipEnabled=yes
root.Layout.SetupLinkEnabled=yes
root.Layout.ShowAMCToolbar=yes
root.Layout.ShowRelCrossEnabled=yes
root.Layout.ShowSceneProfileSelector=yes
root.Layout.ShowVideoFormatDropDown=yes
root.Layout.SnapshotEnabled=no
root.Layout.ViewerIE=activex
root.Layout.ViewerOther=spush
root.Layout.CustomLink.C0.Enabled=no
root.Layout.CustomLink.C0.Name=Custom link 1
root.Layout.CustomLink.C0.URL=http://
root.Layout.CustomLink.C0.Usage=cgi
root.Layout.CustomLink.C1.Enabled=no
root.Layout.CustomLink.C1.Name=Custom link 2
root.Layout.CustomLink.C1.URL=http://
root.Layout.CustomLink.C1.Usage=cgi
root.Layout.CustomLink.C2.Enabled=no
root.Layout.CustomLink.C2.Name=Custom link 3
root.Layout.CustomLink.C2.URL=http://
root.Layout.CustomLink.C2.Usage=cgi
root.Layout.CustomLink.C3.Enabled=no
root.Layout.CustomLink.C3.Name=Custom link 4
root.Layout.CustomLink.C3.URL=http://
root.Layout.CustomLink.C3.Usage=cgi
root.Layout.Trigger.T0.Enabled=no
root.Layout.Trigger.T1.Enabled=no
root.MediaClip.MaxGroups=10
root.MediaClip.M9.Location=/etc/audioclips/camera_clicks16k.au
root.MediaClip.M9.Name=Camera clicks
root.MediaClip.M9.Type=audio
root.Network.BootProto=dhcp
root.Network.Broadcast=192.168.0.255
root.Network.DefaultRouter=192.168.0.1
root.Network.DNSServer1=0.0.0.0
root.Network.DNSServer2=0.0.0.0
root.Network.DomainName=
root.Network.Enabled=yes
root.Network.HostName=axis-accc8e7ea36d
root.Network.InterfaceSelectMode=auto
root.Network.IPAddress=192.168.0.90
root.Network.Media=auto
root.Network.SubnetMask=255.255.255.0
root.Network.tcpECN=1
root.Network.AxisNS.CheckIPAddress=0.0.0.0
root.Network.AxisNS.CheckPeriod=10
root.Network.AxisNS.CheckTTL=0
root.Network.AxisNS.Enabled=no
root.Network.AxisNS.LockButton=yes
root.Network.AxisNS.ServerLink=www.axiscam.net
root.Network.AxisNS.ServerList=www0.axiscam.net,195.60.68.29,www1.axiscam.net,195.60.68.30
root.Network.AxisNS.ServerPath=reg_cam.php
root.Network.AxisNS.UpdatePeriod=0
root.Network.Bonjour.Enabled=yes
root.Network.Bonjour.FriendlyName=AXIS M1065-LW - ACCC12345678
root.Network.DHCP.VendorClass=AXIS,Network Camera,M1065-LW,8.20.1
root.Network.DNSUpdate.DNSName=
root.Network.DNSUpdate.Enabled=no
root.Network.DNSUpdate.TTL=30
root.Network.eth0.Broadcast=192.168.0.255
root.Network.eth0.IPAddress=192.168.0.90
root.Network.eth0.MACAddress=AC:CC:12:34:56:78
root.Network.eth0.SubnetMask=255.255.255.0
root.Network.eth0.IPv6.IPAddresses=
root.Network.Filter.Enabled=no
root.Network.Filter.Input.AcceptAddresses=
root.Network.Filter.Input.Policy=allow
root.Network.Filter.Log.Enabled=no
root.Network.FTP.Enabled=no
root.Network.HTTP.AuthenticationPolicy=digest
root.Network.HTTP.AuthenticationPolicySet=yes
root.Network.HTTP.AuthenticationWithQop=no
root.Network.Interface.I0.SystemDevice=eth0
root.Network.Interface.I0.Type=802.3
root.Network.Interface.I0.Active.Active=no
root.Network.Interface.I0.Active.Broadcast=
root.Network.Interface.I0.Active.IPAddress=
root.Network.Interface.I0.Active.IPv6Addresses=
root.Network.Interface.I0.Active.MACAddress=AC:CC:12:34:56:78
root.Network.Interface.I0.Active.SubnetMask=
root.Network.Interface.I0.dot1x.EAPOLVersion=1
root.Network.Interface.I0.dot1x.Enabled=no
root.Network.Interface.I0.dot1x.Status=Stopped
root.Network.Interface.I0.dot1x.EAPTLS.Identity=
root.Network.Interface.I0.dot1x.EAPTLS.PrivateKeyPassword=******
root.Network.Interface.I0.Link.AcceptRA=yes
root.Network.Interface.I0.Link.BootProto=dhcp
root.Network.Interface.I0.Link.DHCPv6=auto
root.Network.Interface.I0.Link.IPv4Enabled=yes
root.Network.Interface.I0.Link.IPv6Enabled=no
root.Network.Interface.I0.Link.Media=auto
root.Network.Interface.I0.Link.MTU=1500
root.Network.Interface.I0.Manual.Broadcast=192.168.0.255
root.Network.Interface.I0.Manual.DefaultRouter=192.168.0.1
root.Network.Interface.I0.Manual.IPAddress=192.168.0.90
root.Network.Interface.I0.Manual.IPv6Address=
root.Network.Interface.I0.Manual.IPv6DefaultRouter=
root.Network.Interface.I0.Manual.SubnetMask=255.255.255.0
root.Network.Interface.I0.ZeroConf.Enabled=yes
root.Network.Interface.I0.ZeroConf.IPAddress=
root.Network.Interface.I0.ZeroConf.SubnetMask=
root.Network.Interface.I1.SystemDevice=eth1
root.Network.Interface.I1.Type=802.11
root.Network.Interface.I1.Active.Active=yes
root.Network.Interface.I1.Active.Broadcast=192.168.0.255
root.Network.Interface.I1.Active.IPAddress=192.168.0.90
root.Network.Interface.I1.Active.IPv6Addresses=
root.Network.Interface.I1.Active.MACAddress=AC:CC:12:34:56:78
root.Network.Interface.I1.Active.SubnetMask=255.255.255.0
root.Network.Interface.I1.dot1x.EAPOLVersion=1
root.Network.Interface.I1.dot1x.EAPPEAPMSCHAPv2.Identity=
root.Network.Interface.I1.dot1x.EAPPEAPMSCHAPv2.Label=1
root.Network.Interface.I1.dot1x.EAPPEAPMSCHAPv2.Password=******
root.Network.Interface.I1.dot1x.EAPPEAPMSCHAPv2.Version=1
root.Network.Interface.I1.dot1x.EAPTLS.Identity=
root.Network.Interface.I1.dot1x.EAPTLS.PrivateKeyPassword=******
root.Network.Interface.I1.Link.AcceptRA=yes
root.Network.Interface.I1.Link.BootProto=dhcp
root.Network.Interface.I1.Link.DHCPv6=auto
root.Network.Interface.I1.Link.IPv4Enabled=yes
root.Network.Interface.I1.Link.IPv6Enabled=no
root.Network.Interface.I1.Link.MTU=1500
root.Network.Interface.I1.Manual.Broadcast=192.168.0.255
root.Network.Interface.I1.Manual.DefaultRouter=192.168.0.1
root.Network.Interface.I1.Manual.IPAddress=192.168.0.90
root.Network.Interface.I1.Manual.IPv6Address=
root.Network.Interface.I1.Manual.IPv6DefaultRouter=
root.Network.Interface.I1.Manual.SubnetMask=255.255.255.0
root.Network.Interface.I1.ZeroConf.Enabled=yes
root.Network.Interface.I1.ZeroConf.IPAddress=169.254.220.95
root.Network.Interface.I1.ZeroConf.SubnetMask=255.255.0.0
root.Network.IPv6.AcceptRA=yes
root.Network.IPv6.DefaultRouter=
root.Network.IPv6.DHCPv6=auto
root.Network.IPv6.Enabled=no
root.Network.IPv6.IPAddress=
root.Network.QoS.Class1.Desc=AxisLiveVideo
root.Network.QoS.Class1.DSCP=0
root.Network.QoS.Class2.Desc=AxisLiveAudio
root.Network.QoS.Class2.DSCP=0
root.Network.QoS.Class3.Desc=AxisEventAlarm
root.Network.QoS.Class3.DSCP=0
root.Network.QoS.Class4.Desc=AxisManagement
root.Network.QoS.Class4.DSCP=0
root.Network.QoS.Class5.Desc=AxisRemoteService
root.Network.QoS.Class5.DSCP=0
root.Network.QoS.Class6.Desc=AxisMetaData
root.Network.QoS.Class6.DSCP=0
root.Network.Resolver.NameServer1=192.168.0.1
root.Network.Resolver.NameServer2=
root.Network.Resolver.NameServerList=192.168.0.1
root.Network.Resolver.ObtainFromDHCP=yes
root.Network.Resolver.Search=localdomain
root.Network.Routing.DefaultRouter=192.168.0.1
root.Network.Routing.IPv6.DefaultRouter=
root.Network.RTP.AudioDSCP=0
root.Network.RTP.EndPort=50999
root.Network.RTP.InternallyTaggedMulticastEnabled=no
root.Network.RTP.MetadataDSCP=0
root.Network.RTP.NbrOfRTPGroups=2
root.Network.RTP.StartPort=50000
root.Network.RTP.VideoDSCP=0
root.Network.RTP.R0.AlwaysMulticastAudio=no
root.Network.RTP.R0.AlwaysMulticastProfile=videocodec=h264
root.Network.RTP.R0.AlwaysMulticastVideo=no
root.Network.RTP.R0.AudioAddress=239.198.163.237
root.Network.RTP.R0.AudioPort=0
root.Network.RTP.R0.TTL=5
root.Network.RTP.R0.VideoAddress=239.198.163.109
root.Network.RTP.R0.VideoPort=0
root.Network.RTP.R1.AlwaysMulticastAudio=no
root.Network.RTP.R1.AlwaysMulticastProfile=videocodec=h264
root.Network.RTP.R1.AlwaysMulticastVideo=no
root.Network.RTP.R1.AudioAddress=239.228.163.237
root.Network.RTP.R1.AudioPort=0
root.Network.RTP.R1.TTL=5
root.Network.RTP.R1.VideoAddress=239.228.163.109
root.Network.RTP.R1.VideoPort=0
root.Network.RTSP.AllowClientTransportSettings=no
root.Network.RTSP.AuthenticateOverHTTP=no
root.Network.RTSP.AuthenticateRTSPOverHTTP=yes
root.Network.RTSP.Enabled=yes
root.Network.RTSP.Port=554
root.Network.RTSP.ProtViewer=******
root.Network.RTSP.Timeout=60
root.Network.SSH.Enabled=no
root.Network.UPnP.Enabled=yes
root.Network.UPnP.FriendlyName=AXIS M1065-LW - ACCC12345678
root.Network.UPnP.NATTraversal.Active=no
root.Network.UPnP.NATTraversal.Enabled=no
root.Network.UPnP.NATTraversal.ExternalIPAddress=
root.Network.UPnP.NATTraversal.MaxPort=65535
root.Network.UPnP.NATTraversal.MinPort=32768
root.Network.UPnP.NATTraversal.Router=
root.Network.VolatileHostName.HostName=axis-accc12345678
root.Network.VolatileHostName.ObtainFromDHCP=yes
root.Network.Wireless.ESSID=PhG
root.Network.Wireless.MODE=managed
root.Network.Wireless.RTS.Enabled=no
root.Network.Wireless.RTS.Threshold=500
root.Network.Wireless.W0.Enabled=yes
root.Network.Wireless.W0.GenerationMethod=psk-phrase
root.Network.Wireless.W0.Key=******
root.Network.Wireless.W0.Method=WPA-PSK
root.Network.Wireless.W0.Passphrase=******
root.Network.Wireless.W1.Dot1XMethod=EAPTLS
root.Network.Wireless.W1.Enabled=no
root.Network.Wireless.W1.Method=WPA-ENTERPRISE
root.Network.Wireless.Wlwd.Enabled=yes
root.Network.Wireless.WPS.PBC.Enabled=yes
root.Network.ZeroConf.Enabled=yes
root.Network.ZeroConf.IPAddress=169.254.220.95
root.Network.ZeroConf.SubnetMask=255.255.0.0
root.Output.NbrOfOutputs=0
root.Properties.AlwaysMulticast.AlwaysMulticast=yes
root.Properties.API.Browser.Language=yes
root.Properties.API.Browser.RootPwdSetValue=yes
root.Properties.API.Browser.UserGroup=yes
root.Properties.API.ClientNotes.ClientNotes=yes
root.Properties.API.HTTP.AdminPath=/
root.Properties.API.HTTP.Version=3
root.Properties.API.Metadata.Metadata=yes
root.Properties.API.Metadata.Version=1.0
root.Properties.API.OnScreenControls.OnScreenControls=yes
root.Properties.API.PTZ.Presets.Version=2.00
root.Properties.API.RTSP.RTSPAuth=yes
root.Properties.API.RTSP.Version=2.01
root.Properties.API.WebService.EntryService=yes
root.Properties.API.WebService.WebService=yes
root.Properties.API.WebService.ONVIF.ONVIF=yes
root.Properties.API.WebService.ONVIF.Version=1.02
root.Properties.API.WebSocket.RTSP.RTSP=yes
root.Properties.ApiDiscovery.ApiDiscovery=yes
root.Properties.Audio.Audio=yes
root.Properties.Audio.DuplexMode=half,post,get
root.Properties.Audio.Format=lpcm,g711,g726,aac,opus
root.Properties.Audio.InputType=internal
root.Properties.Audio.Decoder.Format=g711,g726,axis-mulaw-128
root.Properties.Audio.Source.A0.Input=yes
root.Properties.Audio.Source.A0.Output=yes
root.Properties.EmbeddedDevelopment.CacheSize=76546048
root.Properties.EmbeddedDevelopment.DefaultCacheSize=92274688
root.Properties.EmbeddedDevelopment.EmbeddedDevelopment=yes
root.Properties.EmbeddedDevelopment.Version=2.16
root.Properties.EmbeddedDevelopment.RuleEngine.MultiConfiguration=yes
root.Properties.Firmware.BuildDate=Feb 15 2019 09:42
root.Properties.Firmware.BuildNumber=26
root.Properties.Firmware.Version=9.10.1
root.Properties.FirmwareManagement.Version=1.0
root.Properties.GuardTour.GuardTour=yes
root.Properties.GuardTour.MaxGuardTours=100
root.Properties.GuardTour.MinGuardTourWaitTime=10
root.Properties.GuardTour.RecordedTour=no
root.Properties.HTTPS.HTTPS=yes
root.Properties.Image.Format=jpeg,mjpeg,h264
root.Properties.Image.NbrOfViews=2
root.Properties.Image.Resolution=1920x1080,1280x960,1280x720,1024x768,1024x576,800x600,640x480,640x360,352x240,320x240
root.Properties.Image.Rotation=0,180
root.Properties.Image.ShowSuboptimalResolutions=false
root.Properties.Image.H264.Profiles=Baseline,Main,High
root.Properties.ImageSource.DayNight=yes
root.Properties.IO.ManualTriggerNbr=6
root.Properties.LEDControl.LEDControl=yes
root.Properties.LightControl.LightControl2=yes
root.Properties.LightControl.LightControlAvailable=yes
root.Properties.LocalStorage.AutoRepair=yes
root.Properties.LocalStorage.ContinuousRecording=yes
root.Properties.LocalStorage.DiskEncryption=yes
root.Properties.LocalStorage.DiskHealth=yes
root.Properties.LocalStorage.ExportRecording=yes
root.Properties.LocalStorage.FailOverRecording=yes
root.Properties.LocalStorage.LocalStorage=yes
root.Properties.LocalStorage.NbrOfContinuousRecordingProfiles=1
root.Properties.LocalStorage.RequiredFileSystem=yes
root.Properties.LocalStorage.SDCard=yes
root.Properties.LocalStorage.StorageLimit=yes
root.Properties.LocalStorage.Version=1.00
root.Properties.Motion.MaxNbrOfWindows=10
root.Properties.Motion.Motion=yes
root.Properties.Network.WLAN.WLANScan2=yes
root.Properties.NetworkShare.CIFS=yes
root.Properties.NetworkShare.IPV6=yes
root.Properties.NetworkShare.NameLookup=yes
root.Properties.NetworkShare.NetworkShare=yes
root.Properties.PackageManager.FormatListing=yes
root.Properties.PackageManager.LicenseKeyManagement=yes
root.Properties.PackageManager.PackageManager=yes
root.Properties.PrivacyMask.MaxNbrOfPrivacyMasks=10
root.Properties.PrivacyMask.Polygon=no
root.Properties.PrivacyMask.PrivacyMask=no
root.Properties.PrivacyMask.Query=list,position,listpxjson,positionpxjson
root.Properties.PTZ.DigitalPTZ=yes
root.Properties.PTZ.DriverManagement=no
root.Properties.PTZ.DriverModeList=none
root.Properties.PTZ.PTZ=yes
root.Properties.PTZ.PTZOnQuadView=no
root.Properties.PTZ.SelectableDriverMode=no
root.Properties.RemoteService.RemoteService=no
root.Properties.RTC.RTC=yes
root.Properties.Sensor.PIR=yes
root.Properties.Serial.Serial=no
root.Properties.System.Architecture=armv7hf
root.Properties.System.HardwareID=70E
root.Properties.System.Language=English
root.Properties.System.LanguageType=default
root.Properties.System.SerialNumber=ACCC12345678
root.Properties.System.Soc=Ambarella S2L (Flattened Device Tree)
root.Properties.Tampering.Tampering=yes
root.Properties.TemperatureSensor.Fan=no
root.Properties.TemperatureSensor.Heater=no
root.Properties.TemperatureSensor.TemperatureControl=yes
root.Properties.TemperatureSensor.TemperatureSensor=yes
root.Properties.VirtualInput.VirtualInput=yes
root.Properties.ZipStream.ZipStream=yes
root.PTZ.BoaProtPTZOperator=******
root.PTZ.CameraDefault=1
root.PTZ.NbrOfCameras=2
root.PTZ.NbrOfSerPorts=0
root.PTZ.CamPorts.Cam1Port=1
root.PTZ.CamPorts.Cam2Port=2
root.PTZ.ImageSource.I0.PTZEnabled=false
root.PTZ.Limit.L1.MaxFieldAngle=100
root.PTZ.Limit.L1.MaxPan=120
root.PTZ.Limit.L1.MaxTilt=120
root.PTZ.Limit.L1.MaxZoom=9999
root.PTZ.Limit.L1.MinFieldAngle=1
root.PTZ.Limit.L1.MinPan=-120
root.PTZ.Limit.L1.MinTilt=-120
root.PTZ.Limit.L1.MinZoom=1
root.PTZ.Limit.L2.MaxFieldAngle=100
root.PTZ.Limit.L2.MaxPan=120
root.PTZ.Limit.L2.MaxTilt=120
root.PTZ.Limit.L2.MaxZoom=9999
root.PTZ.Limit.L2.MinFieldAngle=1
root.PTZ.Limit.L2.MinPan=-120
root.PTZ.Limit.L2.MinTilt=-120
root.PTZ.Limit.L2.MinZoom=1
root.PTZ.Preset.P0.HomePosition=1
root.PTZ.Preset.P0.ImageSource=0
root.PTZ.Preset.P0.Name=
root.PTZ.Preset.P0.Position.P1.Data=pan=0.000000:tilt=0.000000:zoom=1.000000
root.PTZ.Preset.P0.Position.P1.Name=Home
root.PTZ.Preset.P1.HomePosition=1
root.PTZ.Preset.P1.ImageSource=1
root.PTZ.Preset.P1.Name=
root.PTZ.Preset.P1.Position.P1.Data=pan=0.000000:tilt=0.000000:zoom=1.000000
root.PTZ.Preset.P1.Position.P1.Name=Home
root.PTZ.PTZDriverStatuses.Driver1Status=3
root.PTZ.PTZDriverStatuses.Driver2Status=3
root.PTZ.Support.S1.AbsoluteBrightness=false
root.PTZ.Support.S1.AbsoluteFocus=false
root.PTZ.Support.S1.AbsoluteIris=false
root.PTZ.Support.S1.AbsolutePan=true
root.PTZ.Support.S1.AbsoluteTilt=true
root.PTZ.Support.S1.AbsoluteZoom=true
root.PTZ.Support.S1.ActionNotification=true
root.PTZ.Support.S1.AreaZoom=true
root.PTZ.Support.S1.AutoFocus=false
root.PTZ.Support.S1.AutoIrCutFilter=false
root.PTZ.Support.S1.AutoIris=false
root.PTZ.Support.S1.Auxiliary=false
root.PTZ.Support.S1.BackLight=false
root.PTZ.Support.S1.ContinuousBrightness=false
root.PTZ.Support.S1.ContinuousFocus=false
root.PTZ.Support.S1.ContinuousIris=false
root.PTZ.Support.S1.ContinuousPan=true
root.PTZ.Support.S1.ContinuousTilt=true
root.PTZ.Support.S1.ContinuousZoom=true
root.PTZ.Support.S1.DevicePreset=false
root.PTZ.Support.S1.DigitalZoom=false
root.PTZ.Support.S1.GenericHTTP=false
root.PTZ.Support.S1.IrCutFilter=false
root.PTZ.Support.S1.JoyStickEmulation=true
root.PTZ.Support.S1.LensOffset=false
root.PTZ.Support.S1.OSDMenu=false
root.PTZ.Support.S1.ProportionalSpeed=true
root.PTZ.Support.S1.RelativeBrightness=false
root.PTZ.Support.S1.RelativeFocus=false
root.PTZ.Support.S1.RelativeIris=false
root.PTZ.Support.S1.RelativePan=true
root.PTZ.Support.S1.RelativeTilt=true
root.PTZ.Support.S1.RelativeZoom=true
root.PTZ.Support.S1.ServerPreset=true
root.PTZ.Support.S1.SpeedCtl=true
root.PTZ.Support.S2.AbsoluteBrightness=false
root.PTZ.Support.S2.AbsoluteFocus=false
root.PTZ.Support.S2.AbsoluteIris=false
root.PTZ.Support.S2.AbsolutePan=true
root.PTZ.Support.S2.AbsoluteTilt=true
root.PTZ.Support.S2.AbsoluteZoom=true
root.PTZ.Support.S2.ActionNotification=true
root.PTZ.Support.S2.AreaZoom=true
root.PTZ.Support.S2.AutoFocus=false
root.PTZ.Support.S2.AutoIrCutFilter=false
root.PTZ.Support.S2.AutoIris=false
root.PTZ.Support.S2.Auxiliary=false
root.PTZ.Support.S2.BackLight=false
root.PTZ.Support.S2.ContinuousBrightness=false
root.PTZ.Support.S2.ContinuousFocus=false
root.PTZ.Support.S2.ContinuousIris=false
root.PTZ.Support.S2.ContinuousPan=true
root.PTZ.Support.S2.ContinuousTilt=true
root.PTZ.Support.S2.ContinuousZoom=true
root.PTZ.Support.S2.DevicePreset=false
root.PTZ.Support.S2.DigitalZoom=false
root.PTZ.Support.S2.GenericHTTP=false
root.PTZ.Support.S2.IrCutFilter=false
root.PTZ.Support.S2.JoyStickEmulation=true
root.PTZ.Support.S2.LensOffset=false
root.PTZ.Support.S2.OSDMenu=false
root.PTZ.Support.S2.ProportionalSpeed=true
root.PTZ.Support.S2.RelativeBrightness=false
root.PTZ.Support.S2.RelativeFocus=false
root.PTZ.Support.S2.RelativeIris=false
root.PTZ.Support.S2.RelativePan=true
root.PTZ.Support.S2.RelativeTilt=true
root.PTZ.Support.S2.RelativeZoom=true
root.PTZ.Support.S2.ServerPreset=true
root.PTZ.Support.S2.SpeedCtl=true
root.PTZ.UserAdv.U1.MoveSpeed=100
root.PTZ.UserAdv.U2.MoveSpeed=100
root.PTZ.UserCtlQueue.U0.Priority=10
root.PTZ.UserCtlQueue.U0.TimeoutTime=60
root.PTZ.UserCtlQueue.U0.TimeoutType=activity
root.PTZ.UserCtlQueue.U0.UseCookie=no
root.PTZ.UserCtlQueue.U0.UserGroup=Administrator
root.PTZ.UserCtlQueue.U1.Priority=30
root.PTZ.UserCtlQueue.U1.TimeoutTime=60
root.PTZ.UserCtlQueue.U1.TimeoutType=activity
root.PTZ.UserCtlQueue.U1.UseCookie=no
root.PTZ.UserCtlQueue.U1.UserGroup=Operator
root.PTZ.UserCtlQueue.U2.Priority=50
root.PTZ.UserCtlQueue.U2.TimeoutTime=60
root.PTZ.UserCtlQueue.U2.TimeoutType=timespan
root.PTZ.UserCtlQueue.U2.UseCookie=no
root.PTZ.UserCtlQueue.U2.UserGroup=Viewer
root.PTZ.UserCtlQueue.U3.Priority=20
root.PTZ.UserCtlQueue.U3.TimeoutTime=20
root.PTZ.UserCtlQueue.U3.TimeoutType=activity
root.PTZ.UserCtlQueue.U3.UseCookie=no
root.PTZ.UserCtlQueue.U3.UserGroup=Event
root.PTZ.UserCtlQueue.U4.Priority=40
root.PTZ.UserCtlQueue.U4.TimeoutTime=60
root.PTZ.UserCtlQueue.U4.TimeoutType=infinity
root.PTZ.UserCtlQueue.U4.UseCookie=no
root.PTZ.UserCtlQueue.U4.UserGroup=Guardtour
root.PTZ.UserCtlQueue.U5.Priority=35
root.PTZ.UserCtlQueue.U5.TimeoutTime=60
root.PTZ.UserCtlQueue.U5.TimeoutType=infinity
root.PTZ.UserCtlQueue.U5.UseCookie=no
root.PTZ.UserCtlQueue.U5.UserGroup=Autotracking
root.PTZ.UserCtlQueue.U6.Priority=1
root.PTZ.UserCtlQueue.U6.TimeoutTime=60
root.PTZ.UserCtlQueue.U6.TimeoutType=activity
root.PTZ.UserCtlQueue.U6.UseCookie=no
root.PTZ.UserCtlQueue.U6.UserGroup=Onvif
root.PTZ.Various.V1.CtlQueueing=false
root.PTZ.Various.V1.CtlQueueLimit=20
root.PTZ.Various.V1.CtlQueuePollTime=20
root.PTZ.Various.V1.HomePresetSet=true
root.PTZ.Various.V1.Locked=true
root.PTZ.Various.V1.MaxProportionalSpeed=200
root.PTZ.Various.V1.PanEnabled=true
root.PTZ.Various.V1.ProportionalSpeedEnabled=true
root.PTZ.Various.V1.ReturnToOverview=30
root.PTZ.Various.V1.SpeedCtlEnabled=true
root.PTZ.Various.V1.TiltEnabled=true
root.PTZ.Various.V1.ZoomEnabled=true
root.PTZ.Various.V2.CtlQueueing=false
root.PTZ.Various.V2.CtlQueueLimit=20
root.PTZ.Various.V2.CtlQueuePollTime=20
root.PTZ.Various.V2.HomePresetSet=true
root.PTZ.Various.V2.Locked=true
root.PTZ.Various.V2.MaxProportionalSpeed=200
root.PTZ.Various.V2.PanEnabled=true
root.PTZ.Various.V2.ProportionalSpeedEnabled=true
root.PTZ.Various.V2.ReturnToOverview=30
root.PTZ.Various.V2.SpeedCtlEnabled=true
root.PTZ.Various.V2.TiltEnabled=true
root.PTZ.Various.V2.ZoomEnabled=true
root.Recording.DefaultDiskId=SD_DISK
root.Recording.DefaultSplitDuration=300
root.RemoteService.ClientCert=
root.RemoteService.DSCP=0
root.RemoteService.Enabled=oneclick
root.RemoteService.LogFile=syslog
root.RemoteService.ProxyAuth=basic
root.RemoteService.ProxyLogin=
root.RemoteService.ProxyPassword=
root.RemoteService.ProxyPort=3128
root.RemoteService.ProxyServer=
root.RemoteService.ServerList=dispatchse1-st.axis.com:443,dispatchse1-st.axis.com:80,195.60.68.120:443,195.60.68.120:80,dispatchse2-st.axis.com:443,dispatchse2-st.axis.com:80,195.60.68.121:443,195.60.68.121:80,dispatcher-st.axis.com:443,dispatcher-st.axis.com:80,dispatchus1-st.axis.com:443,dispatchus1-st.axis.com:80,dispatchjp1-st.axis.com:443,dispatchjp1-st.axis.com:80
root.SNMP.DSCP=0
root.SNMP.Enabled=no
root.SNMP.EngineBoots=1
root.SNMP.InitialUserPasswd=*****
root.SNMP.InitialUserPasswdSet=no
root.SNMP.V1=no
root.SNMP.V1ReadCommunity=public
root.SNMP.V1WriteCommunity=write
root.SNMP.V2c=no
root.SNMP.V3=no
root.SNMP.Trap.Enabled=no
root.SNMP.Trap.T0.Address=
root.SNMP.Trap.T0.Community=public
root.SNMP.Trap.T0.AuthFail.Enabled=no
root.SNMP.Trap.T0.ColdStart.Enabled=no
root.SNMP.Trap.T0.LinkUp.Enabled=no
root.SNMP.Trap.T0.WarmStart.Enabled=no
root.SOCKS.Enabled=no
root.SOCKS.LocalNetworks=192.168.0.0/255.0.0.0, 169.254.0.0/255.255.0.0, 172.16.0.0/255.240.0.0
root.SOCKS.Password=******
root.SOCKS.Server=socks
root.SOCKS.ServerPort=1080
root.SOCKS.ServerType=4
root.SOCKS.UserName=
root.Storage.MountDir=/var/spool/storage
root.Storage.S0.AutoRepair=yes
root.Storage.S0.CleanupLevel=90
root.Storage.S0.CleanupMaxAge=7
root.Storage.S0.CleanupPolicyActive=fifo
root.Storage.S0.DeviceNode=/dev/sd_disk1
root.Storage.S0.DiskID=SD_DISK
root.Storage.S0.ExtraMountOptions=
root.Storage.S0.FileSystem=vfat
root.Storage.S0.FriendlyName=
root.Storage.S0.Locked=no
root.Storage.S0.MountOnBoot=yes
root.Storage.S0.RequiredFileSystem=none
root.Storage.S1.AutoRepair=yes
root.Storage.S1.CleanupLevel=90
root.Storage.S1.CleanupMaxAge=7
root.Storage.S1.CleanupPolicyActive=fifo
root.Storage.S1.DeviceNode=NetworkShare:
root.Storage.S1.DiskID=NetworkShare
root.Storage.S1.ExtraMountOptions=
root.Storage.S1.FileSystem=cifs
root.Storage.S1.FriendlyName=
root.Storage.S1.Locked=no
root.Storage.S1.MountOnBoot=yes
root.Storage.S1.RequiredFileSystem=none
root.StreamCache.MaxGroups=20
root.StreamCache.Size=76546048
root.StreamCache.S0.Enabled=no
root.StreamCache.S0.Options=
root.StreamCache.S0.RequestedLengthTime=30
root.StreamProfile.MaxGroups=26
root.StreamProfile.S0.Description=profile_1_description
root.StreamProfile.S0.Name=profile_1
root.StreamProfile.S0.Parameters=videocodec=h264
root.StreamProfile.S1.Description=profile_2_description
root.StreamProfile.S1.Name=profile_2
root.StreamProfile.S1.Parameters=videocodec=h265
root.System.AccessLog=Off
root.System.AlternateBoaPort=0
root.System.BoaDSCP=0
root.System.BoaKeepAliveTimeout=180
root.System.BoaPort=80
root.System.BoaProtViewer=******
root.System.CaptureFrequencySet=yes
root.System.EditCgi=no
root.System.HTTPAuthRTSPOverHTTP=no
root.System.HTTPWatchDog=yes
root.System.RootPwdSet=yes
root.System.SkipDigestUriValidation=User-Agent HttpClient
root.System.BoaGroupPolicy.admin=both
root.System.BoaGroupPolicy.operator=both
root.System.BoaGroupPolicy.viewer=both
root.System.EmbeddedDevelopment.VaconfigFilter=Omnicast
root.System.PreventDoSAttack.ActivatePasswordThrottling=Off
root.System.PreventDoSAttack.DoSBlockingPeriod=10
root.System.PreventDoSAttack.DoSPageCount=20
root.System.PreventDoSAttack.DoSPageInterval=1
root.System.PreventDoSAttack.DoSSiteCount=50
root.System.PreventDoSAttack.DoSSiteInterval=1
root.Tampering.T0.DarkDetectionEnabled=yes
root.Tampering.T0.DarkThreshold=90
root.Tampering.T0.MinDuration=20
root.TemperatureControl.Sensor.S0.Name=IR led
root.TemperatureControl.Sensor.S0.TriggerHigh=75
root.TemperatureControl.Sensor.S0.TriggerLow=-10
root.TemperatureControl.Sensor.S1.Name=Sensor
root.TemperatureControl.Sensor.S1.TriggerHigh=75
root.TemperatureControl.Sensor.S1.TriggerLow=-10
root.Time.ObtainFromDHCP=yes
root.Time.POSIXTimeZone=CET-1CEST,M3.5.0,M10.5.0/3
root.Time.ServerDate=
root.Time.ServerTime=
root.Time.SyncSource=NTP
root.Time.DST.Enabled=no
root.Time.NTP.Server=0.0.0.0
root.Time.NTP.VolatileServer=0.0.0.0
root.WebService.UsernameToken.ReplayAttackProtection=yes"""


response_param_cgi_brand = """root.Brand.Brand=AXIS
root.Brand.ProdFullName=AXIS M1065-LW Network Camera
root.Brand.ProdNbr=M1065-LW
root.Brand.ProdShortName=AXIS M1065-LW
root.Brand.ProdType=Network Camera
root.Brand.ProdVariant=
root.Brand.WebURL=http://www.axis.com"""


response_param_cgi_ports = """root.Input.NbrOfInputs=1
root.IOPort.I0.Configurable=no
root.IOPort.I0.Direction=input
root.IOPort.I0.Input.Name=PIR sensor
root.IOPort.I0.Input.Trig=closed
root.Output.NbrOfOutputs=0
"""


response_param_cgi_properties = """root.Properties.AlwaysMulticast.AlwaysMulticast=yes
root.Properties.API.Browser.Language=yes
root.Properties.API.Browser.RootPwdSetValue=yes
root.Properties.API.Browser.UserGroup=yes
root.Properties.API.ClientNotes.ClientNotes=yes
root.Properties.API.HTTP.AdminPath=/
root.Properties.API.HTTP.Version=3
root.Properties.API.Metadata.Metadata=yes
root.Properties.API.Metadata.Version=1.0
root.Properties.API.OnScreenControls.OnScreenControls=yes
root.Properties.API.PTZ.Presets.Version=2.00
root.Properties.API.RTSP.RTSPAuth=yes
root.Properties.API.RTSP.Version=2.01
root.Properties.API.WebService.EntryService=yes
root.Properties.API.WebService.WebService=yes
root.Properties.API.WebService.ONVIF.ONVIF=yes
root.Properties.API.WebService.ONVIF.Version=1.02
root.Properties.API.WebSocket.RTSP.RTSP=yes
root.Properties.ApiDiscovery.ApiDiscovery=yes
root.Properties.Audio.Audio=yes
root.Properties.Audio.DuplexMode=half,post,get
root.Properties.Audio.Format=lpcm,g711,g726,aac,opus
root.Properties.Audio.InputType=internal
root.Properties.Audio.Decoder.Format=g711,g726,axis-mulaw-128
root.Properties.Audio.Source.A0.Input=yes
root.Properties.Audio.Source.A0.Output=yes
root.Properties.EmbeddedDevelopment.CacheSize=76546048
root.Properties.EmbeddedDevelopment.DefaultCacheSize=92274688
root.Properties.EmbeddedDevelopment.EmbeddedDevelopment=yes
root.Properties.EmbeddedDevelopment.Version=2.16
root.Properties.EmbeddedDevelopment.RuleEngine.MultiConfiguration=yes
root.Properties.Firmware.BuildDate=Feb 15 2019 09:42
root.Properties.Firmware.BuildNumber=26
root.Properties.Firmware.Version=9.10.1
root.Properties.FirmwareManagement.Version=1.0
root.Properties.GuardTour.GuardTour=yes
root.Properties.GuardTour.MaxGuardTours=100
root.Properties.GuardTour.MinGuardTourWaitTime=10
root.Properties.GuardTour.RecordedTour=no
root.Properties.HTTPS.HTTPS=yes
root.Properties.Image.Format=jpeg,mjpeg,h264
root.Properties.Image.NbrOfViews=2
root.Properties.Image.Resolution=1920x1080,1280x960,1280x720,1024x768,1024x576,800x600,640x480,640x360,352x240,320x240
root.Properties.Image.Rotation=0,180
root.Properties.Image.ShowSuboptimalResolutions=false
root.Properties.Image.H264.Profiles=Baseline,Main,High
root.Properties.ImageSource.DayNight=yes
root.Properties.IO.ManualTriggerNbr=6
root.Properties.LEDControl.LEDControl=yes
root.Properties.LightControl.LightControl2=yes
root.Properties.LightControl.LightControlAvailable=yes
root.Properties.LocalStorage.AutoRepair=yes
root.Properties.LocalStorage.ContinuousRecording=yes
root.Properties.LocalStorage.DiskEncryption=yes
root.Properties.LocalStorage.DiskHealth=yes
root.Properties.LocalStorage.ExportRecording=yes
root.Properties.LocalStorage.FailOverRecording=yes
root.Properties.LocalStorage.LocalStorage=yes
root.Properties.LocalStorage.NbrOfContinuousRecordingProfiles=1
root.Properties.LocalStorage.RequiredFileSystem=yes
root.Properties.LocalStorage.SDCard=yes
root.Properties.LocalStorage.StorageLimit=yes
root.Properties.LocalStorage.Version=1.00
root.Properties.Motion.MaxNbrOfWindows=10
root.Properties.Motion.Motion=yes
root.Properties.Network.WLAN.WLANScan2=yes
root.Properties.NetworkShare.CIFS=yes
root.Properties.NetworkShare.IPV6=yes
root.Properties.NetworkShare.NameLookup=yes
root.Properties.NetworkShare.NetworkShare=yes
root.Properties.PackageManager.FormatListing=yes
root.Properties.PackageManager.LicenseKeyManagement=yes
root.Properties.PackageManager.PackageManager=yes
root.Properties.PrivacyMask.MaxNbrOfPrivacyMasks=10
root.Properties.PrivacyMask.Polygon=no
root.Properties.PrivacyMask.PrivacyMask=no
root.Properties.PrivacyMask.Query=list,position,listpxjson,positionpxjson
root.Properties.PTZ.DigitalPTZ=yes
root.Properties.PTZ.DriverManagement=no
root.Properties.PTZ.DriverModeList=none
root.Properties.PTZ.PTZ=yes
root.Properties.PTZ.PTZOnQuadView=no
root.Properties.PTZ.SelectableDriverMode=no
root.Properties.RemoteService.RemoteService=no
root.Properties.RTC.RTC=yes
root.Properties.Sensor.PIR=yes
root.Properties.Serial.Serial=no
root.Properties.System.Architecture=armv7hf
root.Properties.System.HardwareID=70E
root.Properties.System.Language=English
root.Properties.System.LanguageType=default
root.Properties.System.SerialNumber=ACCC12345678
root.Properties.System.Soc=Ambarella S2L (Flattened Device Tree)
root.Properties.Tampering.Tampering=yes
root.Properties.TemperatureSensor.Fan=no
root.Properties.TemperatureSensor.Heater=no
root.Properties.TemperatureSensor.TemperatureControl=yes
root.Properties.TemperatureSensor.TemperatureSensor=yes
root.Properties.VirtualInput.VirtualInput=yes
root.Properties.ZipStream.ZipStream=yes"""

response_param_cgi_ptz = """root.PTZ.BoaProtPTZOperator=password
root.PTZ.CameraDefault=1
root.PTZ.NbrOfCameras=1
root.PTZ.NbrOfSerPorts=1
root.PTZ.CamPorts.Cam1Port=1
root.PTZ.ImageSource.I0.PTZEnabled=true
root.PTZ.Limit.L1.MaxBrightness=9999
root.PTZ.Limit.L1.MaxFieldAngle=623
root.PTZ.Limit.L1.MaxFocus=9999
root.PTZ.Limit.L1.MaxIris=9999
root.PTZ.Limit.L1.MaxPan=170
root.PTZ.Limit.L1.MaxTilt=90
root.PTZ.Limit.L1.MaxZoom=9999
root.PTZ.Limit.L1.MinBrightness=1
root.PTZ.Limit.L1.MinFieldAngle=22
root.PTZ.Limit.L1.MinFocus=770
root.PTZ.Limit.L1.MinIris=1
root.PTZ.Limit.L1.MinPan=-170
root.PTZ.Limit.L1.MinTilt=-20
root.PTZ.Limit.L1.MinZoom=1
root.PTZ.Preset.P0.HomePosition=1
root.PTZ.Preset.P0.ImageSource=0
root.PTZ.Preset.P0.Name=
root.PTZ.Preset.P0.Position.P1.Data=tilt=0.000000:focus=32766.000000:pan=0.000000:iris=32766.000000:zoom=1.000000
root.PTZ.Preset.P0.Position.P1.Name=Home
root.PTZ.PTZDriverStatuses.Driver1Status=3
root.PTZ.SerDriverStatuses.Ser1Status=3
root.PTZ.Support.S1.AbsoluteBrightness=true
root.PTZ.Support.S1.AbsoluteFocus=true
root.PTZ.Support.S1.AbsoluteIris=true
root.PTZ.Support.S1.AbsolutePan=true
root.PTZ.Support.S1.AbsoluteTilt=true
root.PTZ.Support.S1.AbsoluteZoom=true
root.PTZ.Support.S1.ActionNotification=true
root.PTZ.Support.S1.AreaZoom=true
root.PTZ.Support.S1.AutoFocus=true
root.PTZ.Support.S1.AutoIrCutFilter=true
root.PTZ.Support.S1.AutoIris=true
root.PTZ.Support.S1.Auxiliary=true
root.PTZ.Support.S1.BackLight=true
root.PTZ.Support.S1.ContinuousBrightness=false
root.PTZ.Support.S1.ContinuousFocus=true
root.PTZ.Support.S1.ContinuousIris=false
root.PTZ.Support.S1.ContinuousPan=true
root.PTZ.Support.S1.ContinuousTilt=true
root.PTZ.Support.S1.ContinuousZoom=true
root.PTZ.Support.S1.DevicePreset=false
root.PTZ.Support.S1.DigitalZoom=true
root.PTZ.Support.S1.GenericHTTP=false
root.PTZ.Support.S1.IrCutFilter=true
root.PTZ.Support.S1.JoyStickEmulation=true
root.PTZ.Support.S1.LensOffset=false
root.PTZ.Support.S1.OSDMenu=false
root.PTZ.Support.S1.ProportionalSpeed=true
root.PTZ.Support.S1.RelativeBrightness=true
root.PTZ.Support.S1.RelativeFocus=true
root.PTZ.Support.S1.RelativeIris=true
root.PTZ.Support.S1.RelativePan=true
root.PTZ.Support.S1.RelativeTilt=true
root.PTZ.Support.S1.RelativeZoom=true
root.PTZ.Support.S1.ServerPreset=true
root.PTZ.Support.S1.SpeedCtl=true
root.PTZ.UserAdv.U1.AdjustableZoomSpeedEnabled=true
root.PTZ.UserAdv.U1.DeviceModVer=model:0467, version:0310
root.PTZ.UserAdv.U1.DeviceStatus=cam=ok,pan=ok,tilt=ok
root.PTZ.UserAdv.U1.LastTestDate=Thu Oct 29 08:12:04 2020
root.PTZ.UserAdv.U1.MoveSpeed=100
root.PTZ.UserAdv.U1.WhiteBalanceOnePushModeEnabled=true
root.PTZ.UserCtlQueue.U0.Priority=10
root.PTZ.UserCtlQueue.U0.TimeoutTime=60
root.PTZ.UserCtlQueue.U0.TimeoutType=activity
root.PTZ.UserCtlQueue.U0.UseCookie=yes
root.PTZ.UserCtlQueue.U0.UserGroup=Administrator
root.PTZ.UserCtlQueue.U1.Priority=30
root.PTZ.UserCtlQueue.U1.TimeoutTime=60
root.PTZ.UserCtlQueue.U1.TimeoutType=activity
root.PTZ.UserCtlQueue.U1.UseCookie=yes
root.PTZ.UserCtlQueue.U1.UserGroup=Operator
root.PTZ.UserCtlQueue.U2.Priority=50
root.PTZ.UserCtlQueue.U2.TimeoutTime=60
root.PTZ.UserCtlQueue.U2.TimeoutType=timespan
root.PTZ.UserCtlQueue.U2.UseCookie=yes
root.PTZ.UserCtlQueue.U2.UserGroup=Viewer
root.PTZ.UserCtlQueue.U3.Priority=20
root.PTZ.UserCtlQueue.U3.TimeoutTime=20
root.PTZ.UserCtlQueue.U3.TimeoutType=activity
root.PTZ.UserCtlQueue.U3.UseCookie=no
root.PTZ.UserCtlQueue.U3.UserGroup=Event
root.PTZ.UserCtlQueue.U4.Priority=35
root.PTZ.UserCtlQueue.U4.TimeoutTime=60
root.PTZ.UserCtlQueue.U4.TimeoutType=infinity
root.PTZ.UserCtlQueue.U4.UseCookie=no
root.PTZ.UserCtlQueue.U4.UserGroup=Autotracking
root.PTZ.UserCtlQueue.U5.Priority=0
root.PTZ.UserCtlQueue.U5.TimeoutTime=60
root.PTZ.UserCtlQueue.U5.TimeoutType=infinity
root.PTZ.UserCtlQueue.U5.UseCookie=no
root.PTZ.UserCtlQueue.U5.UserGroup=Onvif
root.PTZ.Various.V1.AutoFocus=true
root.PTZ.Various.V1.AutoIris=true
root.PTZ.Various.V1.BackLight=false
root.PTZ.Various.V1.BackLightEnabled=true
root.PTZ.Various.V1.BrightnessEnabled=true
root.PTZ.Various.V1.CtlQueueing=false
root.PTZ.Various.V1.CtlQueueLimit=20
root.PTZ.Various.V1.CtlQueuePollTime=20
root.PTZ.Various.V1.FocusEnabled=true
root.PTZ.Various.V1.HomePresetSet=true
root.PTZ.Various.V1.IrCutFilter=auto
root.PTZ.Various.V1.IrCutFilterEnabled=true
root.PTZ.Various.V1.IrisEnabled=true
root.PTZ.Various.V1.MaxProportionalSpeed=200
root.PTZ.Various.V1.PanEnabled=true
root.PTZ.Various.V1.ProportionalSpeedEnabled=true
root.PTZ.Various.V1.PTZCounter=8
root.PTZ.Various.V1.ReturnToOverview=0
root.PTZ.Various.V1.SpeedCtlEnabled=true
root.PTZ.Various.V1.TiltEnabled=true
root.PTZ.Various.V1.ZoomEnabled=true"""
