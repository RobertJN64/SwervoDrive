import requests
import json

# navseq = [
#     {'speed': 100, 'direction': 5, 'duration': 2},
#     {'speed': 100, 'direction': 355, 'duration': 2},
#     {'speed': 100, 'direction': 5, 'duration': 2},
#     {'speed': 100, 'direction': 355, 'duration': 2},
# ]

def main():
    navseq = []
    for direction in range(340, 400):
        navseq.append({'speed': 100, 'direction': direction%360, 'duration': 1})
    # with open('path.json') as f:
    #     navseq = json.load(f)
    requests.post('http://localhost/setnavseq', json=navseq)

if __name__ == '__main__':
    main()