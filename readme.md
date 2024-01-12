
# 说明
源项目  https://github.com/cumulo-autumn/StreamDiffusion


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
# 启动 txt2img 端口：9090
./start-txt-img.sh

```
## 图片图片
```
# 启动 txt2img 端口：9091
./start-img-img.sh

```

## vid2vid
```
# 启动 vid2vid 端口：9092
./start-vid-vid.sh

```


```
# 代码里加入这个，可以下载huggingface
import os
os.environ['HTTP_PROXY'] = '192.168.0.77:18808'
os.environ['HTTPS_PROXY'] = '192.168.0.77:18808'

```


# frp

```
cat /data/work/frp/frpc.ini 
vim /data/work/frp/frpc.ini 

[ssh-stream-diffusion-txt-img]
type = tcp
local_ip = 127.0.0.1
local_port = 9090
remote_port = 9090
use_encryption = false
use_compression = false

[ssh-stream-diffusion-vid]
type = tcp
local_ip = 127.0.0.1
local_port = 9092
remote_port = 9092
use_encryption = false
use_compression = false


# 重启frp
sudo supervisorctl reload

```





```
scp -r /data/work/StreamDiffusion fxbox@192.168.0.67:/data/work
```



```
ValueError: When localhost is not accessible, a shareable link must be created. Please set share=True or check your proxy settings to allow access to localhost.



export no_proxy="localhost, 127.0.0.1, ::1"

```