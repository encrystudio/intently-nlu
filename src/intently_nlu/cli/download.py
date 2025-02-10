"""Download CLI"""

import os

from platformdirs import user_data_dir

from intently_nlu.__about__ import __resource_location__
from intently_nlu.exceptions import ResourceError
from intently_nlu.util.language import is_valid_supported_language_code
from intently_nlu.util.resources import check_for_resource


def add_download_parser(subparsers, formatter_class) -> None:  # type: ignore
    """Add the `download` subcommand"""
    subparser = subparsers.add_parser(  # type: ignore
        "download",
        formatter_class=formatter_class,
        help="Download resources.",
    )
    subparser.add_argument("resources", nargs="+", type=str, help="Resource(s) to download")  # type: ignore
    subparser.set_defaults(func=_download)  # type: ignore


def _download(args_namespace) -> None:  # type: ignore
    download(args_namespace.resources)  # type: ignore


def download(resources: list[str]) -> None:
    """Checks if resources exists or download them

    Args:
        resources (list[str]): The resources to download
    """
    for resource in resources:
        if is_valid_supported_language_code(resource):
            resource = f"languages/{resource}.json"
        try:
            check_for_resource(resource)
            print(f"'{resource}' is already installed.")
            continue
        except ResourceError:
            print(f"Try to install '{resource}'...")
            # pylint: disable=import-outside-toplevel
            from pathlib import Path

            import requests

            try:
                response = requests.get(
                    __resource_location__ + resource, stream=True, timeout=10
                )
                path = Path(
                    os.path.join(
                        user_data_dir(appname="intently-nlu", appauthor="encrystudio"),
                        "resources",
                        resource.replace("/", os.sep),
                    )
                )
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
                with path.open("w", encoding="utf-8") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk.decode("utf-8"))
                print(f"Try to install '{resource}'...Done!")
            except requests.exceptions.RequestException as e:
                print(f"Error downloading '{resource}':", e)

            print("\nDownload complete.")
