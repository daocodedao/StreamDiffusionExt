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

CONTENT_STREAM=None

def generateImage(
    # input,
    input: str = os.path.join(CURRENT_DIR, "..", "..", "images", "inputs", "input.png"),
    output: str = os.path.join(CURRENT_DIR, "..", "..", "images", "outputs", "output.png"),
    model_id_or_path: str = "./models/Model/kohaku-v2.1.safetensors",
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
    global CONTENT_STREAM
    if guidance_scale <= 1.0:
        cfg_type = "none"

    device = "cuda"
    # device_ids = ["cuda"]
    if Util.isMac():
        device = "mps"
        # device_ids = ["cpu"]

    os.makedirs(os.path.dirname(output), exist_ok=True)

    if CONTENT_STREAM is None:
        CONTENT_STREAM = StreamDiffusionWrapper(
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

    print(f"CONTENT_STREAM.prepare")
    CONTENT_STREAM.prepare(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=50,
        guidance_scale=guidance_scale,
        delta=delta,
    )

    print(f"CONTENT_STREAM.preprocess_image(input)")
    image_tensor = CONTENT_STREAM.preprocess_image(input)

    for _ in range(CONTENT_STREAM.batch_size - 1):
        CONTENT_STREAM(image=image_tensor)

    print(f"CONTENT_STREAM(image=image_tensor)")
    output_image = CONTENT_STREAM(image=image_tensor)
    output_image.save(output)
    
    return output_image


def generate_file(file_obj):

    # return file_obj.rotate(45)

    # outImage = generateImage(input = file_obj)
    # return outImage
    global tmpdir
    print('临时文件夹地址：{}'.format(tmpdir))
    print('上传文件的地址：{}'.format(file_obj))  # 输出上传后的文件在gradio中保存的绝对地址

    dirname, filename = os.path.split(file_obj)

    outFileName = f"out_{filename}"
    outFilePath = os.path.join(tmpdir, outFileName)
    os.makedirs(tmpdir, exist_ok=True)

    try:
        generateImage(input = file_obj, output=outFilePath)
        print(f"generateImage 成功：{outFilePath}")

    except Exception as e:
        print(e)
        print(f"generateImage 失败：{outFilePath}")

    # 返回新文件的的地址（注意这里）
    return outFilePath

def main():
    global tmpdir
    os.makedirs('./tmp/', exist_ok=True)
    with gr.Blocks() as demo:
        with gr.Row():
            with tempfile.TemporaryDirectory(dir='./tmp/') as tmpdir:
                # 定义输入和输出
                # inputs = gr.components.File(label="上传文件", file_types=["png", "jpg", "jpeg"])
                # outputs = gr.components.File(label="下载文件", file_types=["png", "jpg", "jpeg"])
                image_input = gr.Image(type="filepath")
                image_output = gr.Image(type="filepath")

        with gr.Row():
            gen_button = gr.Button("生成图片")
        with gr.Row():
            with gr.Accordion("demo"):
                gr.Markdown("<div align='center'>  </div>")

        gen_button.click(generate_file, inputs=image_input, outputs=image_output)

        # demo.launch(share=False, server_port=6006)
        demo.launch(share=False, server_port=9091, ssl_verify=False, debug=True, show_error=True)

if __name__ == "__main__":
    main()