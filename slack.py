#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import argparse
import urllib3

webhook_url=''

def main():
    # baseline = json.load(sys.stdin)
    sys.stderr.write('Error: %s\n' % sys.stdin)
    parser = argparse.ArgumentParser()
    parser.add_argument('-slack_token', dest='slack_token', type=str, help='Slack Token')
    args = parser.parse_args()
    webhook_url = 'https://hooks.slack.com/services/' + args.slack_token
   
    try:
        slack_notification(str(rdjson['diagnostics']), webhook_url)
    except Exception as error:
        sys.stderr.write('Error: %s\n' % error)
        return 1
    return 0

def slack_notification(message, webhook_url):
    try:
        slack_message = {'text': message}

        http = urllib3.PoolManager()
        response = http.request('POST',
                                webhook_url,
                                body = json.dumps(slack_message),
                                headers = {'Content-Type': 'application/json'},
                                retries = False)
    except Exception as error:
         sys.stderr.write('Error: %s\n' % webhook_url)

    return True

if __name__ == '__main__':
    sys.exit(main())
