import requests
import os
import re

# 1080CN 账户信息
username = os.environ["1080CN_USERNAME"]
password = os.environ["1080CN_PASSWORD"]
# 添加 server 酱通知
sckey = os.environ["SERVERCHAN_SCKEY"]
send_url = "https://sctapi.ftqq.com/%s.send" % (sckey)
send_content = 'Server ERROR'

# 1080CN 签到 url
user_url = "http://www.4k1080.com//member.php?mod=logging&action=login"
base_url = "http://www.4k1080.com/"
signin_url = "http://www.4k1080.com/plugin.php?id=k_misign:sign&operation=qiandao&formhash={formhash}&format=empty"
form_data = {
    'formhash': "",
    'referer': "http://www.4k1080.com/",
    'username': username,
    'password': password,
    'questionid': "0",
    'answer': ""
}
inajax = '&inajax=1'

def run(form_data):
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'})
    headers = {"Content-Type": "text/html", 'Connection': 'close'}
    user_resp = s.get(user_url,headers=headers)
    login_text = re.findall('action="(.*?)"', user_resp.text)
    for loginhash in login_text:
        if 'loginhash' in loginhash:
            login_url = base_url + loginhash + inajax
            login_url = login_url.replace("amp;", "")
            print(login_url)
    form_text = re.search('formhash=(.*?)\'', user_resp.text)
    print(form_text.group(1))
    form_data['formhash'] = form_text.group(1)
    print(form_data)

    login_resp = s.post(login_url, data=form_data)
    test_resp = s.get('http://www.4k1080.com/k_misign-sign.html',headers=headers)
    if username in test_resp.text:
      print('login!')
    else:
      return 'login failed!'
    signin_text = re.search('formhash=(.*?)"', test_resp.text)
    signin_resp = s.get(signin_url.format(formhash=signin_text.group(1)))
    test_resp = s.get('http://www.4k1080.com/k_misign-sign.html',headers=headers)
    if '您的签到排名' in test_resp.text:
      print('signin!')
    else:
      return 'signin failed!'


if __name__ == "__main__":
  signin_log = run(form_data)
  if signin_log is None:
    send_content = "1080CN 每日签到成功！"
    print('Sign in automatically!')
  else:
    send_content = signin_log
    print(signin_log)
  params = {'text': '1080CN 每日签到结果通知：', 'desp': send_content}
  requests.post(send_url, params=params)
  print('已通知 server 酱')

