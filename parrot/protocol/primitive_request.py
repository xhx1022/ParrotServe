from dataclasses import dataclass, asdict
from typing import List, Optional
import aiohttp

from parrot.constants import NONE_THREAD_ID

from .common import (
    send_http_request,
    async_send_http_request,
    async_send_http_request_streaming,
    logger,
)
from .sampling_config import SamplingConfig
from .responses import FillResponse, GenerateResponse


@dataclass
class Primitive:
    """Base class for LLM primitives."""

    pid: int
    tid: int
    context: "Context"


@dataclass
class Fill(Primitive):
    """Fill primitive is corresponding to the `prefill` stage in LLM.

    Its mission is to fill the KV cache in the execution engine, extending the context
    using the input tokens.
    """

    token_ids: Optional[List[int]] = None
    text: Optional[str] = None

    def post(self, http_addr: str) -> FillResponse:
        # NOTE(chaofan): For simple fill, there is no thread id.
        assert self.tid == NONE_THREAD_ID

        try:
            resp: FillResponse = send_http_request(
                FillResponse,
                http_addr,
                "/fill",
                retry_times=1,
                pid=self.pid,
                tid=self.tid,
                context_id=self.context.context_id,
                parent_context_id=self.context.parent_context_id,
                token_ids=self.token_ids,
                text=self.text,
            )
            self.context.token_nums += resp.num_filled_tokens
            return resp
        except BaseException as e:
            logger.error(f"Fill error in {http_addr} error: {e}")
            raise e

    async def apost(self, http_addr: str) -> FillResponse:
        # NOTE: For thread fill, there is a thread id.
        assert self.tid != NONE_THREAD_ID

        try:
            async with aiohttp.ClientSession() as client_session:
                resp: FillResponse = await async_send_http_request(
                    client_session,
                    FillResponse,
                    http_addr,
                    "/fill",
                    pid=self.pid,
                    tid=self.tid,
                    context_id=self.context.context_id,
                    parent_context_id=self.context.parent_context_id,
                    token_ids=self.token_ids,
                    text=self.text,
                )
            self.context.token_nums += resp.num_filled_tokens
            return resp
        except BaseException as e:
            logger.error(f"Fill error in {http_addr} error: {e}")
            raise e


@dataclass
class Generate(Primitive):
    """Generate primitive is corresponding to the `decode` stage in LLM.

    Its mission is to generate the output tokens based on certain context.
    """

    sampling_config: SamplingConfig

    async def apost(self, http_addr: str) -> GenerateResponse:
        try:
            async with aiohttp.ClientSession() as client_session:
                resp: GenerateResponse = await async_send_http_request(
                    client_session,
                    GenerateResponse,
                    http_addr,
                    "/generate",
                    pid=self.pid,
                    tid=self.tid,
                    context_id=self.context.context_id,
                    parent_context_id=self.context.parent_context_id,
                    sampling_config=asdict(self.sampling_config),
                )
                self.context.token_nums += len(resp.generated_ids)
                return resp
        except BaseException as e:
            logger.error(f"Generate error in {http_addr} error: {e}")
            raise e

    async def astream(self, http_addr: str):
        try:
            async with aiohttp.ClientSession() as client_session:
                async for resp in async_send_http_request_streaming(
                    client_session,
                    http_addr,
                    "/generate_stream",
                    pid=self.pid,
                    tid=self.tid,
                    context_id=self.context.context_id,
                    parent_context_id=self.context.parent_context_id,
                    sampling_config=asdict(self.sampling_config),
                ):
                    self.context.token_nums += 1
                    yield resp
        except BaseException as e:
            logger.error(f"Generate error in {http_addr} error: {e}")
            raise e
