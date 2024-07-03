from flask import Blueprint, jsonify, request

from app.pubsub.no_dependency import NoDepMessageAnnouncer

bp_sse = Blueprint('sse', __name__, url_prefix="/sse")

announcer = NoDepMessageAnnouncer()

@bp_sse.route("/<string:id>", methods=["GET", "POST"])
def sse(id):
    if request.method == "GET":
        listener = announcer.listen(channel=id)
        
        return listener.messages_generator(), {"Context-Type": "text/event-stream"}
    
    else:
        message = request.json.get("message")
        event = request.json.get("event")
        
        announcer.announce(data=message, channel=id, event=event)
        
        return jsonify({"message": "Ok"})
