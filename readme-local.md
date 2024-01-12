







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


# 操作

## 拷贝
```
scp -r /data/work/StreamDiffusion fxbox@192.168.0.67:/data/work
```
## 代理

```
# 代码里加入这个，可以下载huggingface
import os
os.environ['HTTP_PROXY'] = '192.168.0.77:18808'
os.environ['HTTPS_PROXY'] = '192.168.0.77:18808'

```