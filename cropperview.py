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

def process_video(input_file, output_base_name, use_gpu=False, skip_crop=False):
    """Process a single video file through Handbrake and/or Superview"""
    # If skipping crop, use the input file directly
    if skip_crop:
        cropped_output = input_file
        print(f"Skipping crop for video: {input_file}")
    else:
        # Output path for cropped video
        cropped_output = os.path.join(output_dir, output_base_name + '_cropped.mp4')
        
        # Run Handbrake to crop the video (144 pixels left, 148 right)
        print(f"Running Handbrake to crop the video: {input_file}")
        handbrake_args = [handbrake_cmd, '-i', input_file, '-o', cropped_output, '--crop', '0:0:144:148']
        if use_gpu:
            handbrake_args.extend(['--hwdecode', 'cuda', '--hwaccel', 'cuda'])
        subprocess.run(handbrake_args, shell=True)

    # Run Superview to process the video
    print(f"Running Superview to process the video: {cropped_output}")
    final_output = os.path.join(output_dir, output_base_name + '_superview.mp4')
    subprocess.run([superview_cmd, '-i', cropped_output, '-o', final_output], shell=True)
    
    return final_output

def combine_videos():
    """Combine all videos in the input directory into one file"""
    print("Combining all input videos...")
    
    # Debug: Print full path of input directory
    print(f"Input directory full path: {input_dir}")
    
    # Debug: List all files in the input directory
    print("Files in input directory:")
    for item in os.listdir(input_dir):
        full_path = os.path.join(input_dir, item)
        print(f"- {item} (Full path: {full_path}, Is file: {os.path.isfile(full_path)})")
    
    # Get a list of input video files
    video_files = [
        os.path.join(input_dir, filename) 
        for filename in sorted(os.listdir(input_dir)) 
        if filename.lower().endswith(('.mp4', '.ts'))
    ]
    
    print(f"Detected video files: {video_files}")
    
    if not video_files:
        print("No video files found in the input directory!")
        return None

    # If only one video, return that video directly
    if len(video_files) == 1:
        return video_files[0]
    
    # Combine videos using FFmpeg
    combined_output = os.path.join(input_dir, 'combined_input.mp4')
    
    # Use FFmpeg concat demuxer method
    concat_args = [
        'ffmpeg', 
        '-f', 'concat', 
        '-safe', '0', 
        '-i', ffmpeg_concat_list, 
        '-c', 'copy', 
        combined_output
    ]
    
    # Create the concat list file with full file paths
    with open(ffmpeg_concat_list, 'w') as f:
        for video_file in video_files:
            f.write(f"file '{video_file}'\n")
    
    try:
        # Run FFmpeg to combine videos
        print(f"Executing: {' '.join(concat_args)}")
        result = subprocess.run(concat_args, shell=True, text=True, capture_output=True)
        
        # Print any outputs or errors
        if result.stdout:
            print("FFmpeg stdout:", result.stdout)
        if result.stderr:
            print("FFmpeg stderr:", result.stderr)
        
        # Check if the output file was created
        if not os.path.exists(combined_output):
            print("Failed to create combined video!")
            return None
        
        return combined_output
    
    except Exception as e:
        print(f"Error combining videos: {e}")
        return None
    finally:
        # Clean up the temporary concat list file
        if os.path.exists(ffmpeg_concat_list):
            os.remove(ffmpeg_concat_list)

def main():
    # Check if we should combine videos (passed as command line argument)
    should_combine = len(sys.argv) > 1 and sys.argv[1].lower() == 'combine'
    
    # Check if we should use GPU acceleration
    use_gpu = any(arg.lower() == 'gpu' for arg in sys.argv[1:])
    
    # Check if we should skip cropping
    skip_crop = any(arg.lower() == 'nocrop' for arg in sys.argv[1:])
    
    if should_combine:
        # Combine all videos and process the combined file
        combined_file = combine_videos()
        if combined_file:
            process_video(combined_file, 'combined', use_gpu=use_gpu, skip_crop=skip_crop)
            # Clean up the combined input file if it's a temporary file
            if 'combined_input.mp4' in combined_file:
                os.remove(combined_file)
        else:
            print("Video combination failed!")
    else:
        # Process each video separately
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.mp4', '.ts')):
                print(f"Processing file: {filename}")
                input_file = os.path.join(input_dir, filename)
                output_base_name = os.path.splitext(filename)[0]
                process_video(input_file, output_base_name, use_gpu=use_gpu, skip_crop=skip_crop)
                print(f"Processed: {filename}")

if __name__ == "__main__":
    main()