import os
import subprocess

# Automatically detect the root directory
root_dir = os.getcwd()
print(f"found root dir: {root_dir}")

# Set input and output directories relative to the root
input_dir = os.path.join(root_dir, 'input_videos')
output_dir = os.path.join(root_dir, 'output_videos')

# Set Handbrake and Superview command paths relative to the root
handbrake_cmd = os.path.join(root_dir, 'HandBrakeCLI.exe')
superview_cmd = os.path.join(root_dir, 'superview-cli-windows-amd64-v0.10.exe')

# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.mp4') or filename.endswith('.ts'):
        print(f"Processing file: {filename}")

        # Construct input and output file paths
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + '_cropped.mp4')

        # Run Handbrake to crop the video (144 pixels left, 148 right)
        print("Running Handbrake to crop the video...")
        subprocess.run([handbrake_cmd, '-i', input_file, '-o', output_file, '--crop', '0:0:144:148'], shell=True)

        # Run Superview to process the cropped video
        print("Running Superview to process the cropped video...")
        subprocess.run([superview_cmd, '-i', output_file, '-o', os.path.join(output_dir, os.path.splitext(filename)[0] + '_superview.mp4')], shell=True)

        print(f"Processed: {filename}")