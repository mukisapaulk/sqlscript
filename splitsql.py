import os

# Configuration
input_file = "D:/test_zazella_uganda.sql"  # Your SQL file path
output_dir = "D:/test zazella sql"  # Your output folder path
max_size_mb = 46  # Maximum size per file in MB (updated to 46 MB as requested)
max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def get_file_size(file_path):
    """Get the size of the input file in bytes and MB."""
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)
    return size_bytes, size_mb


def estimate_file_count(total_size_bytes, max_size_bytes):
    """Estimate the number of files based on total size and max size per file."""
    return -(-total_size_bytes // max_size_bytes)  # Ceiling division


def split_sql_file(input_file, output_dir, max_size_bytes):
    # Get total file size
    total_size_bytes, total_size_mb = get_file_size(input_file)
    estimated_files = estimate_file_count(total_size_bytes, max_size_bytes)
    print(f"Input file size: {total_size_mb:.2f} MB")
    print(f"Estimated number of files (max {max_size_mb} MB each): {estimated_files}")

    with open(input_file, 'r', encoding='utf-8') as f:
        file_number = 1
        current_size = 0
        current_lines = []

        for line in f:
            line_size = len(line.encode('utf-8'))  # Size in bytes
            current_lines.append(line)
            current_size += line_size

            # Only split when approaching or exceeding max size and at a semicolon
            if current_size >= max_size_bytes and line.strip().endswith(';'):
                output_file = os.path.join(output_dir, f"split_{file_number}.sql")
                with open(output_file, 'w', encoding='utf-8') as out:
                    out.write(''.join(current_lines))
                print(f"Created {output_file} ({current_size / (1024 * 1024):.2f} MB)")

                # Reset for the next file
                file_number += 1
                current_lines = []
                current_size = 0

        # Write any remaining lines to a final file
        if current_lines:
            output_file = os.path.join(output_dir, f"split_{file_number}.sql")
            with open(output_file, 'w', encoding='utf-8') as out:
                out.write(''.join(current_lines))
            print(f"Created {output_file} ({current_size / (1024 * 1024):.2f} MB)")


# Run the script
if __name__ == "__main__":
    if os.path.exists(input_file):
        print(f"Splitting {input_file} into files <= {max_size_mb} MB...")
        split_sql_file(input_file, output_dir, max_size_bytes)
        print("Splitting complete!")
    else:
        print(f"Error: Input file '{input_file}' not found.")