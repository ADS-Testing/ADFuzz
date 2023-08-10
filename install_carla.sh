cd ~/Documents/self-driving-cars
curl -O <https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/CARLA_0.9.11_RSS.tar.gz>
mkdir carla_0911_rss
tar -xvzf CARLA_0.9.11_RSS.tar.gz -C carla_0911_rss
cd ~/Documents/self-driving-cars/carla_0911_rss/PythonAPI/carla/dist
sudo apt-get install python-setuptools
sudo python -m easy_install carla-0.9.11-py3.7-linux-x86_64.egg
cd ~/Documents/self-driving-cars/carla_0911_rss
curl -O <https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/AdditionalMaps_0.9.11.tar.gz>
mv AdditionalMaps_0.9.11.tar.gz Import/
./ImportAssets.sh
