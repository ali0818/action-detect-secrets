#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import argparse

webhook_url=''

rdjson = {
    'source': {
        'name': 'detect-secrets',
        'url': 'https://github.com/Yelp/detect-secrets'
    },
    'severity': 'ERROR',
    'diagnostics': []
}


def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_known_args()
    print(args)
    webhook_url = 'https://hooks.slack.com/services/' + args.slack_token
    print(webhook_url)

    baseline = json.load(sys.stdin)
    if not baseline['results']:
        baseline['results'] = {}

    results = {}
    for detects in baseline['results'].values():
        for item in detects:
            key = '%s:%s' % (item['filename'], item['line_number'])
            if key in results:
                results[key]['message'] += '\n* ' + item['type']
            else:
                results[key] = {
                    'message': '\n* ' + item['type'],
                    'location': {
                        'path': item['filename'],
                        'range': {
                            'start': {
                                'line': item['line_number']
                            }
                        }
                    }
                }

    for result in results.values():
        rdjson['diagnostics'].append(result)

    try:
        sys.stdout.write(json.dumps(rdjson, indent=2, ensure_ascii=False))
        slack_notification(str(rdjson))
        sys.stdout.write('\n')
    except Exception as error:
        sys.stderr.write('Error: %s\n' % error)
        return 1
    return 0

def slack_notification(message):
    try:
        slack_message = {'text': message}

        http = urllib3.PoolManager()
        response = http.request('POST',
                                webhook_url,
                                body = json.dumps(slack_message),
                                headers = {'Content-Type': 'application/json'},
                                retries = False)
    except:
        traceback.print_exc()

    return True

if __name__ == '__main__':
    sys.exit(main())
