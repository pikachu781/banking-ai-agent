package com.voiceai.voice_agent.service;

import lombok.RequiredArgsConstructor;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class EmailService {

    private final JavaMailSender mailSender;

    public void sendVerificationEmail(String email, String username, String token) {

        String verificationLink =
                "http://localhost:8080/api/auth/verify?token=" + token;

        SimpleMailMessage message = new SimpleMailMessage();

        message.setTo(email);
        message.setSubject("Verify your Voice AI Agent account");

        message.setText(
                "Hello " + username + ",\n\n" +

                        "Thank you for registering with Voice AI Agent.\n\n" +

                        "Please click the link below to verify your email:\n\n" +

                        verificationLink + "\n\n" +

                        "This verification link will expire in 24 hours.\n\n" +

                        "Regards,\n" +
                        "Voice AI Agent Team"
        );

        mailSender.send(message);
    }
}