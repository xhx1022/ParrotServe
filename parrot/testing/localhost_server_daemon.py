# Copyright (c) 2023 by Microsoft Corporation.
# Licensed under the MIT license.


"""Start specific daemon servers in localhost for testing.

The server daemon will run in a separate process created by the lib Python multiprocessing.
"""


import contextlib
from multiprocessing import Process
import uvicorn
import time

from parrot.constants import (
    DEFAULT_SERVER_HOST,
    DEFAULT_OS_SERVER_PORT,
    DEFAULT_ENGINE_SERVER_PORT,
)

from parrot.os.http_server import start_server as start_os_server
from parrot.engine.http_server import start_server as start_engine_server

from .get_configs import get_sample_engine_config_path, get_sample_os_config_path
from .fake_engine_server import app as FakeEngineApp
from .fake_os_server import app as FakeOSApp


@contextlib.contextmanager
def fake_os_server():
    def _launch_fake_os():
        uvicorn.run(
            FakeOSApp,
            host=DEFAULT_SERVER_HOST,
            port=DEFAULT_OS_SERVER_PORT,
            log_level="info",
        )

    p = Process(target=_launch_fake_os, daemon=True)
    p.start()
    time.sleep(0.1)

    yield

    p.terminate()
    time.sleep(0.1)


@contextlib.contextmanager
def fake_engine_server():
    def _launch_fake_engine():
        uvicorn.run(
            FakeEngineApp,
            host=DEFAULT_SERVER_HOST,
            port=DEFAULT_ENGINE_SERVER_PORT,
            log_level="info",
        )

    p = Process(target=_launch_fake_engine, daemon=True)
    p.start()
    time.sleep(0.1)

    yield

    p.terminate()
    time.sleep(0.1)


@contextlib.contextmanager
def os_server():
    def _launch_os():
        os_config_path = get_sample_os_config_path("localhost_os.json")
        release_mode = False

        start_os_server(os_config_path=os_config_path, release_mode=release_mode)

    p = Process(target=_launch_os, daemon=True)
    p.start()
    time.sleep(0.1)

    yield

    p.terminate()
    time.sleep(0.1)


@contextlib.contextmanager
def engine_server(
    engine_config_name: str,
    wait_ready_time: float = 0.1,
    connect_to_os: bool = False,
):
    def _launch_engine():
        engine_config_path = get_sample_engine_config_path(engine_config_name)
        start_engine_server(
            engine_config_path=engine_config_path, connect_to_os=connect_to_os
        )

    p = Process(target=_launch_engine, daemon=True)
    p.start()
    time.sleep(wait_ready_time)

    yield

    p.terminate()
    time.sleep(0.1)


@contextlib.contextmanager
def system_opt():
    with os_server():
        with engine_server(
            engine_config_name="opt-125m.json",
            wait_ready_time=3.0,
            connect_to_os=True,
        ):
            yield


@contextlib.contextmanager
def system_vicuna():
    with os_server():
        with engine_server(
            engine_config_name="vicuna-7b-v1.3.json",
            wait_ready_time=5.0,
            connect_to_os=True,
        ):
            yield


@contextlib.contextmanager
def system_vicuna_vllm():
    with os_server():
        with engine_server(
            engine_config_name="vicuna-7b-v1.3-vllm.json",
            wait_ready_time=5.0,
            connect_to_os=True,
        ):
            yield


@contextlib.contextmanager
def system_mlcllm():
    with os_server():
        with engine_server(
            engine_config_name="Llama-2-13b-chat-hf-q4f16_1-vulkan.json",
            wait_ready_time=3.0,
            connect_to_os=True,
        ):
            yield


@contextlib.contextmanager
def system_openai():
    with os_server():
        with engine_server(
            engine_config_name="azure-openai-gpt-3.5-turbo.json",
            wait_ready_time=3.0,
            connect_to_os=True,
        ):
            yield
