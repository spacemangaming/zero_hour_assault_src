import os
import sys
import re
import subprocess
import urllib.request
import json
import ssl

# ANSI Colors
C_BLUE = "\033[94m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_CYAN = "\033[96m"
C_RESET = "\033[0m"
C_BOLD = "\033[1m"

def print_header():
    print("\033[H\033[2J", end="")
    print(f"{C_BLUE}{C_BOLD}==================================================={C_RESET}")
    print(f"{C_CYAN}{C_BOLD}        ZERO HOUR ASSAULT DEVELOPER TOOL          {C_RESET}")
    print(f"{C_BLUE}{C_BOLD}==================================================={C_RESET}")

def run_command(command, shell=True):
    try:
        result = subprocess.run(command, shell=shell, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"{C_RED}Error running command: {e}{C_RESET}")
        return False

def get_current_versions():
    versions = {}
    
    # Read globals.py
    globals_path = os.path.join("src", "zero_hour_assault", "core", "globals.py")
    if os.path.exists(globals_path):
        with open(globals_path, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'ver\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                versions["globals.py"] = match.group(1)
    
    # Read buildozer.spec
    spec_path = "buildozer.spec"
    if os.path.exists(spec_path):
        with open(spec_path, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'version\s*=\s*([^\s#]+)', content)
            if match:
                versions["buildozer.spec"] = match.group(1)
                
    # Read pyproject.toml
    toml_path = "pyproject.toml"
    if os.path.exists(toml_path):
        with open(toml_path, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                versions["pyproject.toml"] = match.group(1)
                
    return versions

def update_versions():
    versions = get_current_versions()
    print(f"\n{C_YELLOW}Current Detected Versions:{C_RESET}")
    for file, ver in versions.items():
        print(f"  - {C_CYAN}{file}{C_RESET}: {C_GREEN}{ver}{C_RESET}")
        
    new_ver = input(f"\nEnter new version (e.g. 1.6.0): ").strip()
    if not new_ver:
        print(f"{C_RED}Cancelled version update.{C_RESET}")
        return
    
    # Update globals.py
    globals_path = os.path.join("src", "zero_hour_assault", "core", "globals.py")
    if os.path.exists(globals_path):
        with open(globals_path, "r", encoding="utf-8") as f:
            content = f.read()
        new_content = re.sub(r'(ver\s*=\s*["\'])([^"\']+)(["\'])', rf'\g<1>{new_ver}\g<3>', content)
        with open(globals_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"{C_GREEN}✓ Updated src/zero_hour_assault/core/globals.py{C_RESET}")
    else:
        print(f"{C_RED}✗ globals.py not found{C_RESET}")
        
    # Update buildozer.spec
    spec_path = "buildozer.spec"
    if os.path.exists(spec_path):
        with open(spec_path, "r", encoding="utf-8") as f:
            content = f.read()
        new_content = re.sub(r'(version\s*=\s*)([^\s#]+)', rf'\g<1>{new_ver}', content)
        with open(spec_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"{C_GREEN}✓ Updated buildozer.spec{C_RESET}")
    else:
        print(f"{C_RED}✗ buildozer.spec not found{C_RESET}")
        
    # Update pyproject.toml
    toml_path = "pyproject.toml"
    if os.path.exists(toml_path):
        with open(toml_path, "r", encoding="utf-8") as f:
            content = f.read()
        new_content = re.sub(r'(version\s*=\s*["\'])([^"\']+)(["\'])', rf'\g<1>{new_ver}\g<3>', content)
        with open(toml_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"{C_GREEN}✓ Updated pyproject.toml{C_RESET}")
    else:
        print(f"{C_RED}✗ pyproject.toml not found{C_RESET}")
        
    print(f"\n{C_GREEN}Success! Version bumped to {new_ver} across all files.{C_RESET}")

def run_client():
    print(f"\n{C_YELLOW}Launching game client...{C_RESET}")
    python_exe = os.path.join(".venv", "Scripts", "python.exe")
    if not os.path.exists(python_exe):
        python_exe = "python"
    
    main_file = os.path.join("src", "zero_hour_assault", "zero_hour_assault.py")
    if not os.path.exists(main_file):
        main_file = "main.py"
        
    run_command(f'"{python_exe}" "{main_file}"')

def run_server():
    print(f"\n{C_YELLOW}Launching server in a new window...{C_RESET}")
    python_exe = os.path.join(".venv", "Scripts", "python.exe")
    if not os.path.exists(python_exe):
        python_exe = "python"
        
    server_file = os.path.join("server", "zhaserver.py")
    if not os.path.exists(server_file):
        print(f"{C_RED}✗ Server file not found.{C_RESET}")
        return
        
    # Launch in a new command prompt window that stays open
    cmd = f'start cmd /k ""{python_exe}" "{server_file}""'
    run_command(cmd)
    print(f"{C_GREEN}Server window launched.{C_RESET}")

def compile_pc():
    print(f"\n{C_YELLOW}Compiling PC Client (Running build_pc.py)...{C_RESET}")
    python_exe = os.path.join(".venv", "Scripts", "python.exe")
    if not os.path.exists(python_exe):
        python_exe = "python"
        
    run_command(f'"{python_exe}" build_pc.py')

def git_push():
    print(f"\n{C_YELLOW}Staging files...{C_RESET}")
    run_command("git add buildozer.spec .github/workflows/build.yml src/zero_hour_assault/core/globals.py pyproject.toml")
    
    commit_msg = input(f"\nEnter commit message: ").strip()
    if not commit_msg:
        print(f"{C_RED}Commit message cannot be empty. Cancelled git push.{C_RESET}")
        return
        
    print(f"\n{C_YELLOW}Committing...{C_RESET}")
    if run_command(f'git commit -m "{commit_msg}"'):
        print(f"\n{C_YELLOW}Pushing to origin/main (to trigger CI/CD)...{C_RESET}")
        run_command("git push origin main")
    else:
        print(f"{C_RED}Nothing to commit or commit failed.{C_RESET}")

def check_actions():
    print(f"\n{C_YELLOW}Fetching latest GitHub Actions run status...{C_RESET}")
    url = "https://api.github.com/repos/spacemangaming/zero_hour_assault_src/actions/runs"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    ssl_ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=ssl_ctx) as response:
            data = json.loads(response.read().decode())
            runs = data.get('workflow_runs', [])
            if runs:
                print(f"\n{C_YELLOW}Latest Runs:{C_RESET}")
                for r in runs[:3]:
                    status = r['status']
                    conclusion = r['conclusion']
                    
                    status_color = C_YELLOW
                    if status == "completed":
                        if conclusion == "success":
                            status_color = C_GREEN
                        elif conclusion == "failure":
                            status_color = C_RED
                            
                    display_status = conclusion if status == "completed" else status
                    print(f"  - Run: {C_CYAN}{r['id']}{C_RESET} | Event: {r['event']} | Status: {status_color}{display_status}{C_RESET} | Commit: {r['head_commit']['message']}")
            else:
                print(f"{C_RED}No runs found.{C_RESET}")
    except Exception as e:
        print(f"{C_RED}Error fetching runs: {e}{C_RESET}")

def main():
    # Enable colors on windows cmd
    os.system("")
    
    while True:
        print_header()
        versions = get_current_versions()
        global_ver = versions.get("globals.py", "Unknown")
        print(f"Active Version: {C_GREEN}{global_ver}{C_RESET}")
        print(f"---------------------------------------------------")
        print(f"1. Update Game Version (Across files)")
        print(f"2. Run Local Game Client")
        print(f"3. Run Local Game Server (New window)")
        print(f"4. Compile PC Client locally (build_pc.py)")
        print(f"5. Git Commit & Push (Trigger Android/PC Build)")
        print(f"6. Check GitHub Action Runs")
        print(f"7. Exit")
        print(f"---------------------------------------------------")
        
        choice = input("Enter choice (1-7): ").strip()
        
        if choice == "1":
            update_versions()
        elif choice == "2":
            run_client()
        elif choice == "3":
            run_server()
        elif choice == "4":
            compile_pc()
        elif choice == "5":
            git_push()
        elif choice == "6":
            check_actions()
        elif choice == "7":
            print(f"\n{C_CYAN}Goodbye!{C_RESET}")
            sys.exit(0)
        else:
            print(f"\n{C_RED}Invalid choice.{C_RESET}")
            
        input(f"\nPress Enter to continue...")

if __name__ == "__main__":
    main()
