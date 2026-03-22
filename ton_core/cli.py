import argparse

from ton_core.__meta__ import __version__


def main() -> None:
    """CLI entry-point."""
    parser = argparse.ArgumentParser(
        prog="ton-core",
        description="TON Core CLI.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"ton-core {__version__}",
    )
    parser.parse_args()


if __name__ == "__main__":
    main()
