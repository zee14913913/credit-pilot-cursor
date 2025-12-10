# email_service.py
# CreditPilot - 邮件发送服务

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import date
from typing import Optional
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()


def send_reminder_email(
    recipient_email: str,
    excel_file_path: str,
    reminder_data: dict,
    smtp_server: str = None,
    smtp_port: int = None,
    sender_email: str = None,
    sender_password: str = None
) -> bool:
    """
    发送提醒邮件（带Excel附件）
    
    Args:
        recipient_email: 收件人邮箱
        excel_file_path: Excel文件路径
        reminder_data: 提醒数据
        smtp_server: SMTP服务器（默认Gmail）
        smtp_port: SMTP端口（默认587）
        sender_email: 发件人邮箱
        sender_password: 发件人密码（Gmail需要使用应用专用密码）
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # 从环境变量获取配置
        smtp_server = smtp_server or os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = smtp_port or int(os.getenv('SMTP_PORT', '587'))
        sender_email = sender_email or os.getenv('SENDER_EMAIL', '')
        sender_password = sender_password or os.getenv('SENDER_PASSWORD', '')
        
        if not sender_email or not sender_password:
            print("⚠️ 邮件配置未设置，请配置环境变量：")
            print("  - SENDER_EMAIL: 发件人邮箱")
            print("  - SENDER_PASSWORD: 发件人密码（Gmail使用应用专用密码）")
            return False
        
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"CreditPilot 每日提醒 - {date.today().strftime('%Y年%m月%d日')}"
        
        # 邮件正文
        body = generate_email_body(reminder_data)
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 添加Excel附件
        if os.path.exists(excel_file_path):
            with open(excel_file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {Path(excel_file_path).name}'
            )
            msg.attach(part)
        
        # 发送邮件
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启用TLS加密
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"✓ 邮件已成功发送到: {recipient_email}")
        return True
        
    except Exception as e:
        print(f"✗ 邮件发送失败: {str(e)}")
        return False


def generate_email_body(reminder_data: dict) -> str:
    """生成邮件正文内容"""
    today = date.today()
    
    body = f"""
============================================================
📋 CreditPilot 每日到期提醒
============================================================

生成时间: {today.strftime('%Y年%m月%d日 %H:%M')}

"""
    
    if reminder_data['tomorrow_count'] > 0:
        body += f"明天到期 ({reminder_data['tomorrow_count']} 笔):\n\n"
        for i, stmt in enumerate(reminder_data['tomorrow'], 1):
            body += f"{i}️⃣ {stmt['client_name']} - {stmt.get('bank_name', '')} *{stmt.get('card_number', '')}\n"
            body += f"   💰 GZ代付: RM {stmt['gz_payment']:.2f} {stmt['gz_status']}\n"
            body += f"   💰 Owner付款: RM {stmt['owner_payment']:.2f} {stmt['owner_status']}\n"
            body += f"   📎 单据: {stmt['doc_status']}\n\n"
    
    if reminder_data['day_after_count'] > 0:
        body += f"后天到期 ({reminder_data['day_after_count']} 笔):\n\n"
        for i, stmt in enumerate(reminder_data['day_after'], 1):
            body += f"{i}️⃣ {stmt['client_name']} - {stmt.get('bank_name', '')} *{stmt.get('card_number', '')}\n"
            body += f"   💰 GZ代付: RM {stmt['gz_payment']:.2f} {stmt['gz_status']}\n"
            body += f"   💰 Owner付款: RM {stmt['owner_payment']:.2f} {stmt['owner_status']}\n"
            body += f"   📎 单据: {stmt['doc_status']}\n\n"
    
    body += "-" * 60 + "\n"
    body += f"总计需代付 (GZ): RM {reminder_data['total_gz_payment']:.2f}\n"
    body += f"总计需客户付 (Owner): RM {reminder_data['total_owner_payment']:.2f}\n"
    body += f"合计: RM {reminder_data['total_gz_payment'] + reminder_data['total_owner_payment']:.2f}\n\n"
    
    if reminder_data.get('most_urgent_client') and reminder_data['most_urgent_client']:
        urgent = reminder_data['most_urgent_client']
        body += f"🔴 最紧急: {urgent.get('client_name', '')} (RM {urgent.get('total_amount', 0):.2f})\n"
        if urgent.get('reasons'):
            body += f"   原因: {' | '.join(urgent['reasons'])}\n"
    
    body += "\n" + "=" * 60 + "\n"
    body += "\n详细数据请查看附件Excel文件。\n"
    body += "\n此邮件由CreditPilot系统自动发送。\n"
    
    return body
