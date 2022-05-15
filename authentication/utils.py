from random import choice


def generate_OTP(length: int = 6):
    """
    Generates a random OTP of given length.
    """
    return "".join(choice("0123456789") for _ in range(length))
