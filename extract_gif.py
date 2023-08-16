from PIL import Image
import os

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
    
# you can make an input file consisted with directory path.
# Such as
# /home/ubuntu/Documents/self-driving-cars/ADFuzz/run_results_op/nsga2/Town06_Opt_forward/Town06_Opt_forward/op/2023_08_04_00_43_21,50_10_none_500_coeff_0_0.1_0.5_only_unique_0
# and so on.
with open("input.txt") as f:
    scenario_folders=f.readlines()
scenario_folders= [line[:-1] for line in scenario_folders]
duration_between_frames_ms = 5  # You can adjust this value for frame duration in milliseconds

for scenario_folder in scenario_folders:
    for b in ['/bugs', '/non_bugs']:
        bug_folder=scenario_folder + b
        for sub_folder in os.listdir(bug_folder):
            print(sub_folder)
            ff_name= bug_folder + '/' + sub_folder
            print(f'ff name: {ff_name}')
            create_gif(ff_name, duration_between_frames_ms)
            # frames_folder
        # output_gif_path =  frames_folder + '/output.gif'