from parrot.os.tokenizer import Tokenizer


TESTING_PROMPT_TEXT = (
    "He is widely acknowledged as one of the top achievers in his class"
)
TESTING_TOKEN_IDS = [
    940,
    338,
    17644,
    24084,
    3192,
    408,
    697,
    310,
    278,
    2246,
    3657,
    347,
    874,
    297,
    670,
    770,
]


def test_encode():
    tokenizer = Tokenizer()
    tokenizer_name = "hf-internal-testing/llama-tokenizer"

    encoded = tokenizer.tokenize(TESTING_PROMPT_TEXT, tokenizer_name)

    # print(encoded)
    assert encoded == TESTING_TOKEN_IDS


def test_decode():
    tokenizer = Tokenizer()
    tokenizer_name = "hf-internal-testing/llama-tokenizer"

    decoded = tokenizer.detokenize(TESTING_TOKEN_IDS, tokenizer_name)

    assert TESTING_PROMPT_TEXT == decoded


if __name__ == "__main__":
    test_encode()
    test_decode()
