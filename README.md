### 本项目使用python3 flask框架

### 数据库使用sqlite，已经初始化完成

### 启动服务：flask run --port 9000

### 实现了几个接口

1. 生成邮件内容接口 POST /tracking/send
2. 上报用户事件接口 GET /tracking/track?tracking_id=1111&event=click_button_1
3. 事件列表 GET /tracking/tracks
4. 概览 GET /tracking/overview

