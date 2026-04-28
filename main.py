import os
import shutil
from extractor import extract_manga
from transformer import transform_to_cbz
from loader import load_to_server

def cleanup(folder_path, cbz_path):
    """
    Deletes the temporary folder and local .cbz file after a successful upload.
    """
    print(f"\n🧹 [CLEANUP] Removing temporary local files...")
    try:
        if folder_path and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            print(f"   🗑️ Removed folder: {folder_path}")
            
        if cbz_path and os.path.isfile(cbz_path):
            os.remove(cbz_path)
            print(f"   🗑️ Removed file: {cbz_path}")
            
        print("✨ Cleanup complete!")
    except Exception as error:
        print(f"⚠️ Cleanup Error: {error}")

def run_pipeline():
    """
    The Main Orchestrator.
    Ties together the Extract, Transform, and Load phases of the Manga-Sync pipeline.
    """
    print("="*50)
    print(" 🌟 Welcome to Manga-Sync ETL Pipeline 🌟")
    print("="*50)
    
    # 1. Ask the user for inputs
    url = input("🔗 Enter the URL of the manga chapter: ").strip()
    series_name = input("📚 Enter the Series Name (e.g., Blue_Lock): ").strip()
    chapter_number = input("🔢 Enter the Chapter Number (e.g., 016): ").strip()
    
    if not url or not series_name or not chapter_number:
        print("❌ Error: All fields are required. Exiting pipeline.")
        return

    # Load default SFTP credentials from environment variables (e.g. from .env file)
    from dotenv import load_dotenv
    load_dotenv()
    
    default_host = os.getenv("SFTP_HOST", "")
    default_port = os.getenv("SFTP_PORT", "22")
    default_user = os.getenv("SFTP_USER", "")
    default_pass = os.getenv("SFTP_PASS", "")

    # Prompt for SFTP credentials, using defaults if empty
    print("\n[SFTP Credentials for Pikapods] (Press Enter to use default values from .env)")
    sftp_host = input(f"🖥️  Host [{default_host}]: ").strip() or default_host
    sftp_port_input = input(f"🚪 Port [{default_port}]: ").strip() or default_port
    sftp_port = int(sftp_port_input)
    sftp_user = input(f"👤 Username [{default_user}]: ").strip() or default_user
    sftp_pass = input(f"🔑 Password [{'******' if default_pass else ''}]: ").strip() or default_pass

    # 2. Phase 1: Extract
    folder_path = extract_manga(url, series_name, chapter_number)
    if not folder_path:
        print("🛑 Pipeline stopped: Extraction failed.")
        return
        
    # 3. Phase 2: Transform
    cbz_path = transform_to_cbz(folder_path)
    if not cbz_path:
        print("🛑 Pipeline stopped: Transformation failed.")
        return
        
    # 4. Phase 3: Load
    # Set the predetermined route depending on the series name
    # e.g. /data/Manga/Blue_Lock/
    remote_dir = f"/data/Manga/{series_name}/"
    upload_success = load_to_server(cbz_path, sftp_host, sftp_port, sftp_user, sftp_pass, remote_dir=remote_dir)
    if not upload_success:
        print("🛑 Pipeline stopped: Load failed.")
        return
        
    # 5. Cleanup
    cleanup(folder_path, cbz_path)
    print("\n🎉 Pipeline completed successfully! The chapter is now on your Komga server.")

if __name__ == '__main__':
    run_pipeline()
