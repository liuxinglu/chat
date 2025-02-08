from flask import Blueprint, render_template, request, flash, session, jsonify

pageops_bp = Blueprint('pageops', __name__)



@pageops_bp.route('/userKeyword', methods=['GET'])
def getKeywordPage():
    return render_template('domain1.html')


@pageops_bp.route('/getBankPage', methods=['GET'])
def getBankPage():
    return render_template('bank.html')


@pageops_bp.route('/servicedeskops_TicketCreation', methods=['GET'])
def getChatPage():
    return render_template('ticket.html')


@pageops_bp.route('/selectModel', methods=['POST'])
def selectModel():
    data = request.get_json()
    selected_model = data.get('model')
    session["selected_model"] = selected_model
    return jsonify({'model': session['selected_model']}), 200

@pageops_bp.route('/getModel', methods=['GET'])
def getModel():
    return jsonify({'model': session['selected_model']}), 200


@pageops_bp.route('/domain', methods=['GET'])
def fileops():
    return jsonify({"menu":[{"id":"userKeyword", "content":'关键字提取'}]}), 200

@pageops_bp.route('/servicedesk', methods=['GET'])
def servicedeskops():
    return jsonify({"menu":[{"id":"servicedeskops_TicketCreation", "content":'ITSM Ticket Creation'}]}), 200

@pageops_bp.route('/security', methods=['GET'])
def securityops():
    return jsonify({"menu":[{"id":"securityops", "content":'#'}]}), 200

@pageops_bp.route('/cloud', methods=['GET'])
def cloudops():
    return jsonify({"menu":[{"id":"cloudops", "content":'#'}]}), 200


@pageops_bp.route('/chatops', methods=['GET'])
def chatops():
    return jsonify({"menu":[{"id":"userChat", "content":'自由对话'}]}), 200

