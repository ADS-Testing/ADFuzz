# FusED replication docs
## Requirements

Based on [original repo](https://github.com/AIasd/ADFuzz/blob/main/doc/stack5_carla_openpilot.md)

- Monitor (i.e., due to the limitation of OpenPilot, the simulation can only run on a machine with a monitor/virtual monitor)
- OS: Ubuntu 20.04
- CPU: at least 4 cores
- GPU: at least 6GB memory
- Storage(SSD recommended): at least 150GB
- Openpilot 0.8.5 (customized)
- Carla 0.9.11
- Python 3.8.5

## Environmental Setup

### Install pyenv and python3.8

**TODO: Change it to conda**  
install pyenv for python. If you have 

```
curl -L <https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer> | bash

```

install python

```
PATH=$HOME/.pyenv/bin:$HOME/.pyenv/shims:$PATH
pyenv install -s 3.8.5
pyenv global 3.8.5
pyenv rehash
eval "$(pyenv init -)"

```

add the following lines to the end of `~/.bashrc` to make sure pyenv is active when openning a new terminal

```
PATH=$HOME/.pyenv/bin:$HOME/.pyenv/shims:$PATH
eval "$(pyenv init -)"

```

### Directory Structure

```bash
mkdir -p ~/Documents/self-driving-cars

```

~(home folder)

```
├── openpilot(To be cloned)
├── Documents
│   ├── self-driving-cars (created by the user manually)
│   │   ├── ADFuzz (To be cloned)
│   │   ├── carla_0911_rss (To be installed)

```

### Clone project repository

```
cd ~/Docuements/self-driving-cars
git clone https://github.com/ADS-Testing/ADFuzz.git
```

### Python package installation

```
pip install pipenv
pipenv install

```

Activate environment

```bash
cd ~/Docuements/self-driving-cars/ADFuzz
pipenv shell

```

You can either use conda to install python modules

```
conda create -n [YOUR_ENV_NAME] python=3.8.5
conda activate [YOUR_ENV_NAME]
pip install -r requirements.txt
```

Install pytorch on its official website via pip.

Install pytroch-lightening, torchvision

```
pip3 install pytorch-lightning==0.8.5
pip install torchvision

```

### Install OpenPilot 0.8.5 (customized)

```
cd ~
git clone https://github.com/ADS-Testing/openpilot.git

```

```
cd ~/openpilot
./tools/ubuntu_setup.sh

```

- Once you get `ERROR: Couldn't install package: pprofile` message, just hit the `pip install pprofile` again.

Compile Openpilot

```

cd ~/openpilot
scons -j $(nproc)

```

### Common Compilation Issue

clang 10 is needed. If you need to install it, run

```
sudo apt install clang

```

### Common OpenCL Issue

Your environment needs to support opencl 2.0+ in order to run `scons` successfully (when using `clinfo`, it must show something like  "your OpenCL library only supports OpenCL <2.0+>")

### Install Carla 0.9.11

```
cd ~/Documents/self-driving-cars/ADFuzz
./install_carla.sh

```
This will download and extract CARLA file, and set the right Python path. Also it will download and install additional maps(For experimental setting in this repository, we need to download and install additional maps).

### Openpilot Python path issue

You should make sure that `/home/ubuntu/openpilot` is included in the Python path which you are running.
In pipenv, it can be acheived by adding
```
export PYTHONPATH="${PYTHONPATH}:/home/ubuntu/openpilot”
```
to `activate` file of the current virtual env.  


If not, ImportError regarding `'cereal'` module will occur.


## How to run

### Run fuzzing(Scenario generation)

```
cd ~/Documents/self-driving-cars/ADFuzz
python ga_fuzzing.py --simulator carla_op --n_gen 10 --pop_size 50 --algorithm_name nsga2 --has_run_num 500 --episode_max_time 200 --only_run_unique_cases 0 --objective_weights 1 0 0 0 -1 -2 0 -m op --route_type 'Town06_Opt_forward'

```

For the parameters passed into the parser, please refer to [here](https://github.com/ADS-Testing/ADFuzz/blob/main/customized_utils.py#L61C46-L61C46)

Results will be saved in `~/Documents/self-driving-cars/ADFuzz/run_results_op` folder. In case of the failure scenarios, following informations will be saved.

- Camera snapshots of front and top sides
- Failure situation: `tmp_data`
```
collision,558.7705688476562,-20.72282600402832,0.0019020652398467064,-0.009705698117613792,-179.6072235107422,0.0014395343605428934,vehicle.carlamotors.carlacola,6.688277322547812,0.0
```
- Trajectory data: `simlulation_data`
```
frame_id: 1155
camera_leads_dict: [{'dRel': 6.909393768310547, 'yRel': -0.36076778173446655, 'vRel': -1.706642508506775, 'a': 0.04999332129955292, 'dRelStd': 4.923594951629639, 'yRelStd': 1.808293104171753, 'vRelStd': 2.712010145187378, 'aStd': 1.5765703916549683, 'modelProb': 0.9795579314231873, 't': 0.0}, {'dRel': 6.909393768310547, 'yRel': -0.36076778173446655, 'vRel': -1.706642508506775, 'a': 0.04999332129955292, 'dRelStd': 4.923594951629639, 'yRelStd': 1.808293104171753, 'vRelStd': 2.712010145187378, 'aStd': 1.5765703916549683, 'modelProb': 0.8961397409439087, 't': 2.0}]

radar_clusters_dict: [{'dRel': 2.9375, 'yRel': -0.1875, 'vRel': -2.84375, 'modelProb': 1}, {'dRel': 36.0, 'yRel': 4.25, 'vRel': 3.875, 'modelProb': 1}]

radar_clusters_raw_dict: [{'dRel': 2.9375, 'yRel': -0.1875, 'vRel': -2.84375, 'modelProb': 1}, {'dRel': 36.0, 'yRel': 4.25, 'vRel': 3.875, 'modelProb': 1}]

lead_d_carla_dict: {'dRel': 0.0, 'yRel': -0.15846120924115326, 'vRel': -2.768737451390415, 'aLeadK': 0.0663042336391517, 'status': True, 'modelProb': 1.0}

leads_predicted_list_dict: [{'dRel': 2.9375, 'yRel': -0.1875, 'vRel': -2.84375, 'modelProb': 0.9795579314231873}, {'dRel': 2.9375, 'yRel': -0.1875, 'vRel': -2.84375, 'modelProb': 0.8961397409439087}]

cam_total_error: 0.7273484420776368
radar_total_error: 0.0
pred_total_error: 0.0
total_count, error_count, fusion_error_both_count, fusion_error_cam_count, fusion_error_radar_count: 30,23,0,0,21

d_avg_list_dict: [29.63967974431693, 72.92078503892161, 37.215992565009145, 80.85025676859185, 67.28505662656099, 73.83413022880481]
d_avg_old_list_dict: [29.582399286075752, 72.92078503892161, 85.06933731950718, 80.85025676859185, 67.28505662656099, 73.83413022880481]
vehicle_info_dict: {'counter': 1155, 'frame_id': 1155, 'vehicle_control_throttle': 0.04165737330913544, 'vehicle_control_steer': -0.0014628267381340265, 'vehicle_control_brake': -0.0, 'vehicle_state_speed': 6.768716572291674, 'vehicle_state_vel_x': -6.768579483032227, 'vehicle_state_vel_y': -0.043079204857349396, 'vehicle_state_vel_z': 2.097873675666051e-06, 'vehicle_state_angle': 1.5359679460525513, 'vehicle_state_cruise_button': 0, 'vehicle_state_is_engaged': True, 'npc_actor_0_speed': 10.208353533861033, 'cur_ego_car_model': 'op'}
```
- Running information: `cur_info`
```
{'x': array([ 39.16190005,  37.94668264,  27.69385807,  45.84670725,
       166.80784197, -65.63806642,   9.2803567 ,  31.91311005,
        25.12512797,   1.37688038,   6.        ,   0.        ,
        56.        ,   5.        ,  15.        ,  -3.5       ,
         0.        ,   2.6731921 ,   2.        , -90.27666335,
         6.60275357,   2.        ,   1.23876765,   0.        ,
        ...
         4.        , -15.        ,   3.5       ,   0.        ,
       -88.00020459,   1.        , -91.9219806 ,   1.        ,
       -33.64567335,   0.        , -50.8636195 ,   0.        ,
       -37.29653781,   0.        , -34.46723091]), 'objectives': array([0.00999224, 1.        , 6.13407443, 0.        , 1.        ,
       0.        , 0.        ]), 
       'labels': ['cloudiness', 'precipitation', 'precipitation_deposits', 'wind_intensity', 'sun_azimuth_angle', 'sun_altitude_angle', 'fog_density', 'fog_distance', 'wetness', 'fog_falloff', 'num_of_vehicles', 'delay_time_to_start', 'ego_maximum_speed', 'num_of_vehicle_types_0', 'vehicle_x_0', 'vehicle_y_0', 'vehicle_yaw_0', 'vehicle_speed_0', 'vehicle_0_vehicle_lane_change_0', 'vehicle_0_vehicle_speed_0', 'vehicle_0_vehicle_lane_change_1', 'vehicle_0_vehicle_speed_1', 'vehicle_0_vehicle_lane_change_2', 
       
       ... 

       'vehicle_4_vehicle_lane_change_2', 'vehicle_4_vehicle_speed_2', 'vehicle_4_vehicle_lane_change_3', 'vehicle_4_vehicle_speed_3', 'vehicle_4_vehicle_lane_change_4', 'vehicle_4_vehicle_speed_4', 'num_of_vehicle_types_5', 'vehicle_x_5', 'vehicle_y_5', 'vehicle_yaw_5', 'vehicle_speed_5', 'vehicle_5_vehicle_lane_change_0', 'vehicle_5_vehicle_speed_0', 'vehicle_5_vehicle_lane_change_1', 'vehicle_5_vehicle_speed_1', 'vehicle_5_vehicle_lane_change_2', 'vehicle_5_vehicle_speed_2', 'vehicle_5_vehicle_lane_change_3', 'vehicle_5_vehicle_speed_3', 'vehicle_5_vehicle_lane_change_4', 'vehicle_5_vehicle_speed_4'], 
       'is_bug': 1,
        'bug_type': 1, 
        'xl': array([   0. ,    0. ,    0. ,    0. ,    0. ,  -90. ,    0. ,    0. ,
          0. ,    0. ,    6. ,    0. ,   56. ,    0. ,   15. ,   -3.5,
          0. , -100. ,    0. , -100. ,    0. , -100. ,    0. , -100. ,
            ...
          0. , -100. ,    0. , -100. ,    0. , -100. ,    0. , -100. ,
          0. ,  -15. ,    3.5,    0. , -100. ,    0. , -100. ,    0. ,
       -100. ,    0. , -100. ,    0. , -100. ,    0. , -100. ]), 
       'xu': array([100. ,  80. ,  80. ,  50. , 360. ,  90. ,  15. , 100. ,  40. ,
       ...
        50. ,   2. ,  50. ,   2. ,  50. ,   2. ,  50. ,  27. , -15. ,
         3.5,   0. ,  50. ,   2. ,  50. ,   2. ,  50. ,   2. ,  50. ,
         2. ,  50. ,   2. ,  50. ]), 
         'mask': ['real', 'real', 'real', 'real', 'real', 'real', 'real', 'real', 'real', 'real', 'int', 'real', 'int', 'int', 'real', 'real', 'real', 'real', 'int', 'real', 'int', 'real', 'int', 'real', 'int', 'real', 'int', 
         ...
         'real', 'int', 'real', 'int', 'real', 'int', 'real', 'real', 'real', 'real', 'int', 'real', 'int', 'real', 'int', 'real', 'int', 'real', 'int', 'real'], 
         'fuzzing_content': <tools.sim.op_script.setup_labels_and_bounds.emptyobject object at 0x7f3a56e53400>, 'fuzzing_arguments': "Namespace(adv_conf_th=-4, algorithm_name='nsga2', attack_stop_conf=0.9, carla_path='/home/ubuntu/Documents/self-driving-cars/carla_0911_rss/CarlaUE4.sh', check_unique_coeff=[0, 0.1, 0.5], chosen_labels=[], consider_interested_bugs=1, correct_spawn_locations_after_run=0, debug=1, default_objectives=array([130.,   0.,   0.,   1.,   0.,   0.,   0.]), ego_car_model='op', emcmc=0, episode_max_time=200, finish_after_has_run=1, gpus='0,1', grid_dict_name='grid_dict_one_ped_town07', grid_start_index=0, has_display='0', has_run_num=500, initial_fit_th=100, mating_max_iterations=200, max_running_time=86400, mean_objectives_across_generations_path='run_results_op/nsga2/Town06_Opt_forward/Town06_Opt_forward/op/2023_08_04_00_43_21,50_10_none_500_coeff_0_0.1_0.5_only_unique_0/mean_objectives_across_generations.txt', min_bug_num_to_fit_dnn=10, model_type='one_output', n_gen=10, n_offsprings=300, no_simulation_data_path=None, normalize_objective=1, objective_labels=['min_d', 'collision', 'speed', 'd_angle_norm', 'is_bug', 'fusion_error_perc', 'diversity'], objective_weights=array([ 1.,  0.,  0.,  0., -1., -2.,  0.]), only_run_unique_cases=0, outer_iterations=3, parent_folder='run_results_op/nsga2/Town06_Opt_forward/Town06_Opt_forward/op/2023_08_04_00_43_21,50_10_none_500_coeff_0_0.1_0.5_only_unique_0/', pgd_eps=1.01, pop_size=50, ports=[2003], random_seed=0, rank_mode='none', ranking_model='nn_pytorch', record_every_n_step=2000, regression_nn_use_running_data=1, root_folder='run_results_op', route_type='Town06_Opt_forward', sample_avoid_ego_position=1, sample_multiplier=200, scenario_type='Town06_Opt_forward', simulator='carla_op', standardize_objective=1, survival_multiplier=1, synthetic_function='', terminate_on_collision=1, termination_condition='generations', traj_dist_metric='nearest', uncertainty='', use_single_nn=1, use_single_objective=1, use_unique_bugs=0, warm_up_len=-1, warm_up_path=None)", 
         'sim_specific_arguments': "{'route_info': {'town_name': 'Town06_Opt', 'location_list': [(586.908142, -20.562836, 0.3, 0.0, -179.580566, 0.0), (426.908142, -20.562836, 0.3, 0.0, -179.580566, 0.0)]}, 'ego_start_position': (586.908142, -20.562836, -179.580566), 'carla_path': '/home/ubuntu/Documents/self-driving-cars/carla_0911_rss/CarlaUE4.sh', 'client': None, 'ego_car_model_final': None, 'ego_final_start_time': 0, 'kd_tree': <sklearn.neighbors._kd_tree.KDTree object at 0x5597ec4c1160>}", 'dt_arguments': <customized_utils.emptyobject object at 0x7f3995636fd0>, 'counter': 44, 'trajectory_vector': array([1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0.,
       0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0.,
       0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0.,
       ...
       0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
       0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
       0., 0., 0., 0.]), 'fuzzing_content_text': "{'labels': ['cloudiness', 'precipitation', 'precipitation_deposits', 'wind_intensity', 'sun_azimuth_angle', 'sun_altitude_angle', 'fog_density', 'fog_distance', 'wetness', 'fog_falloff', 'num_of_vehicles', 'delay_time_to_start', 'ego_maximum_speed', 'num_of_vehicle_types_0', 'vehicle_x_0', 'vehicle_y_0', 'vehicle_yaw_0', 'vehicle_speed_0', 'vehicle_0_vehicle_lane_change_0', 'vehicle_0_vehicle_speed_0', 'vehicle_0_vehicle_lane_change_1', 'vehicle_0_vehicle_speed_1', 
       ...
       'vehicle_speed_5', 'vehicle_5_vehicle_lane_change_0', 'vehicle_5_vehicle_speed_0', 'vehicle_5_vehicle_lane_change_1', 'vehicle_5_vehicle_speed_1', 'vehicle_5_vehicle_lane_change_2', 'vehicle_5_vehicle_speed_2', 'vehicle_5_vehicle_lane_change_3', 'vehicle_5_vehicle_speed_3', 'vehicle_5_vehicle_lane_change_4', 'vehicle_5_vehicle_speed_4'],
       ...
```

For the additional information, please refer to [here](https://www.notion.so/donghwan-shin/Interpretation-of-generated-scenarios-cb389f521f4e440f8beee0336142907d?pvs=4)



### Rerun previous simulations

```
cd ~/openpilot/tools/sim/op_script
python rerun_carla_op.py -p <path-to-the-parent-folder-consisting-of-single-simulation-runs-indexed-by-numbers>

```

## Get metadata on generated scenarios

### Simple description of program structure

- `[MyProblem` class](https://github.com/ADS-Testing/ADFuzz/blob/main/ga_fuzzing.py#L148)
    - `init()`: set `xl`, `xu`, the boundaries of fuzzing
    - `[_evaluate(self, X, out, *args, **kwargs)](https://github.com/ADS-Testing/ADFuzz/blob/main/ga_fuzzing.py#L239)`
        - `MyProblem` class is extended from `Problem` from [Pymoo](https://pymoo.org/problems/definition.html#:~:text=In%20pymoo%20the%20problem%20is,the%20__init__%20method), there and there is no certain code calling `_evaluate()`. Pymoo supports the interface calling this.
        
        ```python
        def _evaluate(self, X, out, *args, **kwargs):
          ...
          for i in range(X.shape[0]):
            ...
            try:
                p = Process(target=fun, args=(self, x, launch_server, self.counter, port, return_dict))
                p.start()
                p.join(240)
                if p.is_alive():
                    print("Function is hanging!")
                    p.terminate()
                    print("Kidding, just terminated!")
            except:
                traceback.print_exc()
                objectives, run_info, has_run = default_objectives, None, 0
        
        ```
        
- `[fun(obj, x, launch_server, counter, port, return_dict)](https://github.com/ADS-Testing/ADFuzz/blob/main/ga_fuzzing.py#L115)`
    
    ```python
    if not_critical_region or violate_constraints:
        returned_data = [default_objectives, None, 0]
    else:
        objectives, run_info  = run_simulation(x, fuzzing_content, fuzzing_arguments, sim_specific_arguments, dt_arguments, launch_server, counter, port)
    
        print('\\n'*3)
        print("counter:", counter, " run_info['is_bug']:", run_info['is_bug'], " run_info['bug_type']:", run_info['bug_type'], " objectives:", objectives)
        print('\\n'*3)
    
        # correct_travel_dist(x, labels, customized_data['tmp_travel_dist_file'])
        returned_data = [objectives, run_info, 1]
    if return_dict is not None:
        return_dict['returned_data'] = returned_data
    return returned_data
    
    ```
    
- `[run_op_simulation(x, fuzzing_content, fuzzing_arguments, sim_specific_arguments, dt_arguments, launch_server, sim_counter, port)](https://github.com/ADS-Testing/openpilot/blob/main/tools/sim/op_script/bridge_multiple_sync3.py#L948)`
    - This function is from the customized openpilot repository
- `[bridge(customized_data, arguments, sim_specific_arguments, launch_server, port)](https://github.com/AIasd/openpilot/blob/main/tools/sim/op_script/bridge_multiple_sync3.py#L447)`
    - Executes the openpilot script with a subprocess, then step it by frame unit.
    
    ```python
    while 1:
          # -1. Check end conditions
          # 0. Send current time, tick the world, and send sensor data
          # 1. Read the throttle, steer and brake from op or manual controls
          # 2. Set instructions in Carla
          # 3. Send current carstate to op via can
          # if counter >= 18:
          #     break
    
    ```
    
    - Finally, the fuzzed input passed into the CARLA simulater are `customized_data`, `arguments`, `sim_specific_arguments` of the function parameters.

### Checking metadata by modifying script

- In sake of re-running the scenarios, [metadata of failure scenarios](https://github.com/AIasd/openpilot/blob/main/tools/sim/op_script/bridge_multiple_sync3.py#L1054) is saved in a pickle file.
- In order to observe the generated failure scenarios by text, we can modify the script like [this](https://github.com/ADS-Testing/openpilot/commit/eae98ca188cab046cd75be082b3bc4892bb47fdc)

### Structure of the scenario metadata

All of the information of generated scenario will be saved in cur_info.pickle by [following format](https://github.com/ADS-Testing/openpilot/blob/main/tools/sim/op_script/bridge_multiple_sync3.py#L1054)

- Please refer to [this page](https://www.notion.so/doc/scenario_input.md)

TODO: generated scenario  => 시나리오가 cur_info 안에 있음을 명시해주고 form 설명해주기.

### Get .gif file of the failure scenarios

- Once you have the time series data of images of the failure scenarios, follow the [code](https://github.com/ADS-Testing/openpilot/blob/main/tools/sim/op_script/extract_gif.py). Provided code uploads the simulation metadata and the gif file to the s3 as well, however you can utilize the code to the way as you want.
- Execpted result
    
    ![/doc/figures/failure_output.gif](/doc/figures/failure_output.gif)
    

## Links to the troubleshooting wiki

- [Save meatadata to txt](https://github.com/ADS-Testing/Main/wiki/%5BFusED---Openpilot%5D-Save-metadata-to-txt)
- [Gif generation script](https://github.com/ADS-Testing/Main/wiki/%5BFusED---Openpilot%5D-Gif-generation-script)

## Authors

### Original source

```
@inproceedings{zhong2022detecting,
  title={Detecting multi-sensor fusion errors in advanced driver-assistance systems},
  author={Zhong, Ziyuan and Hu, Zhisheng and Guo, Shengjian and Zhang, Xinyang and Zhong, Zhenyu and Ray, Baishakhi},
  booktitle={Proceedings of the 31st ACM SIGSOFT International Symposium on Software Testing and Analysis},
  pages={493--505},
  year={2022}
}

```

### Replicated and modified by

- [Kyungwook Nam](https://github.com/nkwook)
- [Taehyun Ahn](https://dev.paxtaeo.com/en)
- Advised by [Donghwan Shin](https://www.dshin.info/)

## Reference

This repo leverages code from [Carla Challenge (with LBC supported)](https://github.com/bradyz/2020_CARLA_challenge) and [pymoo](https://github.com/anyoptimization/pymoo)

## License

[MIT License](https://www.notion.so/LICENSE.md)