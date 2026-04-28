import os
import shutil

def transform_to_cbz(folder_path):
    """
    Phase 2: Transform.
    Packages the folder containing downloaded images into a Comic Book Zip (.cbz) file.
    
    Args:
        folder_path (str): The path to the folder containing the images.
        
    Returns:
        str: The file path of the generated .cbz file, or None if transformation failed.
    """
    print(f"\n📦 [Phase 2: TRANSFORM] Starting packaging for {folder_path}...")
    
    try:
        # Check if the folder exists
        if not os.path.isdir(folder_path):
            print(f"❌ Transformation Error: Folder '{folder_path}' does not exist.")
            return None
            
        zip_path = f"{folder_path}.zip"
        cbz_path = f"{folder_path}.cbz"
        
        print(f"🗜️  Zipping the folder contents...")
        # Create a zip archive of the folder
        shutil.make_archive(base_name=folder_path, format='zip', root_dir=folder_path)
        
        print(f"🔄 Converting .zip to .cbz...")
        # Rename the extension from .zip to .cbz safely (overwrites if exists)
        os.replace(zip_path, cbz_path)
        
        print(f"✅ Mission accomplished! Comic book generated at: {cbz_path}")
        return cbz_path
        
    except Exception as error:
        print(f"❌ Transformation Error: {error}")
        return None

# --- Test Block ---
if __name__ == '__main__':
    # Dummy test assuming a folder named "Blue_Lock_016" exists
    test_folder = "Blue_Lock_016"
    if os.path.exists(test_folder):
        transform_to_cbz(test_folder)
    else:
        print(f"⚠️ Test folder '{test_folder}' not found. Run the extractor first to test.")
