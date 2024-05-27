import streamlit as st
from PIL import Image
from glob import glob
import os
import io
import json
import base64
import urllib
import requests

backup_path = "streamlit log"
os.makedirs(backup_path, exist_ok = True)

# 번역
def translation(input_str:str):
    client_id = "YOUR ID"
    client_secret = "YOUR SECRET"
    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"

    data = input_str
    encText = urllib.parse.quote(data)
    data = "source=ko&target=en&text=" + encText # source = 원본 언어, target = 변환할 언어

    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        en_text = json.loads(response_body.decode('utf-8'))['message']['result']['translatedText']
        return en_text
    
# text2img
def t2i(prompt, negative_prompt):
    r = requests.post(
        'https://api.kakaobrain.com/v2/inference/karlo/t2i',
        json = {
            "version": "v2.1", 
            "prompt": prompt,
            "negative_prompt": negative_prompt, 
            "width": 1024,
            "height": 768,
            "return_type": "base64_string",
            "prior_num_inference_steps": 25,
            "prior_guidance_scale": 5.0,
            "num_inference_steps": 50 ,
            "guidance_scale": 5.0,
            "image_format": "png" ,
            "samples": "8" ,
            "upscale": False,
            "scale": 2 ,
        },
        headers = {
            'Authorization': f'KakaoAK YOUR KEY',
            'Content-Type': 'application/json'
        }
    )
    # 응답 JSON 형식으로 변환
    response = json.loads(r.content)
    return response

control_dict = {
    "fixed_prompt_default": "high quality, hyper-detailed, best composition, flat, for storyboard cut scene",
    
    "fixed_negative_prompt_default": "out of frame, low resolution, blurry, worst quality, fuzzy, text, low quality, normal quality, signature, watermark, grainy, bad proportions, cropped, duplicate, malformed, cropped, pixelated, poorly drawn hands, poorly drawn feet, poorly drawn face, body out of frame, distorted face, bad anatomy, missing anatomy, missing body, missing face, missing legs, missing fingers, missing feet, missing toe, fewer digits, extra limbs, extra anatomy, extra face, extra arms, extra fingers, extra hands, extra legs, extra feet, extra toe, mutated hands, ugly, mutilated, disfigured, mutation, bad proportions, cropped head, cross-eye, mutilated, distorted eyes, detailed face, distorted hands, strabismus",
    
    "style": {
        "기본형": {
            "name": "",
            "pos": "",
            "neg": ""
        }, 
        "Pencil sketch with no color": {
            "name": "Pencil sketch with no color",
            "pos": "",
            "neg": "Real pencil"
        }, 
        "Colored pencil": {
            "name": "Colored pencil",
            "pos": "",
            "neg": "Real pencil"
        }, 
        "Webtoon": {
            "name": "Webtoon",
            "pos": "Similar picture",
            "neg": ""
        }, 
        "Watercolor": {
            "name": "Watercolor",
            "pos": "",
            "neg": ""
        }
    },
    
    "angle": {
        "선택 안함": {
            "name": "",
            "pos": "",
            "neg": ""
        }, 
        "High angle shot": {
            "name": "High angle shot",
            "pos": "",
            "neg": ""
        }, 
        "Low angle shot": {
            "name": "Low angle shot",
            "pos": "",
            "neg": ""
        }, 
        "Eye level shot": {
            "name": "Eye level shot",
            "pos": "",
            "neg": ""
        }, 
        "Close up angle": {
            "name": "Close up angle",
            "pos": "",
            "neg": ""
        }, 
        "Full shot": {
            "name": "Full shot",
            "pos": "",
            "neg": ""
        },
        "Overhead view": {
            "name": "Overhead view",
            "pos": "",
            "neg": ""
        },
    },
}

def main():
    st.title("karlo test web page")
    st.write(f"""
    karlo prompt를 실험하기 위한 페이지입니다.\n
    아래 내용을 작성 후 이미지 생성 버튼을 눌러주세요.
    화풍, 카메라 구도 항목은 추가 업데이트 될 수 있습니다.
    
    \nparameter 설명\n
    fixed_prompt: 고정적으로 입력되는 prompt, 보통 고정해 사용합니다.
    
    fixed_negative_prompt: 고정적으로 입력되는 negative prompt, 보통 고정해 사용합니다.
    
    user_input: 그리고 싶은 키워드를 입력하세요. 영어로 자동 번역돼 karlo에 입력됩니다.
    
    image_style: 화풍을 선택해주세요.
    {[i for i in control_dict["style"]]}
    
    camera_angle: 카메라 구도를 선택해주세요. 
    {[i for i in control_dict["angle"]]}""")
    
    with st.form('karlo'):
        fixed_prompt = st.text_input(
            label = "fixed_prompt", 
            value = control_dict["fixed_prompt_default"],
            placeholder = "please enter what you want to add base prompt"
        )
        fixed_negative_prompt = st.text_input(
            label = "fixed_negative_prompt",
            value = control_dict["fixed_negative_prompt_default"],
            placeholder = "please enter what you want to add base negative prompt"
        )
        
        style = st.selectbox("choose your image_style", [i for i in control_dict["style"]])
        angle = st.selectbox("choose your camera_angle", [i for i in control_dict["angle"]])
        
        user_input = st.text_input(
            label = "user_input",
            value = "고양이,나른한 오후,낮잠",
            placeholder = "please enter keyword you want to draw"
        )
        
        if st.form_submit_button(label='이미지 생성'):
            prompt = ", ".join(
                [
                    translation(user_input),
                    control_dict["angle"][angle]["name"],
                    control_dict["style"][style]["name"],
                    control_dict["style"][style]["pos"],
                    control_dict["angle"][angle]["pos"],
                    fixed_prompt
                ]
            ).replace(", ,",",").replace(", ,",",").replace(", ,",",").strip()
            negative_prompt = ", ".join(
                [
                    fixed_negative_prompt,
                    control_dict["style"][style]["neg"], 
                    control_dict["angle"][angle]["neg"]
                ]
            ).replace(", ,",",").replace(", ,",",").strip()
            
            if negative_prompt[-1] == ",":
                negative_prompt = negative_prompt[:-1]
            
            response = t2i(prompt, negative_prompt)
            
            st.write(f"{style}의 긍정 프롬프트, 부정 프롬프트")
            st.write("긍정: " + control_dict["style"][style]["pos"])
            st.write("부정: " + control_dict["style"][style]["neg"])
            st.write("-"*30)
            
            st.write(f"{angle}의 긍정 프롬프트, 부정 프롬프트")
            st.write("긍정: " + control_dict["angle"][angle]["pos"])
            st.write("부정: " + control_dict["angle"][angle]["neg"])
            st.write("-"*30)
            
            st.write("입력된 prompt")
            st.write(prompt)
            st.write("-"*30)
            
            st.write("입력된 negative_prompt")
            st.write(negative_prompt)
            
            
            save_base_name = (backup_path + "/" + user_input + f",{style}" + f",{angle}").replace(",,",",")
            
            if save_base_name[-1] == ",":
                save_base_name = save_base_name[:-1]
            
            for img_num in range(8):
                img_str = response["images"][img_num]["image"]
                imgdata = base64.b64decode(img_str)
                dataBytesIO = io.BytesIO(imgdata)
                PIL_img = Image.open(dataBytesIO)

                st.image(PIL_img)

                cnt = 0
                save_file_lst = glob(backup_path + "/*")
                for i in save_file_lst:
                    if save_base_name in i:
                        cnt += 1

                PIL_img.save(save_base_name + f"_{str(cnt).zfill(4)}" + ".jpg")

if __name__=="__main__":
    main()
