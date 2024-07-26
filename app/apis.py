from datetime import datetime
from flask import jsonify, Blueprint, request, redirect, Response, render_template
from app.models import UserEvent, EmailSendRecord
from app.exts import db
from app.schemas import UserEventSchema
from app.enums import PlatformEnum
from app.services.track import track_service
from app.services.user import user_service

bp = Blueprint('tracking', __name__, url_prefix='/tracking')

# TODO 接口校验先不做


@bp.post('send')
def send_email():
    tracking_id = track_service.generate_tracking_id()
    instance = EmailSendRecord(
        user_id=1,
        email='abc@mail.com',
        tracking_id=tracking_id
    )
    db.session.add(instance)
    db.session.commit()
    data = {
        'open_event': f'http://127.0.0.1:9000/tracking/track?tracking_id={tracking_id}&event=open',
        'click_button_1_event': f'http://127.0.0.1:9000/tracking/track?tracking_id={tracking_id}&event=click_button_1',
        'click_button_2_event': f'http://127.0.0.1:9000/tracking/track?tracking_id={tracking_id}&event=click_button_2'
    }
    html_content = render_template('page.html', data=data)
    return html_content


@bp.get('track')
def track():
    ''' 收集用户行为数据
    '''
    event = request.args.get('event')
    tracking_id = request.args.get('tracking_id')
    target = request.args.get('target')
    platform = PlatformEnum.EMAIL.value if tracking_id else PlatformEnum.WEB.value
    repeated = False
    if platform == PlatformEnum.EMAIL.value:
        user_id = track_service.get_user_id_by_tracking_id(tracking_id)
        query = UserEvent.query.filter(
            UserEvent.platform == PlatformEnum.EMAIL.value,
            UserEvent.tracking_id == tracking_id,
            UserEvent.event == event
        ).exists()
        repeated = db.session.query(query).scalar()
    else:
        # TODO token先不处理了
        user_id = user_service.auth(token=None)
    user_event = UserEvent(
        user_id=user_id,
        event=event,
        platform=platform,
        tracking_id=tracking_id,
        repeated=repeated,
    )
    db.session.add(user_event)
    db.session.commit()
    if target:
        return redirect(target, code=302)
    else:
        return Response(None, mimetype='image/png')


@bp.get('tracks')
def tracks():
    ''' 用户行为数据列表
    '''
    records = UserEvent.query.all()
    items = UserEventSchema(many=True).dump(records)
    data = {
        'total': len(items),
        'items': items
    }
    return jsonify(data)


@bp.get('overview')
def overview():
    ''' 概览
        各渠道打开人次、按钮1点击数、按钮2点击数
        对于邮件事件，只统计第一次事件
    '''
    start_timestamp = request.args.get('start')
    end_timestamp = request.args.get('end')
    start = datetime.fromtimestamp(int(start_timestamp))
    end = datetime.fromtimestamp(int(end_timestamp))
    query = db.session.query(
        UserEvent.platform,
        db.func.count(db.case(((UserEvent.event == 'open', 1)))).label('open'),
        db.func.count(db.case(((UserEvent.event == 'click_button_1', 1)))).label('click_button_1'),
        db.func.count(db.case(((UserEvent.event == 'click_button_2', 1)))).label('click_button_2')
    ).filter(
        UserEvent.created_at >= start,
        UserEvent.created_at <= end,
        ~((UserEvent.platform == 'email') & (UserEvent.repeated == 1))
    ).group_by(UserEvent.platform).all()

    data = {
        'email': {
            'open': 0,
            'click_button_1': 0,
            'click_button_2': 0
        },
        'web': {
            'open': 0,
            'click_button_1': 0,
            'click_button_2': 0
        }
    }
    for item in query:
        data[item.platform] = {
            'open': item.open,
            'click_button_1': item.click_button_1,
            'click_button_2': item.click_button_2
        }
    return jsonify(data)
