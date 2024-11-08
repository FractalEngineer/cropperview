# cropperview.py
import os
import subprocess
import sys

# Automatically detect the root directory
root_dir = os.getcwd()
print(f"found root dir: {root_dir}")

# Set input and output directories relative to the root
input_dir = os.path.join(root_dir, 'input_videos')
output_dir = os.path.join(root_dir, 'output_videos')

# Set Handbrake and Superview command paths relative to the root
handbrake_cmd = os.path.join(root_dir, 'HandBrakeCLI.exe')
superview_cmd = os.path.join(root_dir, 'superview-cli-windows-amd64-v0.10.exe')
ffmpeg_concat_list = os.path.join(root_dir, 'concat_list.txt')

def process_video(input_file, output_base_name):
    """Process a single video file through Handbrake and Superview"""
    cropped_output = os.path.join(output_dir, output_base_name + '_cropped.mp4')
    
    # Run Handbrake to crop the video (144 pixels left, 148 right)
    print(f"Running Handbrake to crop the video: {input_file}")
    subprocess.run([handbrake_cmd, '-i', input_file, '-o', cropped_output, '--crop', '0:0:144:148'], shell=True)

    # Run Superview to process the cropped video
    print(f"Running Superview to process the cropped video: {cropped_output}")
    final_output = os.path.join(output_dir, output_base_name + '_superview.mp4')
    subprocess.run([superview_cmd, '-i', cropped_output, '-o', final_output], shell=True)
    
    return final_output

def combine_videos():
    """Combine all videos in the input directory into one file"""
    print("Combining all input videos...")
    
    # Create a list of all video files
    with open(ffmpeg_concat_list, 'w') as f:
        for filename in sorted(os.listdir(input_dir)):
            if filename.endswith(('.mp4', '.ts')):
                file_path = os.path.join(input_dir, filename)
                f.write(f"file '{file_path}'\n")
    
    # Combine all videos using FFmpeg
    combined_output = os.path.join(input_dir, 'combined_input.mp4')
    subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', ffmpeg_concat_list, '-c', 'copy', combined_output], shell=True)
    
    # Clean up the temporary file list
    os.remove(ffmpeg_concat_list)
    
    return combined_output

def main():
    # Check if we should combine videos (passed as command line argument)
    should_combine = len(sys.argv) > 1 and sys.argv[1].lower() == 'combine'
    
    if should_combine:
        # Combine all videos and process the combined file
        combined_file = combine_videos()
        process_video(combined_file, 'combined')
        # Clean up the combined input file
        os.remove(combined_file)
    else:
        # Process each video separately
        for filename in os.listdir(input_dir):
            if filename.endswith(('.mp4', '.ts')):
                print(f"Processing file: {filename}")
                input_file = os.path.join(input_dir, filename)
                output_base_name = os.path.splitext(filename)[0]
                process_video(input_file, output_base_name)
                print(f"Processed: {filename}")

if __name__ == "__main__":
    main()