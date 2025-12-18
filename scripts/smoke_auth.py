#!/usr/bin/env python3
import os
import sys
import json
import urllib.request

def main():
    base_url = os.environ.get('RENDER_URL', 'https://dunes.onrender.com')
    url = base_url.rstrip('/') + '/auth/smoke'
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print('Auth smoke summary:', json.dumps(data, indent=2))
            if data.get('status') != 'ok' or data.get('players_fail') or data.get('clubs_fail'):
                print('Auth smoke found failures.')
                sys.exit(1)
    except Exception as e:
        print('Auth smoke error:', e)
        sys.exit(2)

if __name__ == '__main__':
    main()
