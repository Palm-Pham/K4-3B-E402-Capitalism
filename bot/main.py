"""Interactive local console; does not connect to or post on Discord."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from codebase.agent import classify_context

if __name__ == '__main__':
    print('TA Context CP3 — nhập /quit để thoát. Web demo: python -m codebase.server')
    while True:
        try:
            message = input('Student: ')
        except (EOFError, KeyboardInterrupt):
            break
        if message == '/quit':
            break
        if message.strip():
            result = classify_context(message)
            print(json.dumps(result, ensure_ascii=False, indent=2))
