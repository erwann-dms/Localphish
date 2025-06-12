from flask import Blueprint, request, Response, abort
from flask_login import login_required, current_user
from .models import Campaign
import requests

proxy_bp = Blueprint('proxy', __name__, url_prefix='/proxy')

@proxy_bp.route('/<int:campaign_id>/<path:path>', methods=['GET', 'POST'])
def proxy_request(campaign_id, path):
    campaign = Campaign.query.get(campaign_id)
    if not campaign or not campaign.is_active:
        abort(404)
    
    # For demonstration, proxy to localhost on port 8081 (could be changed)
    target_url = f"http://127.0.0.1:8081/{path}"
    
    if request.method == 'POST':
        resp = requests.post(target_url, data=request.form, headers=request.headers)
    else:
        resp = requests.get(target_url, headers=request.headers, params=request.args)
    
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]
    
    response = Response(resp.content, resp.status_code, headers)
    return response
