import time
import requests


def main():
    origin = 'http://127.0.0.1:5000'
    s = requests.Session()
    files = {'file': open('test_data.csv', 'rb')}
    resp = s.post(origin + '/api/calculateDistance', files=files)
    task_id = resp.json()['task_id']
    while True:
        time.sleep(1.0)
        r = s.get('/api/getResults?task_id='+ task_id)
        data = r.json()
        print(data)
        if data["status"] == "done":
            break


if __name__ == '__main__':
    main()
