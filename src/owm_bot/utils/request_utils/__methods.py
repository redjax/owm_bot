from __future__ import annotations

import logging
import typing as t

log = logging.getLogger("owm_bot.utils.request_utils")

import typing

import httpx

def build_request(
    method: str = "GET",
    url: str = None,
    files: list | None = None,
    data: t.Any | None = None,
    content: bytes | None = None,
    params: dict | None = None,
    headers: dict | None = None,
    cookies: dict | None = None,
    stream: t.Union[httpx.SyncByteStream, httpx.AsyncByteStream] | None = None,
    extensions: dict | None = None,
) -> httpx.Request:
    """Build an `httpx.Request()` object from inputs.

    Params:
        method (str): (default="GET") The HTTP method for the request.
        url (str): The URL to send request to.
        files (list): List of files to send with request.
        data (Any): <UNDOCUMENTED>
        contents (bytes): Byte-encoded request content.
        params (dict): URL params for request. Pass each param as a key/value pair, like:
            `{"api_key": api_key, "days": 15, "page": 2}`
        headers (dict): Headers for request.
        cookies (dict): Cookies for request.
        extensions (dict): Extensions for request. Example: `{"timeout": {"connect": 5.0}}`.
        stream (httpx.SyncByteStream | httpx.AsyncByteSTream): <UNDOCUMENTED>
    """
    _request: httpx.Request = httpx.Request(
        method=method,
        url=url,
        params=params,
        headers=headers,
        cookies=cookies,
        content=content,
        data=data,
        files=files,
        extensions=extensions,
        stream=stream,
    )

    return _request
