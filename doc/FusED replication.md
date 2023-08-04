# FusED replication docs
Based on [original repo](https://github.com/AIasd/ADFuzz/blob/main/doc/stack5_carla_openpilot.md)  

## Requirements
* Monitor (i.e., due to the limitation of OpenPilot, the simulation can only run on a machine with a monitor/virtual monitor)
* OS: Ubuntu 20.04
* CPU: at least 4 cores
* GPU: at least 6GB memory
* Storage(SSD recommended): at least 150GB
* Openpilot 0.8.5 (customized)
* Carla 0.9.11
* Python 3.8.5(readme 참고해서 pyenv 설치하면 됨)

## Environmental Setup 
### Install pyenv and python3.8

install pyenv
```
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
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

#### Directory Structure
~(home folder)
```
├── openpilot
├── Documents
│   ├── self-driving-cars (created by the user manually)
│   │   ├── ADFuzz
│   │   ├── carla_0911_rss
```

### Python package installation

In `~/Docuements/self-driving-cars`,
```
git clone https://github.com/ADS-Testing/ADFuzz.git
```

Install environment
```
pipenv install
```

Install pytorch on its official website via pip.

Install pytroch-lightening, torchvision
```
pip3 install pytorch-lightning==0.8.5
pip install torchvision
```

### Install OpenPilot 0.8.5 (customized)
In `~`,
```
git clone https://github.com/ADS-Testing/openpilot.git
```
In `~/openpilot`,
```
./tools/ubuntu_setup.sh
```
* Once you get `ERROR: Couldn't install package: pprofile` message, just hit the `pip install pprofile` again.

In `~/openpilot`, compile Openpilot
```
scons -j $(nproc)
```

### Common Compilation Issue
clang 10 is needed. To install it, run
```
sudo apt install clang
```

### Common OpenCL Issue
Your environment needs to support opencl 2.0+ in order to run `scons` successfully (when using `clinfo`, it must show something like  "your OpenCL library only supports OpenCL <2.0+>")

### Install Carla 0.9.11
In `~/Documents/self-driving-cars`,
```
curl -O https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/CARLA_0.9.11_RSS.tar.gz
mkdir carla_0911_rss
tar -xvzf CARLA_0.9.11_RSS.tar.gz -C carla_0911_rss
```

In `~/Documents/self-driving-cars/carla_0911_rss/PythonAPI/carla/dist`,
```
sudo apt-get install python-setuptools
sudo python -m easy_install carla-0.9.11-py3.7-linux-x86_64.egg
```

### Install additional maps
In `~/Documents/self-driving-cars/carla_0911_rss`,
```
curl -O https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/AdditionalMaps_0.9.11.tar.gz
mv AdditionalMaps_0.9.11.tar.gz Import/

```
and then run
```
./ImportAssets.sh
```

## How to run 
### Run fuzzing(Scenario generation)
```
  python ga_fuzzing.py --simulator carla_op --n_gen 10 --pop_size 50 --algorithm_name nsga2 --has_run_num 500 --episode_max_time 200 --only_run_unique_cases 0 --objective_weights 1 0 0 0 -1 -2 0 -m op --route_type 'Town06_Opt_forward'
```
Results will be saved in `run_results_op` folder. In case of the failure scenarios, following informations will be saved.
* Camera snapshots of front and top sides
* Failure situation: `tmp_data`
* Trajectory data: `simlulation_data`
* Running information: `cur_info`  

### Rerun previous simulations
In `~/openpilot/tools/sim/op_script`,
```
python rerun_carla_op.py -p <path-to-the-parent-folder-consisting-of-single-simulation-runs-indexed-by-numbers>
```

## Get metadata on generated scenarios
### Simple description of program structure
* [`MyProblem` class](https://github.com/ADS-Testing/ADFuzz/blob/main/ga_fuzzing.py#L148) 
  - `init()`: set `xl`, `xu`, the boundaries of fuzzing
  - [`_evaluate(self, X, out, *args, **kwargs)`](https://github.com/ADS-Testing/ADFuzz/blob/main/ga_fuzzing.py#L239)
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
- [`fun(obj, x, launch_server, counter, port, return_dict)`](https://github.com/ADS-Testing/ADFuzz/blob/main/ga_fuzzing.py#L115)
  ```python
  if not_critical_region or violate_constraints:
      returned_data = [default_objectives, None, 0]
  else:
      objectives, run_info  = run_simulation(x, fuzzing_content, fuzzing_arguments, sim_specific_arguments, dt_arguments, launch_server, counter, port)

      print('\n'*3)
      print("counter:", counter, " run_info['is_bug']:", run_info['is_bug'], " run_info['bug_type']:", run_info['bug_type'], " objectives:", objectives)
      print('\n'*3)

      # correct_travel_dist(x, labels, customized_data['tmp_travel_dist_file'])
      returned_data = [objectives, run_info, 1]
  if return_dict is not None:
      return_dict['returned_data'] = returned_data
  return returned_data
  ```
- [`run_op_simulation(x, fuzzing_content, fuzzing_arguments, sim_specific_arguments, dt_arguments, launch_server, sim_counter, port)`](https://github.com/ADS-Testing/openpilot/blob/main/tools/sim/op_script/bridge_multiple_sync3.py#L948)
  - This function is from the customized openpilot repository
- [`bridge(customized_data, arguments, sim_specific_arguments, launch_server, port)`](https://github.com/AIasd/openpilot/blob/main/tools/sim/op_script/bridge_multiple_sync3.py#L447)
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
- Please refer to [this page](/doc/scenario_input.md)

### Get .gif file of the failure scenarios
- Once you have the time series data of images of the failure scenarios, follow the [code](https://github.com/ADS-Testing/openpilot/blob/main/tools/sim/op_script/extract_gif.py). Provided code uploads the simulation metadata and the gif file to the s3 as well, however you can utilize the code to the way as you want. 
- Execpted result  
![src](/doc/figures/failure_output.gif)

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
[MIT License](/LICENSE.md)

















