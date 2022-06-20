import requests
import json

# navseq = [
#     {'speed': 10, 'direction': 0, 'duration': 0.5},
#     {'speed': 100, 'direction': 0, 'duration': 1.5},
#     {'speed': 10, 'direction': 90, 'duration': 0.5},
#     {'speed': 100, 'direction': 90, 'duration': 1.5},
#     {'speed': 10, 'direction': 180, 'duration': 0.5},
#     {'speed': 100, 'direction': 180, 'duration': 1.5},
#     {'speed': 10, 'direction': 270, 'duration': 0.5},
#     {'speed': 100, 'direction': 270, 'duration': 1.5},
# ]

def main():
    with open('path.json') as f:
        navseq = json.load(f)
    requests.post('http://192.168.4.1/setnavseq', json=navseq)

if __name__ == '__main__':
    main()