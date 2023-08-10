from PIL import Image
import os
import boto3
import configparser

config = configparser.ConfigParser()
with open('conf.ini', 'w') as configfile:
    config.write(configfile)

# need to be encapsulated by using env var
s3 = boto3.client("s3", aws_access_key_id=os.environ["AWS_ACCESS_KEY"], aws_secret_access_key=os.environ["AWS_SECRET_KEY"])
s3_bucket_name = os.environ["S3_BUCKET_NAME"]

def create_gif(scenario_folder, duration=100):
    output_gif_path=scenario_folder + '/output.gif'
    pickle_path=scenario_folder + '/cur_info.pickle'
    txt_path=scenario_folder + '/cur_info.txt'
    # Get all image files from the frames folder
    frames_folder=scenario_folder + '/front'
    frame_files = [f for f in os.listdir(frames_folder) if f.endswith('.jpg')]
    # Sort the image files numerically (assuming filenames are numbers)
    frame_files.sort(key=lambda x: int(x.split('.')[0]))

    images = []
    for frame_file in frame_files:
        frame_path = os.path.join(frames_folder, frame_file)
        img = Image.open(frame_path)
        images.append(img)
    
    if len(images)==0:
        print(f"No image in {frames_folder}")
        return
    # Save the images as a GIF file
    images[0].save(
        output_gif_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )
    
    s3_prefix="FusED/" + scenario_folder 

    # s3_file_path="Fused/Town06_Opt_forward/" + '/'.join(frames_folder.split('/')[-3:]) + '.gif'
    try:
        # Upload the file to the specified S3 bucket
        s3.upload_file(output_gif_path, s3_bucket_name, s3_prefix + '/output.gif')
        print(f"File '{output_gif_path}' uploaded successfully to S3 bucket '{s3_bucket_name}.")
        s3.upload_file(pickle_path, s3_bucket_name, s3_prefix + '/cur_info.pickle')
        print(f"File '{pickle_path}' uploaded successfully to S3 bucket '{s3_bucket_name}.")
        s3.upload_file(txt_path, s3_bucket_name, s3_prefix + '/cur_info.txt')
        print(f"File '{txt_path}' uploaded successfully to S3 bucket '{s3_bucket_name}.")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")

scenario_folders = config.items("paths")
duration_between_frames_ms = config.items('duration')

for _, scenario_folder in scenario_folders:
    for b in ['/bugs', '/non_bugs']:
        bug_folder=scenario_folder + b
        for sub_folder in os.listdir(bug_folder):
            print(sub_folder)
            ff_name= bug_folder + '/' + sub_folder
            print(f'ff name: {ff_name}')
            create_gif(ff_name, duration_between_frames_ms)
            # frames_folder
        # output_gif_path =  frames_folder + '/output.gif'