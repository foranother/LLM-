import openai
import requests
from main_utils.singleton import SingletonMeta
from main_utils.disease_vector_gpt import vector_collection
from PyPDF2 import PdfReader



class ChatGPT(metaclass=SingletonMeta):

    
    def run(self, title,disease, item, etc):
        srchres = vector_collection(disease)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role" : "assistant", "content": f"{srchres}"},
                {"role": "system", "content": "너는 간호 전문가야. 유저가 간호 시뮬레이션 시나리오를 생성하는 것을 도와줘"},
                {"role": "user", "content": f"간호학과 학생들이 {title} 환자를 돌보는 시뮬레이션 시나리오를 생성해줘. 시나리오의 목표를 5개 작성해주고, 환자 프로필에 {item}내용을 포함하고 현재 환자의 상태를 포함하여 생성해주고 상황해설을 포함해서 작성해줘. 추가 사항으로는 {etc}가 있어"}
            ]
        )
        return completion.choices[0].message

    def re_run(self,content, chat):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 간호 전문가야. 유저가 간호 시뮬레이션 시나리오를 생성하는 것을 도와줘"},
                {"role": "user", "content": f"{content} 이게 기존에 생성된 시뮬레이션 시나리오이고, {chat} 내용에 맞게 수정해줘"}
            ]
        )
        return completion.choices[0].message
    
    def runscenario(self, content):
        reader = PdfReader('D:/연구실/수업/2-1/융프/웹사이트/simnursebe-main/main_utils/간질 소아 환자 간호.pdf')
        pages = reader.pages
        text = pages[13].extract_text() + pages[14].extract_text()
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role" : "assistant", "content": f"{text}"},
                {"role": "system", "content": "너는 간호 전문가야. 유저가 간호 시뮬레이션 시나리오를 생성하는 것을 도와줘"},
                {"role": "user", "content": f"{content} 이게 기존에 생성된 시뮬레이션 시나리오이고, 이 시나리오에 맞게 간호사와 환자가 대화하는 대화 시나리오 3분짜리로 만들어줘, 한글로 작성해줘"}
            ]
        )
        return completion.choices[0].message
    
    def imagegpt(self, content):
        response = openai.Image.create(
            model="dall-e-3",
            prompt=str(content) + '해당 환자 개요에 맞는 가상환자 이미지를 그려줘',
            n=1,
            size="1024x1024"
        )

        image_url = response['data'][0]['url']
        image_data = requests.get(image_url).content
        with open('output_image.png', 'wb') as handler:
            handler.write(image_data)
        return image_url