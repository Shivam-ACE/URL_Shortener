ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode_id(n: int) -> str:
    if n == 0:
        return ALPHABET[0]

    chars = []
    while n > 0:
        remainder = n % 62
        chars.append(ALPHABET[remainder])
        n //= 62

    chars.reverse()
    return "".join(chars)
