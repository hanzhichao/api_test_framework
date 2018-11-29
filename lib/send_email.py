import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import sys
sys.path.append('..')
from config.config import *


def send_email(report_file):
    msg = MIMEMultipart()
    msg.attach(MIMEText(open(report_file, encoding='utf-8').read(), 'html', 'utf-8'))

    msg['From'] = 'test_results@sina.com'
    msg['To'] = '2375247815@qq.com'
    msg['Subject'] = Header(subject, 'utf-8')  # 从配置文件中读取

    att1 = MIMEText(open(report_file, 'rb').read(), 'base64', 'utf-8')  # 从配置文件中读取
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="{}"'.format(os.path.basename(report_file))  # 参数化一下report_file
    msg.attach(att1)

    try:
        smtp = smtplib.SMTP_SSL(smtp_server)  # 从配置文件中读取
        smtp.login(smtp_user, smtp_password)  # 从配置文件中读取
        smtp.sendmail(sender, receiver, msg.as_string())
        logging.info("邮件发送完成！")
    except Exception as e:
        logging.error(str(e))
    finally:
        smtp.quit()

