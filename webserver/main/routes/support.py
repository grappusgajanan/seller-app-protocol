from flask import g
from flask_expects_json import expects_json
from flask_restx import Namespace, Resource, reqparse
from jsonschema import validate

from main import constant
from main.repository.ack_response import get_ack_response
from main.service import send_message_to_queue_for_given_request
from main.service.common import dump_request_payload
from main.utils.schema_utils import get_json_schema_for_given_path, get_json_schema_for_response

support_namespace = Namespace('support', description='Support Namespace')


@support_namespace.route("/v1/support")
class SupportOrder(Resource):
    path_schema = get_json_schema_for_given_path('/support')

    @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response('/support')
        resp = get_ack_response(ack=True)
        payload = g.data
        dump_request_payload(payload, "support")
        message = {
            "request_type": "support",
            "message_ids": {
                "support": payload[constant.CONTEXT]["message_id"]
            }
        }
        send_message_to_queue_for_given_request(message)
        validate(resp, response_schema)
        return resp
