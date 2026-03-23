import os
import subprocess
import sys

def main():
    # Expected to be run from the 'sites' directory of frappe-bench
    if not os.path.exists("common_site_config.json"):
        print("Please run this script from the 'sites' directory of your bench.")
        print("Example: cd sites && ../env/bin/python ../apps/maxedu/maxedu/test_data/run_all.py")
        sys.exit(1)

    test_scripts = [
        "create_leave_data.py",
        "create_notice_data.py",
        "create_routine_generator.py",
        "create_test_data_routine.py",
        "create_sc_12_data.py"
    ]

    base_path = "../apps/maxedu/maxedu/test_data"
    python_bin = "../env/bin/python"

    print("==========================================")
    print("Running All MaxEdu Test Data Scripts")
    print("==========================================\n")

    for script in test_scripts:
        script_path = os.path.join(base_path, script)
        if not os.path.exists(script_path):
            print(f"[SKIPPED] Cannot find {script_path}")
            continue

        print(f"--> Executing {script} ...")
        result = subprocess.run([python_bin, script_path], capture_output=False, text=True)
        
        if result.returncode == 0:
            print(f"[SUCCESS] {script} ran without errors.\n")
        else:
            print(f"[FAILED] {script} encountered an error (exit code: {result.returncode}).\n")

    print("==========================================")
    print("Done executing test scripts.")
    print("==========================================")

if __name__ == "__main__":
    main()
