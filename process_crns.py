import subprocess

def run_command(command):
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode().strip()
        print(f"Output:\n{output}\n")
        return True  # command succeeded
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {command}")
        print(e.stderr.decode().strip())
        return False  # command failed

def process_crns(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines:
        crn = line.strip()
        if not crn or not crn.startswith("crn:"):
            continue

        print(f"\n============================")
        print(f"Processing CRN:\n{crn}")
        print(f"============================")

        # Step 1: icdctl dl <crn>
        if not run_command(f"icdctl dl '{crn}'"):
            print("Skipping remaining steps for this CRN due to failure in setting context.\n")
            continue

        # Step 2: icdctl formation
        if not run_command("icdctl formation"):
            print("Skipping REOL exemption due to failure in formation fetch.\n")
            continue

        # Step 3: Apply REOL exemption
        if not run_command('icdctl formation-lifecycle reol exempt 49990 --until "2025-08-13T23:59:59z"'):
            print("REOL exemption failed.\n")
            continue

        # Step 4: Validate again
        run_command("icdctl formation")

if __name__ == "__main__":
    process_crns("crns.txt")
