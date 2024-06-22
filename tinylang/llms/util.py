import os


def get_api_key(api_key: str | None, os_variable: str) -> str:
    if not api_key and not os.getenv(os_variable):
        raise ValueError(
            f"{os_variable} is required, either pass it as an argument or set it as an environment variable as {os_variable}=YOUR_API_KEY"
        )

    return api_key or os.getenv(os_variable)  # type: ignore
