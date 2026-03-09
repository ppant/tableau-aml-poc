import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_data", required=True)
    args = parser.parse_args()

    input_path = Path(args.input_data)
    print(f"Pipeline received input: {input_path}")


if __name__ == "__main__":
    main()
