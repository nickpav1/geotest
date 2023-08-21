import time
import requests


def main():
    s = requests.Session()
    files = {'file': open('data.csv', 'rb')}
    resp = s.post('http://127.0.0.1:5000/api/calculateDistance', files=files)
    task_id = resp.json()['task_id']
    while True:
        time.sleep(1.0)
        r = s.get('http://127.0.0.1:5000/api/getResults?task_id='+ task_id)
        data = r.json()
        print(data)
        if data["status"] == "done":
            break


if __name__ == '__main__':
    main()
