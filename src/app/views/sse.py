from flask import Blueprint, jsonify, request, Response

from app.pubsub.no_dependency import NoDepMessageAnnouncer

bp_sse = Blueprint('sse', __name__, url_prefix="/sse")

announcer = NoDepMessageAnnouncer()

@bp_sse.route("/<string:id>", methods=["GET", "POST"])
def sse(id):
    if request.method == "GET":
        listener = announcer.listen(channel=id)
        
        def stream():
            yield "retry: 0\n"
            
            for message in listener.messages_generator():
                if message:
                    yield message
        
        return Response(stream(), mimetype="text/event-stream")
    
    else:
        message = request.json.get("message")
        event = request.json.get("event")
        
        announcer.announce(data=message, channel=id, event=event)
        
        return jsonify({"message": "Ok"})
