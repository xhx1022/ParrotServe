from typing import List, Optional
from asyncio import Event

from ..program.placeholder import Placeholder
from ..orchestration.tokenize import TokenizedStorage


class TokensHolder:
    """Placeholder stores the text while TokensHolder stores the tokenized ids.

    Hence it's tokenizer-related.
    """

    def __init__(
        self,
        tokenizer: str,
        tokenized_storage: TokenizedStorage,
        placeholder: Optional[Placeholder] = None,
    ):
        # ---------- Basic info ----------
        self.token_ids: Optional[List[int]] = None
        self.tokenized_storage = tokenized_storage
        self.tokenizer: str = tokenizer
        self.placeholder = placeholder

        # ---------- Jobs ----------
        self.consumers: List["FillJob"] = []
        self.producer: Optional["GenerationJob"] = None

        # ---------- Events ----------
        self.streaming_event: Event = Event()
        self.ready_event: Event = Event()

        if placeholder is not None:
            self.placeholder.assign_callbacks.append(
                self.sync_from_placeholder
            )  # Add callback
            if placeholder.ready:
                self.sync_from_placeholder()

    @property
    def ready(self) -> bool:
        return self.ready_event.is_set()

    @property
    def is_constant(self) -> bool:
        return self.placeholder is None

    def assign(self, token_ids: List[int]):
        assert not self.ready, "This tokenholder is filled. Can't assign."
        assert (
            not self.streaming_event.is_set()
        ), "This tokeholder is streaming. Can't assign."

        self.token_ids = token_ids
        self.ready_event.set()
        # NOTE(chaofan): When it has data, also set the streaming event.
        self.streaming_event.set()

    def sync_from_placeholder(self):
        assert self.placeholder is not None, "No placeholder"
        assert self.placeholder.ready, "Placeholder not ready"
        assert self.tokenized_storage is not None, "No tokenized storage"
        self.assign(
            self.tokenized_storage.tokenize(
                self.placeholder.content,
                self.tokenizer,
            )
        )

    def sync_to_placeholder_partial(
        self, token_ids: List[int], prev_last_token: Optional[int]
    ):
        assert self.placeholder is not None, "No placeholder"
        assert self.tokenized_storage is not None, "No tokenized storage"

        if self.placeholder.content is None:
            self.placeholder.content = ""

        if prev_last_token:
            token_ids = [prev_last_token] + token_ids
            prev_last_text = self.tokenized_storage.detokenize(
                [prev_last_token],
                self.tokenizer,
            )

        partial_text = self.tokenized_storage.detokenize(
            token_ids,
            self.tokenizer,
        )

        if prev_last_token:
            partial_text = partial_text[len(prev_last_text) :]

        self.placeholder.content += partial_text

    def __str__(self) -> str:
        if self.is_constant:
            return f"[TokensHolder(Constant): {self.token_ids}]"
        return f"[TokensHolder(Placeholder): {self.placeholder.name}]"

    def send_token(self, token_id: int, put_into_holder: bool = True):
        assert self.streaming_event.is_set(), "This tokenholder is not streaming."
        assert not self.ready, "This tokenholder is filled. Can't send token."

        # Pushing to output holder
        if put_into_holder:
            self.token_ids.append(token_id)

        # Routing to pipes
        for consumer in self.consumers:
            consumer.input_pipe.queue.put_nowait(token_id)
        assert self.producer is not None, "No producer"
        self.producer.detokenize_pipe.queue.put_nowait(token_id)
