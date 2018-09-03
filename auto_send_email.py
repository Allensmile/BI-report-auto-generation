import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class SenderEmail:

    def __init__(self):
        self.mail_msg = MIMEMultipart()

    def add_address(self, subject, from_addr, to_addrs):
        """
        Add email subject, sender email address, receiver email address
        :param subject: email subject
        :param from_addr: sender email address
        :param to_addrs: receiver email address
        :return:
        """
        self.mail_msg['Subject'] = subject
        self.mail_msg['From'] = from_addr
        if isinstance(to_addrs, str):
            self.mail_msg['To'] = to_addrs
        elif isinstance(to_addrs, (list, tuple)) and len(to_addrs) == 1:
            self.mail_msg['To'] = to_addrs[0]
        elif isinstance(to_addrs, (list, tuple)) and len(to_addrs) > 1:
            self.mail_msg['To'] = ','.join(to_addrs)
        else:
            raise TypeError('receiver address must be str or list or tuple')

        return self.mail_msg

    def add_email_content(self, msg):
        """
        Add email content
        :param msg: email content
        :return:
        """
        """
        Email content
        :param msg: content
        :return: 
        """
        text_plain = MIMEText(msg, 'plain', 'utf-8')
        self.mail_msg.attach(text_plain)
        return self.mail_msg

    def add_attach_image(self, image_path):
        """
        Add image attach
        :param image_path: image path
        :return:
        """
        send_image = open(image_path, 'rb').read()
        image = MIMEImage(send_image)
        image.add_header('Content-ID', '<image1>')
        image["Content-Disposition"] = 'attachment; filename="belle.jpg"'
        self.mail_msg.attach(image)
        return self.mail_msg

    def add_attach_html(self, html):
        """
        Add html attach
        :param html:
        :return:
        """
        # 构造html
        # 发送正文中的图片:由于包含未被许可的信息，网易邮箱定义为垃圾邮件，报554 DT:SPM ：<p><img src="cid:image1"></p>
        text_html = MIMEText(html, 'html', 'utf-8')
        text_html["Content-Disposition"] = 'attachment; filename="texthtml.html"'
        self.mail_msg.attach(text_html)
        return self.mail_msg

    def add_attach_text(self, text_path):
        """
        Add text attach
        :param text_path: text path
        :return:
        """
        sendfile = open(text_path, 'rb').read()
        text_att = MIMEText(sendfile, 'base64', 'utf-8')
        text_att["Content-Type"] = 'application/octet-stream'
        # 以下附件可以重命名成report.txt
        # text_att["Content-Disposition"] = 'attachment; filename="report.txt"'
        # 另一种实现方式
        text_att.add_header('Content-Disposition', 'attachment', filename='中文附件.txt')
        self.mail_msg.attach(text_att)
        return self.mail_msg

    def connect(self, smtp_addr, from_addr, password, to_addrs):
        """
        Build connnect
        :param smtp_addr: smtp address (eg. "smtp.163.com")
        :param from_addr: sender email address (eg. "xxx@163.com")
        :param password: sender email password (eg. "123456")
        :param to_addrs: receiver email address (eg. ["yyy@163.com"])
        :return:
        """
        s = smtplib.SMTP()
        try:
            s.connect(smtp_addr)  # 连接smtp服务器
            s.login(from_addr, password)  # 登录邮箱
            s.sendmail(from_addr, to_addrs, self.mail_msg.as_string())  # 发送邮件
            print('Email successfully sent!')
        except Exception:
            print("Error: unable to send email")
            print(traceback.format_exc())
        finally:
            s.quit()


def main():
    # 定义自己的邮件主题、发送人邮件地址、收件人邮件地址、邮件内容、附件html内容、
    # smtp地址、发送人邮箱密码，此处我将这些放在自己的配置文件config.py中
    from instance.config import subject, from_addr, to_addrs, msg, \
        html, smtp_addr, password

    auto_email = SenderEmail()

    auto_email.add_address(subject=subject, from_addr=from_addr,
                           to_addrs=to_addrs)

    auto_email.add_email_content(msg=msg)

    auto_email.add_attach_image('/home/tanyouwei/桌面/meinv.jpg')

    auto_email.add_attach_html(html)
    auto_email.add_attach_text('/home/tanyouwei/桌面/datingTestSet.txt')

    auto_email.connect(smtp_addr=smtp_addr,
                       from_addr=from_addr, to_addrs=to_addrs,
                       password=password)



if __name__ == '__main__':
    main()
