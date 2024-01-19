import gradio as gr

import os
import sys
from typing import Literal, Dict, Optional
import tempfile
import fire
import torch

from tqdm import tqdm

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from utils.wrapper import StreamDiffusionWrapper
from utils.util import Util

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

import torch
from diffusers import AutoencoderTiny, StableDiffusionPipeline
from diffusers.utils import load_image

from streamdiffusion import StreamDiffusion
from streamdiffusion.image_utils import postprocess_image

def generateImage(
    input: str = os.path.join(CURRENT_DIR, "..", "..", "images", "inputs", "input.png"),
    output: str = os.path.join(CURRENT_DIR, "..", "..", "images", "outputs", "output.png"),
    model_id_or_path: str = "KBlueLeaf/kohaku-v2.1",
    lora_dict: Optional[Dict[str, float]] = None,
    prompt: str = "1girl with brown dog hair, thick glasses, smiling",
    negative_prompt: str = "low quality, bad quality, blurry, low resolution",
    width: int = 512,
    height: int = 512,
    acceleration: Literal["none", "xformers", "tensorrt"] = "xformers",
    use_denoising_batch: bool = True,
    guidance_scale: float = 1.2,
    cfg_type: Literal["none", "full", "self", "initialize"] = "self",
    seed: int = 2,
    delta: float = 0.5,
):
    if guidance_scale <= 1.0:
        cfg_type = "none"

    device = "cuda"
    # device_ids = ["cuda"]
    if Util.isMac():
        device = "mps"
        # device_ids = ["cpu"]

    os.makedirs(os.path.dirname(output), exist_ok=True)

    stream = StreamDiffusionWrapper(
        model_id_or_path=model_id_or_path,
        lora_dict=lora_dict,
        t_index_list=[22, 32, 45],
        frame_buffer_size=1,
        width=width,
        height=height,
        warmup=10,
        acceleration=acceleration,
        mode="img2img",
        use_denoising_batch=use_denoising_batch,
        cfg_type=cfg_type,
        seed=seed,
        use_lcm_lora = True,
        lcm_lora_id = "./models/LoRA/pytorch_lora_weights.safetensors",
        # device_ids = device_ids,
        device = device
    )

    stream.prepare(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=50,
        guidance_scale=guidance_scale,
        delta=delta,
    )

    image_tensor = stream.preprocess_image(input)

    for _ in range(stream.batch_size - 1):
        stream(image=image_tensor)

    output_image = stream(image=image_tensor)
    output_image.save(output)
    
    return output


def generate_file(file_obj):
    global tmpdir
    print('临时文件夹地址：{}'.format(tmpdir))
    print('上传文件的地址：{}'.format(file_obj.name))  # 输出上传后的文件在gradio中保存的绝对地址

    dirname, filename = os.path.split(file_obj.name)

    outFileName = f"out_{filename}"
    outFilePath = os.path.join(tmpdir, outFileName)
    os.makedirs(tmpdir, exist_ok=True)

    try:
        generateImage(input = file_obj.name, output=outFilePath)
    except Exception as e:
        print(e)
        print(f"generateImage 失败")

    # 返回新文件的的地址（注意这里）
    return outFilePath

def main():
    global tmpdir
    os.makedirs('./tmp/', exist_ok=True)
    with gr.Blocks() as demo:
        with gr.Row():
            with tempfile.TemporaryDirectory(dir='./tmp/') as tmpdir:
                # 定义输入和输出
                inputs = gr.components.File(label="上传文件", file_types=["png", "jpg", "jpeg"])
                outputs = gr.components.File(label="下载文件", file_types=["png", "jpg", "jpeg"])
        with gr.Row():
            gen_button = gr.Button("生成图片")
        with gr.Row():
            with gr.Accordion("demo"):
                gr.Markdown("<div align='center'>  </div>")

        gen_button.click(generate_file, inputs=inputs, outputs=outputs)

        # demo.launch(share=False, server_port=6006)
        demo.launch(share=False, server_port=9091, ssl_verify=False, debug=True, show_error=True)

if __name__ == "__main__":
    main()