
# 说明
https://github.com/daocodedao/StreamDiffusionExt.git


源项目  https://github.com/cumulo-autumn/StreamDiffusion
Jan 8, 2024 commit id: 8ff959a3ae6536f33d6f0fbf809e9b620e346978


# 安装
## 环境 

```
python3.10 -m venv venv_steam_diff
source venv_steam_diff/bin/activate


# 查看 cuda 版本
cat /usr/local/cuda/version.json
ls -l /usr/local | grep cuda
/usr/local/cuda/bin/nvcc --version


# cuda11.8
pip3 install torch==2.1.0 torchvision==0.16.0 xformers --index-url https://download.pytorch.org/whl/cu118

```

# 安装 npm
```
sudo apt update
sudo apt install -y nodejs
sudo apt install -y npm

https://weekendprojects.dev/posts/fixed-npm-install-error-missing-required-argument-1/
curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
source ~/.profile
nvm install node 
```
# 项目启动
## 文字图片

```
# 启动 txt2img 端口： 9090
cd /data/work/generative-models
./start-txt-img.sh
```
## 图片图片
```
# 启动 txt2img 端口： 9091
cd /data/work/generative-models
./start-img-img.sh
```

## vid2vid
```
# 启动 vid2vid 端口： 9092
cd /data/work/generative-models
./start-vid-vid.sh  
```
## vid2vid example
```
cd examples
python vid2vid/main.py --input resource/input/奢奢夫人.mp4 --output path/to/奢奢夫人_out.mp4

```



# 常见问题

```
ValueError: When localhost is not accessible, a shareable link must be created. Please set share=True or check your proxy settings to allow access to localhost.

export no_proxy="localhost, 127.0.0.1, ::1"

```