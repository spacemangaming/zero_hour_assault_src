import os
import paramiko
from scp import SCPClient

# --- CONFIGURATION ---
HOSTNAME = "137.184.213.80"
PORT = 22
USERNAME = "root"
KEY_PATH = r"C:\Users\henry\.ssh\id_ed25519"

# Remote base directory on the server (change if the server path differs)
REMOTE_BASE_DIR = "/root"

# List of files modified in recent tasks to be uploaded
# Paths should be relative to the local repository root (C:\Users\henry\zero_hour_assault_src)
FILES_TO_UPLOAD = [
    r"server/data/match_modes.json",
    r"server/modules/utils/data_loader.py",
    r"server/modules/utils/match.py",
    r"server/modules/net/zh_net_gameplay_2.py",
    r"server/modules/net/zh_net_gameplay_3.py",
    r"server/modules/net/zh_net_gameplay_4.py",
    r"server/modules/net/zh_net_data_editor.py",
    r"server/modules/entities/npc.py",
    r"server/modules/core/zh_persistence.py",
    r"server/maps/massacre_in_the_city.map",
]

def upload_modified_files():
    local_base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Initialize SSH Client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Load Private Key (Ed25519)
        print(f"Loading private key: {KEY_PATH}")
        private_key = paramiko.Ed25519Key.from_private_key_file(KEY_PATH)
        
        # Connect to Server
        print(f"Connecting to {HOSTNAME}:{PORT} as {USERNAME}...")
        ssh.connect(hostname=HOSTNAME, port=PORT, username=USERNAME, pkey=private_key)
        
        # Initialize SCP
        print("Starting SCP Client...")
        with SCPClient(ssh.get_transport()) as scp:
            for rel_path in FILES_TO_UPLOAD:
                local_file_path = os.path.join(local_base_dir, rel_path)
                
                # Check if local file exists
                if not os.path.exists(local_file_path):
                    print(f"[-] Local file does not exist, skipping: {rel_path}")
                    continue
                
                # Build remote destination path (Linux uses forward slashes)
                remote_file_path = os.path.join(REMOTE_BASE_DIR, rel_path).replace("\\", "/")
                remote_dir = os.path.dirname(remote_file_path)
                
                # Automatically create remote directories if they don't exist
                # Runs 'mkdir -p' via SSH
                ssh.exec_command(f"mkdir -p {remote_dir}")
                
                print(f"[+] Uploading {rel_path} -> {remote_file_path}")
                scp.put(local_file_path, remote_file_path)
                
        print("\n[OK] All modified files uploaded successfully!")
        
    except Exception as e:
        print(f"\n[ERROR] Upload failed: {e}")
        print("Please verify that you ran 'pip install paramiko scp' in your environment.")
    finally:
        ssh.close()

if __name__ == "__main__":
    upload_modified_files()
