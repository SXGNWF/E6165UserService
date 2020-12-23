from __future__ import print_function

import boto3
import json
from urllib.request import Request, urlopen, URLError, HTTPError
import requests

import utilities.context as ctx


class sns_slack():

    def __init__(self):
        _connect_info = ctx.get_connect_info()
        self.sns = boto3.client("sns",
                                region_name=_connect_info["region_name"],
                                aws_access_key_id=_connect_info["aws_access_key_id"],
                                aws_secret_access_key=_connect_info["aws_secret_access_key"])
        self.topics = dict()
        self.topic_arn_list = []
        self.HOOK_URL = "https://hooks.slack.com/services/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"
        # self.HOOK_URL = "https://hooks.slack.com/services/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"

    def create_topic(self, topic):
        response = self.sns.create_topic(Name=topic)
        topic_arn = response["TopicArn"]
        self.topics[topic] = topic_arn

    def publish_to_topic(self, topic, message, subject):
        self.sns.publish(TopicArn=self.topics[topic],
                         Message=message,
                         Subject=subject)

    def list_topics(self):
        response = self.sns.list_topics()
        topics = response["Topics"]
        return topics

    def delete_topics(self, topic):
        self.sns.delete_topic(TopicArn=self.topics[topic])
        del self.topics[topic]

    def send_to_slack(self, message):

        slack_message = {
            'channel': 'project',
            # 'channel': "Arya Zhao, Lalitha, Phyllis Li, Tanmay Chopra",
            'text': message,
            'username': 'TaoLi',
            'icon_emoji': ':tophat:'
        }

        response = requests.post(
            self.HOOK_URL, data=json.dumps(slack_message),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
#
#
# def lambda_handler(event, context):
#     logger.info("Event: " + str(event))
#
#     state_dict = {"Ok": ":thumbsup:", "Info": ":information_source:", "Severe": ":exclamation:"}
#
#     d = dict(line.split(": ") for line in event['Records'][0]['Sns']["Message"].splitlines() if ": " in line)
#
#     transition = re.match('Environment health has transitioned from (.*) to (.*?)\.', d['Message'])
#     if transition:
#         original, became = map(lambda x: state_dict.get(x, x), transition.groups())
#         d["Message"] = "*Health*: " + original + u" ⟶ " + became + "\n_" + d["Message"].split(". ", 1)[1] + "_"
#
#     slack_message = {
#         'channel': 'build' if "New application version was deployed" in d["Message"] else 'beanstalk',
#         'text': d["Message"],
#         'username': d["Environment"],
#         'icon_emoji': ':tophat:'
#     }
#
#     req = Request(HOOK_URL, json.dumps(slack_message))
#
#     try:
#         response = urlopen(req)
#         response.read()
#         logger.info("Message posted to %s", slack_message['channel'])
#     except HTTPError as e:
#         logger.error("Request failed: %d %s", e.code, e.reason)
#     except URLError as e:
#         logger.error("Server connection failed: %s", e.reason)
