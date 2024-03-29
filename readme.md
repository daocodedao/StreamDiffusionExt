
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


pip install -r requirements.txt

python setup.py develop easy_install streamdiffusion[tensorrt]
python -m streamdiffusion.tools.install-tensorrt
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
cd /data/work/StreamDiffusion
./start-txt-img.sh
```
## 图片图片
```
# 启动 txt2img 端口： 9091
cd /data/work/StreamDiffusion
./start-img-img.sh
```

## vid2vid
```
# 启动 vid2vid 端口： 9092
cd /data/work/StreamDiffusion
./start-vid-vid.sh  
```

## example
### vid2vid
```
cd /data/work/StreamDiffusion
source venv_steam_diff/bin/activate 
python examples/vid2vid/main.py --input resource/input/奢奢夫人.mp4 --output resource/output/outvid.mp4 --prompt "girls with red hair" --model_id ./models/Model/kohaku-v2.1.safetensors 

python examples/vid2vid/main.py --input resource/input/2088_1705490330.mp4 --output resource/output/2088_1705490330_out.mp4 --prompt "girls with red hair" --model_id ./models/Model/kohaku-v2.1.safetensors 


```

### txt2img
```
cd /data/work/StreamDiffusion
source venv_steam_diff/bin/activate 
python examples/txt2img/single.py --output ./resource/output/outtxt.png --prompt "1girl with brown dog ears, thick frame glasses" --model_id_or_path ./models/Model/kohaku-v2.1.safetensors

# turbo
python examples/txt2img/single.py --output ./resource/output/outtxt.png --prompt "1girl with brown dog ears, thick frame glasses" --model_id_or_path ./models/sd_turbo/sd_turbo.safetensors
```


### img2img
参考 https://github.com/radames/Real-Time-Latent-Consistency-Model/tree/main?tab=readme-ov-file
https://huggingface.co/collections/latent-consistency/latent-consistency-model-demos-654e90c52adb0688a0acbe6f
```
cd /data/work/StreamDiffusion
source venv_steam_diff/bin/activate 
python examples/img2img/single.py --input ./resource/input/in.png --output ./resource/output/outimg.png --prompt "girls with red hair" --model_id_or_path ./models/Model/kohaku-v2.1.safetensors


./start-gradio-img-img.sh
```


# 常见问题

```
ValueError: When localhost is not accessible, a shareable link must be created. Please set share=True or check your proxy settings to allow access to localhost.

export no_proxy="localhost, 127.0.0.1, ::1"

```


