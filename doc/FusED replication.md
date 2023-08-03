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
git clone https://github.com/AIasd/ADFuzz.git
```

Install environment
```
pip3 install -r requirements.txt
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

### Common Python Path Issue
Make sure the python path is set up correctly through pyenv, in particular, run
```
which python
```
One should see the following:
```
~/.pyenv/shims/python
```
Otherwise, one needs to follow the displayed instructions after running
```
pyenv init
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
### Run Fuzzing
```
python ga_fuzzing.py --simulator carla_op --n_gen 10 --pop_size 50 --algorithm_name nsga2 --has_run_num 500 --episode_max_time 200 --only_run_unique_cases 0 --objective_weights 1 0 0 0 -1 -2 0 -m op --route_type 'Town06_Opt_forward'
```
* 

Traceback (most recent call last):
  File "/home/ubuntu/openpilot/selfdrive/manager/manager.py", line 9, in <module>
    import cereal.messaging as messaging
ModuleNotFoundError: No module named 'cereal'