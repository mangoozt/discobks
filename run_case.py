import contextlib
import ctypes
import json
import logging
import os
import subprocess
import tempfile
import time


def fix_return_code(code):
    return ctypes.c_int32(code).value


@contextlib.contextmanager
def remember_cwd():
    cur_dir = os.getcwd()
    try:
        yield
    finally:
        os.chdir(cur_dir)


def make_usv_files(case_data):
    for k in case_data:
        with open(f'{k}', 'w') as f:
            json.dump(case_data[k], f)


def run_executable(exe):
    command = [exe, "--target-settings", "target-settings",
               "--targets", "targets",
               "--settings", "settings",
               "--nav-data", "nav-data",
               "--hydrometeo", "hydrometeo",
               "--constraints", "constraints",
               "--route", "route",
               "--maneuver", "maneuver",
               "--analyse", "analyse",
               "--predict", "predict"]

    completed_proc = None
    try:
        completed_proc = subprocess.run(command,
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        stdin=subprocess.PIPE, timeout=35)
        code = fix_return_code(completed_proc.returncode)
    # Added to prevent freezing
    except subprocess.TimeoutExpired:
        code = 6

    return code, completed_proc.stdout


def run_case(exe, case_data):
    with tempfile.TemporaryDirectory() as temp_dir, remember_cwd() as _:
        os.chdir(temp_dir)

        make_usv_files(case_data)

        run_executable(exe)

        ret_dict = {}
        try:
            with open("maneuver") as f:
                ret_dict['maneuver'] = json.load(f)
            with open("analyse") as f:
                ret_dict['analyse'] = json.load(f)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            return None
        return ret_dict


def test_usv(executable):
    with open("situation.json") as f:
        diction_case = json.load(f)
    res = run_case(executable, diction_case)
    with open("result.json", "w") as f:
        json.dump(res, f)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="BKS report generator")
    parser.add_argument("executable", type=str, help="Path to USV executable")
    parser.add_argument("--working_dir", type=str, help="Path to situation.json")

    args, extra_args = parser.parse_known_args()

    usv_executable = os.path.abspath(args.executable)

    logging.info("Start running cases...")
    time_start = time.time()
    test_usv(usv_executable)

    logging.info(f'Finished in {time.time() - time_start} sec')
