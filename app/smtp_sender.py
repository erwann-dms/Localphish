from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
import smtplib
import yaml

smtp_bp = Blueprint('smtp', __name__, url_prefix='/smtp', template_folder='templates')

CONFIG_PATH = "config.yaml"

def load_smtp_config():
    with open(CONFIG_PATH, 'r') as f:
        cfg = yaml.safe_load(f)
    return cfg.get('smtp', {})

def save_smtp_config(smtp_config):
    with open(CONFIG_PATH, 'r') as f:
        cfg = yaml.safe_load(f)
    cfg['smtp'] = smtp_config
    with open(CONFIG_PATH, 'w') as f:
        yaml.safe_dump(cfg, f)

@smtp_bp.route('/', methods=['GET', 'POST'])
@login_required
def smtp_settings():
    smtp_config = load_smtp_config()
    if request.method == 'POST':
        smtp_config['server'] = request.form.get('server')
        smtp_config['port'] = int(request.form.get('port'))
        smtp_config['use_tls'] = request.form.get('use_tls') == 'on'
        smtp_config['username'] = request.form.get('username')
        smtp_config['password'] = request.form.get('password')
        save_smtp_config(smtp_config)
        flash('SMTP configuration saved.', 'success')
        return redirect(url_for('smtp.smtp_settings'))
    return render_template('smtp_settings.html', smtp=smtp_config)

def send_mail(to_addr, subject, body, smtp_cfg):
    message = f"""From: {smtp_cfg.get('username')}
To: {to_addr}
Subject: {subject}

{body}
"""
    try:
        if smtp_cfg.get('use_tls'):
            server = smtplib.SMTP(smtp_cfg.get('server'), smtp_cfg.get('port'))
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(smtp_cfg.get('server'), smtp_cfg.get('port'))
        server.login(smtp_cfg.get('username'), smtp_cfg.get('password'))
        server.sendmail(smtp_cfg.get('username'), to_addr, message)
        server.quit()
        return True
    except Exception as e:
        print(f"SMTP error: {e}")
        return False
