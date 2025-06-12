from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from .models import Campaign, Credential
from . import db

campaigns_bp = Blueprint('campaigns', __name__, url_prefix='/campaigns', template_folder='templates')

@campaigns_bp.route('/')
@login_required
def dashboard():
    campaigns = Campaign.query.all()
    return render_template('campaigns.html', campaigns=campaigns)

@campaigns_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_campaign():
    if request.method == 'POST':
        name = request.form.get('name')
        template_html = request.form.get('template_html')
        if not name or not template_html:
            flash('Name and template HTML are required.', 'warning')
            return redirect(url_for('campaigns.new_campaign'))
        campaign = Campaign(name=name, template_html=template_html)
        db.session.add(campaign)
        db.session.commit()
        flash('Campaign created.', 'success')
        return redirect(url_for('campaigns.dashboard'))
    return render_template('campaign_form.html')

@campaigns_bp.route('/edit/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def edit_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if request.method == 'POST':
        campaign.name = request.form.get('name')
        campaign.template_html = request.form.get('template_html')
        db.session.commit()
        flash('Campaign updated.', 'success')
        return redirect(url_for('campaigns.dashboard'))
    return render_template('campaign_form.html', campaign=campaign)

@campaigns_bp.route('/delete/<int:campaign_id>', methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign deleted.', 'info')
    return redirect(url_for('campaigns.dashboard'))

@campaigns_bp.route('/toggle/<int:campaign_id>', methods=['POST'])
@login_required
def toggle_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.is_active = not campaign.is_active
    db.session.commit()
    flash(f"Campaign {'started' if campaign.is_active else 'stopped'}.", 'success')
    return redirect(url_for('campaigns.dashboard'))

@campaigns_bp.route('/credentials/<int:campaign_id>')
@login_required
def view_credentials(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    credentials = Credential.query.filter_by(campaign_id=campaign_id).order_by(Credential.timestamp.desc()).all()
    return render_template('credentials.html', campaign=campaign, credentials=credentials)
