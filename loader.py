import paramiko
import os

def load_to_server(cbz_path, host, port, username, password, remote_dir="/data/Manga/"):
    """
    Phase 3: Load.
    Uploads the compiled .cbz file to a remote Pikapods server securely via SFTP.
    
    Args:
        cbz_path (str): Local path to the .cbz file.
        host (str): SFTP server hostname or IP.
        port (int): SFTP server port.
        username (str): SFTP username.
        password (str): SFTP password.
        remote_dir (str): Destination directory on the remote server.
        
    Returns:
        bool: True if upload was successful, False otherwise.
    """
    print(f"\n🚀 [Phase 3: LOAD] Starting upload to remote server for {cbz_path}...")
    
    if not cbz_path or not os.path.isfile(cbz_path):
        print(f"❌ Upload Error: File '{cbz_path}' does not exist.")
        return False

    file_name = os.path.basename(cbz_path)
    remote_path = os.path.join(remote_dir, file_name).replace('\\', '/')
    
    transport = None
    sftp = None
    
    try:
        print(f"🌐 Establishing connection to {host}:{port}...")
        
        # Set up the transport and connect
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        
        # Create an SFTP client from the transport
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        print(f"📤 Uploading {file_name} to {remote_dir}...")
        
        # Ensure the remote directory exists (Optional advanced logic could create it)
        # We assume /data/Manga/ already exists based on the requirements.
        sftp.put(cbz_path, remote_path)
        
        print(f"✅ Mission accomplished! File successfully uploaded to {remote_path}")
        return True
        
    except paramiko.AuthenticationException:
        print("❌ Authentication Error: Invalid username or password.")
        return False
    except TimeoutError:
        print("❌ Timeout Error: The server took too long to respond.")
        return False
    except Exception as error:
        print(f"❌ Upload Error: {error}")
        return False
    finally:
        # Always ensure the connections are closed
        if sftp:
            sftp.close()
        if transport:
            transport.close()
            print("🔌 Connection closed.")

# --- Test Block ---
if __name__ == '__main__':
    # These should ideally be set as environment variables
    test_host = os.environ.get("SFTP_HOST", "lean-tiger.pikapod.net")
    test_port = int(os.environ.get("SFTP_PORT", 22))
    test_user = os.environ.get("SFTP_USER", "p23773")
    test_pass = os.environ.get("SFTP_PASS", "lgY0Y9VSeJnslDh0qU4zudZo")
    
    test_file = "Blue_Lock_016.cbz"
    if os.path.exists(test_file):
         load_to_server(test_file, test_host, test_port, test_user, test_pass)
    else:
        print(f"⚠️ Test file '{test_file}' not found. Run the transformer first to test.")
