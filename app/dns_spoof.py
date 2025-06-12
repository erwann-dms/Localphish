from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
import threading
from dnslib import DNSRecord, RR, QTYPE, A, DNSHeader
import socketserver

dns_spoof_bp = Blueprint('dns_spoof', __name__, url_prefix='/dns_spoof', template_folder='templates')

# Global variables for DNS spoofing
spoof_enabled = False
spoof_domains = {}
dns_thread = None

class DNSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, socket = self.request
        request = DNSRecord.parse(data)
        reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
        
        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]
        
        # Remove trailing dot
        qname = qname.rstrip('.')
        
        if spoof_enabled and qname in spoof_domains:
            ip = spoof_domains[qname]
            reply.add_answer(RR(qname, getattr(QTYPE, qtype), rdata=A(ip), ttl=60))
        else:
            # No spoof, return no answers
            pass
        
        socket.sendto(reply.pack(), self.client_address)

def dns_server():
    server = socketserver.UDPServer(('0.0.0.0', 53), DNSHandler)
    server.serve_forever()

@dns_spoof_bp.route('/', methods=['GET', 'POST'])
@login_required
def manage_spoof():
    global spoof_enabled, spoof_domains, dns_thread
    if request.method == 'POST':
        enabled = request.form.get('enabled') == 'on'
        domains_raw = request.form.get('domains', '')
        ip = request.form.get('ip', '127.0.0.1')
        
        domains = [d.strip().lower() for d in domains_raw.split(',') if d.strip()]
        
        spoof_enabled = enabled
        spoof_domains = {d: ip for d in domains}
        
        if spoof_enabled and dns_thread is None:
            dns_thread = threading.Thread(target=dns_server, daemon=True)
            dns_thread.start()
        
        flash(f"DNS Spoofing {'enabled' if spoof_enabled else 'disabled'} for domains: {', '.join(spoof_domains)}", 'success')
        return redirect(url_for('dns_spoof.manage_spoof'))
    
    return render_template('dns_spoof.html', enabled=spoof_enabled, domains=','.join(spoof_domains.keys()), ip=spoof_domains.get(next(iter(spoof_domains), ''), '127.0.0.1'))
