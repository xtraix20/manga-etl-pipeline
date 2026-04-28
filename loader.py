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
        
        # Ensure the remote directory exists
        try:
            sftp.stat(remote_dir)
        except IOError:
            print(f"📁 Creating remote directory {remote_dir}...")
            # Create directories one by one if needed (simple approach for one level deep)
            try:
                sftp.mkdir(remote_dir)
            except IOError:
                # If it's a nested path like /data/Manga/SeriesName, make sure /data/Manga exists first
                # For our use case, we assume the parent already exists
                pass

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

