import requests
import json

# navseq = [
#     {'speed': 100, 'direction': 5, 'duration': 2},
#     {'speed': 100, 'direction': 355, 'duration': 2},
#     {'speed': 100, 'direction': 5, 'duration': 2},
#     {'speed': 100, 'direction': 355, 'duration': 2},
# ]

def main():
    with open('path.json') as f:
        navseq = json.load(f)
    requests.post('http://192.168.4.1/setnavseq', json=navseq)

if __name__ == '__main__':
    main()