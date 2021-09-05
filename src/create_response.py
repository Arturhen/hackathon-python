from flask import  Response, json

def create_response(status, name_content, content, message=False):
    body = {}
    body[name_content] = content

    if(message):
        body[message] = message
    
    return Response(json.dumps(body), status=status, mimetype="application/json")
