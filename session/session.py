import logging
import requests
import json
import time
import webbrowser

class WQSession(requests.Session):
    def __init__(self, json_fn='credentials.json'):
        super().__init__()
        self.json_fn = json_fn

        #실제 로그인 여기서 아이디, 비번 읽고 post로그인, Session쿠키 저장, 이후 모든 요청에 자동 사용 기능 포함.
        self.login()

        #timeout되어도 재실행될수있도록 설계
        old_get = self.get
        def new_get(*args, **kwargs):
            for _ in range(5):
                try:
                    return old_get(*args, **kwargs)
                except Exception:
                    time.sleep(1)
            raise Exception("GET failed after 5 retries")
        
        old_post = self.post
        def new_post(*args, **kwargs):
            for _ in range(5):
                try:
                    return old_post(*args, **kwargs)
                except Exception:
                    time.sleep(1)
            raise Exception("POST failed after 5 retries")
        self.get = new_get
        self.post = new_post
        #만료 플래그. Unauthorized만료되면 True로 바뀌어 재로그인 시도가능
        self.login_expired = False

    def login(self):
        try:
            with open(self.json_fn, 'r') as f:
                creds = json.loads(f.read())
                email, password = creds['email'], creds['password']
                self.auth = (email, password)
                r = self.post('https://api.worldquantbrain.com/authentication')
        except FileNotFoundError:
            logging.error(f"Credentials file {self.json_fn} not found. Please create it based on credentials.json.example")
            raise
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in {self.json_fn}")
            raise
        except KeyError as e:
            logging.error(f"Missing key in credentials: {e}")
            raise
            
        if 'user' not in r.json():
            if 'inquiry' in r.json():
                auth_url = f"{r.url}/persona?inquiry={r.json()['inquiry']}"
                print(f"🔐 생체 인증이 필요합니다.")
                print(f"🌐 브라우저에서 인증 페이지를 여는 중...")
                print(f"📱 인증 링크: {auth_url}")
                
                # 자동으로 브라우저에서 인증 페이지 열기
                try:
                    webbrowser.open(auth_url)
                    print(f"✅ 브라우저에서 인증 페이지가 열렸습니다!")
                except Exception as e:
                    print(f"⚠️ 브라우저를 자동으로 열 수 없습니다: {e}")
                    print(f"📋 수동으로 다음 링크를 복사해서 브라우저에 붙여넣으세요:")
                    print(f"🔗 {auth_url}")
                
                input(f"생체 인증을 완료한 후 엔터를 눌러주세요...")
                self.post(f"{r.url}/persona", json=r.json())
            else:
                print(f'WARNING! {r.json()}')
                input('Press enter to quit...')
        logging.info('Logged in to WQBrain!')