"""
******************************************************************************
Developed by: Jayden Becton
Access Control CSEC 2320
Project: Group Access Control System – Biological Data Management
Python 3.13.0v

Assignment Instructions:
Design a group access control system where multiple users (subjects) interact
with a set of shared files (objects) in the domain of biological data
management. Each user has specific permissions: read and write (r/w),
read-only (r), or no permission (np), assigned for each file.

Steps:
  1. Design and save the access control matrix to MAC.txt.
  2. Display the table content from MAC.txt on the screen.
  3. Admin interface: Add new subject / Update existing subject permissions.
  4. Authorization function: checks subject access to each of the five files.
******************************************************************************
"""

import os


# ===========================================================================
# SECTION 1 — MAC.txt Initialization, Reading, Saving, and Display
# ===========================================================================

MAC_FILE = "MAC.txt"
FILES    = ["File1", "File2", "File3", "File4", "File5"]

VALID_PERMISSIONS = {"r/w", "r", "np"}

DEFAULT_MATRIX = {
    "Alice":   ["r/w", "r/w", "r",   "r",   "r"],
    "Bob":     ["np",  "np",  "r",   "r",   "r/w"],
    "Charlie": ["np",  "np",  "np",  "r/w", "r/w"],
    "Daisy":   ["r",   "r",   "r/w", "r",   "np"],
    "Emmy":    ["np",  "np",  "np",  "np",  "np"],
}


def initialize_mac():
    """Write the default access control matrix to MAC.txt."""
    save_mac(DEFAULT_MATRIX)
    print("[INFO] MAC.txt initialized with default access control matrix.")


def read_mac() -> dict:
    """
    Parse MAC.txt and return the access control matrix as a dictionary.
    Returns: { "SubjectName": ["perm1", "perm2", "perm3", "perm4", "perm5"] }
    """
    matrix = {}
    with open(MAC_FILE, "r") as f:
        lines = f.readlines()

    # Skip the two header lines (column headers + separator)
    for line in lines[2:]:
        parts = line.strip().split()
        if len(parts) == 6:
            subject      = parts[0]
            permissions  = parts[1:]
            matrix[subject] = permissions

    return matrix


def save_mac(matrix: dict):
    """Write the given access control matrix dictionary back to MAC.txt."""
    with open(MAC_FILE, "w") as f:
        # Header row
        f.write(f"{'Subject':<12} {'File1':<8} {'File2':<8} "
                f"{'File3':<8} {'File4':<8} {'File5':<8}\n")
        # Separator
        f.write("-" * 60 + "\n")
        # Data rows
        for subject, perms in matrix.items():
            f.write(
                f"{subject:<12} {perms[0]:<8} {perms[1]:<8} "
                f"{perms[2]:<8} {perms[3]:<8} {perms[4]:<8}\n"
            )


def display_mac():
    """Read MAC.txt and print the access control matrix to the screen."""
    print("\n" + "=" * 60)
    print("        ACCESS CONTROL MATRIX  (MAC.txt)")
    print("=" * 60)
    with open(MAC_FILE, "r") as f:
        print(f.read())
    print("=" * 60)


# ===========================================================================
# SECTION 2 — Admin Interface
# ===========================================================================

def admin_interface():
    """
    Admin menu.
    Option 1 – Create: add a new subject.
    Option 2 – Update: change permissions for an existing subject.
    Option 3 – Display current matrix.
    Option 4 – Exit admin interface.
    """
    while True:
        print("\n" + "=" * 60)
        print("               ADMIN INTERFACE")
        print("=" * 60)
        print("  Options:")
        print("    Create (1) – Add a new user and their permissions")
        print("    Update (2) – Modify permissions for an existing user")
        print("    Display(3) – Show current access control matrix")
        print("    Exit   (4) – Return to main menu")
        print("=" * 60)

        choice = input("Enter option: ").strip()

        if choice == "1":
            admin_add_subject()
        elif choice == "2":
            admin_update_subject()
        elif choice == "3":
            display_mac()
        elif choice == "4":
            print("[INFO] Exiting admin interface.")
            break
        else:
            print("[ERROR] Invalid option. Please enter 1, 2, 3, or 4.")


def admin_add_subject():
    """
    Add a new subject to the access control matrix.
    Input format:  Name_perm1_perm2_perm3_perm4_perm5
    Example:       Fanny_np_r/w_r_r_r
    """
    print("\n--- Create New Subject ---")
    print("Format : Name_File1perm_File2perm_File3perm_File4perm_File5perm")
    print("Example: Fanny_np_r/w_r_r_r")
    print("Valid permissions: r/w | r | np")

    entry = input("\nInput: ").strip()
    parts = entry.split("_")

    # Validate structure
    if len(parts) != 6:
        print("[ERROR] Invalid format. Exactly 6 underscore-separated fields required.")
        return

    name  = parts[0]
    perms = parts[1:]

    # Validate each permission token
    for p in perms:
        if p not in VALID_PERMISSIONS:
            print(f"[ERROR] Invalid permission '{p}'. Must be one of: r/w, r, np")
            return

    matrix = read_mac()

    if name in matrix:
        print(f"[ERROR] Subject '{name}' already exists. Use Update (2) to modify.")
        return

    # Add and persist
    matrix[name] = perms
    save_mac(matrix)

    print(f"\n[SUCCESS] Subject '{name}' added to the access control matrix.")
    display_mac()


def admin_update_subject():
    """
    Update permissions for an existing subject.
    Prompts for each file permission individually.
    """
    matrix = read_mac()

    print("\n--- Update Existing Subject ---")
    print("Current subjects:", ", ".join(matrix.keys()))
    name = input("Enter subject name to update: ").strip()

    if name not in matrix:
        print(f"[ERROR] Subject '{name}' not found in the matrix.")
        return

    print(f"\nCurrent permissions for {name}:")
    for i, perm in enumerate(matrix[name]):
        print(f"  {FILES[i]}: {perm}")

    print("\nEnter new permissions (r/w | r | np) for each file:")
    new_perms = []
    for file_label in FILES:
        while True:
            perm = input(f"  {file_label} permission: ").strip()
            if perm in VALID_PERMISSIONS:
                new_perms.append(perm)
                break
            print("  [ERROR] Invalid. Enter r/w, r, or np.")

    matrix[name] = new_perms
    save_mac(matrix)

    print(f"\n[SUCCESS] Permissions for '{name}' updated successfully.")
    display_mac()


# ===========================================================================
# SECTION 3 — Access Authorization Function
# ===========================================================================

# Map file labels to column indices in the matrix
FILE_INDEX_MAP = {
    "file1": 0, "file2": 1, "file3": 2, "file4": 3, "file5": 4,
}


def check_access(subject: str, file_label: str):
    """
    Authorize a subject's access request to a file.

    Rules:
      np  → print NO PERMISSION, do not open or print file contents.
      r   → print file contents; deny any write operation.
      r/w → print file contents; open file for reading and writing.

    Args:
        subject    : name of the requesting user (e.g. "Alice")
        file_label : file identifier (e.g. "File1", "file1", "File1.txt")
    """
    matrix = read_mac()

    # Normalize the file label
    normalized = file_label.lower().replace(".txt", "").replace(" ", "")

    print("\n" + "=" * 60)
    print(f"  ACCESS REQUEST:  {subject}  →  {file_label}")
    print("=" * 60)

    # Validate subject
    if subject not in matrix:
        print(f"[ERROR] Subject '{subject}' not found in access control matrix.")
        print("=" * 60)
        return

    # Validate file label
    if normalized not in FILE_INDEX_MAP:
        print(f"[ERROR] File '{file_label}' is not recognized.")
        print("=" * 60)
        return

    col_index  = FILE_INDEX_MAP[normalized]
    permission = matrix[subject][col_index]
    file_path  = f"{normalized.capitalize()}.txt"   # e.g. File1.txt

    print(f"  Subject    : {subject}")
    print(f"  File       : {file_path}")
    print(f"  Permission : {permission}")
    print("-" * 60)

    # ── NO PERMISSION ────────────────────────────────────────────────────────
    if permission == "np":
        print("\n  *** NO PERMISSION ***")
        print(f"  Access DENIED — {subject} has no permission for {file_path}.")
        print("=" * 60)
        return

    # Confirm the file actually exists on disk
    if not os.path.exists(file_path):
        print(f"[WARNING] {file_path} does not exist on disk.")
        print("=" * 60)
        return

    # ── READ ONLY ────────────────────────────────────────────────────────────
    if permission == "r":
        print(f"\n  READ ACCESS GRANTED")
        print(f"  Opening {file_path} for reading...")
        print(f"  Write access DENIED for {subject}.\n")
        print(f"--- Contents of {file_path} ---")
        with open(file_path, "r") as f:
            print(f.read())
        print(f"--- End of {file_path} ---")

    # ── READ / WRITE ──────────────────────────────────────────────────────────
    elif permission == "r/w":
        print(f"\n  READ / WRITE ACCESS GRANTED")
        print(f"  Opening {file_path} for reading and writing...\n")
        print(f"--- Contents of {file_path} ---")
        with open(file_path, "r+") as f:
            print(f.read())
        print(f"--- End of {file_path} ---")

    print("=" * 60)


# ===========================================================================
# SECTION 4 — Main Program Loop
# ===========================================================================

def main():
    print("""
******************************************************************************
  Developed by : Jayden Becton
  Course       : Access Control CSEC 2320
  Project      : Group Access Control System – Biological Data Management
  Python       : 3.13.0v
******************************************************************************
""")

    # Initialize MAC.txt if it does not exist yet
    if not os.path.exists(MAC_FILE):
        initialize_mac()

    # (20 pts) Display the access control matrix on startup
    display_mac()

    while True:
        print("\n" + "=" * 60)
        print("                  MAIN MENU")
        print("=" * 60)
        print("  (1) Admin Interface  – Manage users and permissions")
        print("  (2) Check Access     – Authorize a subject/file request")
        print("  (3) Display Matrix   – Print current MAC.txt")
        print("  (4) Exit")
        print("=" * 60)

        choice = input("Enter option: ").strip()

        # ── Admin interface ──────────────────────────────────────────────────
        if choice == "1":
            admin_interface()

        # ── Access check ─────────────────────────────────────────────────────
        elif choice == "2":
            print("\nAccess Check")
            print("Format: SubjectName_FileNumber  (e.g. Alice_File1 or Bob_File4)")
            entry = input("Input: ").strip()

            parts = entry.split("_")
            if len(parts) != 2:
                print("[ERROR] Invalid format. Use: SubjectName_FileNumber")
            else:
                check_access(parts[0], parts[1])

        # ── Display matrix ───────────────────────────────────────────────────
        elif choice == "3":
            display_mac()

        # ── Exit ─────────────────────────────────────────────────────────────
        elif choice == "4":
            print("Exiting program. Goodbye!")
            break

        else:
            print("[ERROR] Invalid option. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
