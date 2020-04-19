package com.tongji.etl.util;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.PropertySource;
import org.springframework.stereotype.Component;

import javax.mail.*;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import java.io.UnsupportedEncodingException;
import java.util.Date;
import java.util.Properties;

/**
 * @author: guangxush
 * @create: 2020/04/17
 */
@Component
@PropertySource("classpath:config/mail.properties")
public class MailSend {

    @Value("${mail.protocol}")
    private String protovol;

    @Value("${mail.host}")
    private String host;

    @Value("$mail.from")
    private String from;

    @Value("${mail.port}")
    private String port;

    @Value("${mail.name}")
    private String name;

    @Value("${mail.password}")
    private String password;

    @Value("${mail.to}")
    private String to;

    @Value("${mail.subject}")
    private String subject;

    /**
     * send email to monitor the kafka data
     * @param content
     * @return
     */
    public boolean sendmail(String content){

        Properties props = new Properties();
        props.put("mail.transport.protocol", protovol);
        props.put("mail.host", host);
        props.put("mail.from", from);
        props.put("mail.smtp.auth", true);
        Authentication authentication = new Authentication(name, password);

        if (true) {
            props.put("mail.smtp.starttls.enable", "true");
            props.put("mail.smtp.socketFactory.fallback", "false");
            props.put("mail.smtp.socketFactory.port", port);
        }

        Session session = Session.getDefaultInstance(props,authentication);
        session.setDebug(true);
        try {
            Transport transport = session.getTransport();
            transport.connect(name, password);
            Address toAddress = new InternetAddress(to);
            MimeMessage message = new MimeMessage(session);
            String nick="";
            try {
                nick=javax.mail.internet.MimeUtility.encodeText("我的昵称");
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
            message.setFrom(new InternetAddress(nick+" <"+name+">"));
            message.setSubject(subject);
            message.addRecipient(Message.RecipientType.TO, toAddress);
            message.setContent(content, "text/html;charset=utf-8");
            message.setSentDate(new Date());
            transport.sendMessage(message, InternetAddress.parse(to));
            return true;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return false;
    }

    class Authentication extends Authenticator {

        private String username=null;
        private String password=null;

        public Authentication(String username, String password) {
            this.username = username;
            this.password = password;
        }

        /**
         * using password authentication
         * @return
         */
        @Override
        protected PasswordAuthentication getPasswordAuthentication(){
            PasswordAuthentication pa = new PasswordAuthentication(username, password);
            return pa;
        }
    }
}
