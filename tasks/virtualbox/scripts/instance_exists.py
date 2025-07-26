#!/usr/bin/env python3

from sys import exit
from argparse import ArgumentParser
from subprocess import run
from re import sub


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--not-exists", action="store_true")
    parser.add_argument("instance")
    return parser.parse_args()


def list_instances():
    result = run(
        args=["VBoxManage", "list", "vms"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [sub(r'^"(.+)".*', "\\g<1>", line) for line in result.stdout.splitlines()]


def inverse_status(status):
    return (status + 1) % 2


def main():
    args = parse_args()
    status = 0 if args.instance in list_instances() else 1
    if args.not_exists:
        status = inverse_status(status)
    exit(status)


if __name__ == "__main__":
    main()
