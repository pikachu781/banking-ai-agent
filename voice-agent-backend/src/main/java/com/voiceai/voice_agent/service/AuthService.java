package com.voiceai.voice_agent.service;


import com.voiceai.voice_agent.dto.LoginRequest;
import com.voiceai.voice_agent.dto.LoginResponse;
import com.voiceai.voice_agent.dto.RegisterRequest;
import com.voiceai.voice_agent.dto.RegisterResponse;
import com.voiceai.voice_agent.entity.User;
import com.voiceai.voice_agent.entity.VerificationToken;
import com.voiceai.voice_agent.exception.BadRequestException;
import com.voiceai.voice_agent.repository.UserRepository;
import com.voiceai.voice_agent.repository.VerificationTokenRepository;
import com.voiceai.voice_agent.exception.GlobalExceptionHandler;

import lombok.RequiredArgsConstructor;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final VerificationTokenRepository verificationTokenRepository;
    private final PasswordEncoder passwordEncoder;
    private final EmailService emailService;

    private final JwtService jwtService;
    public RegisterResponse register(RegisterRequest request) {

        // 1. Check password confirmation
        if (!request.getPassword().equals(request.getConfirmPassword())) {
            throw new RuntimeException("Passwords do not match");
        }

        // 2. Check username
        if (userRepository.existsByUsername(request.getUsername())) {
            throw new RuntimeException("Username already exists");
        }

        // 3. Check email
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new RuntimeException("Email already registered");
        }

        // 4. Create user
        User user = User.builder()
                .username(request.getUsername())
                .email(request.getEmail())
                .password(passwordEncoder.encode(request.getPassword()))
                .emailVerified(false)
                .role("USER")
                .createdAt(LocalDateTime.now())
                .build();

        // 5. Save user
        User savedUser = userRepository.save(user);

        // 6. Generate verification token
        String token = UUID.randomUUID().toString();

        VerificationToken verificationToken =
                VerificationToken.builder()
                        .token(token)
                        .user(savedUser)
                        .expiryDate(LocalDateTime.now().plusHours(24))
                        .build();

        verificationTokenRepository.save(verificationToken);

        // 7. Send verification email
        emailService.sendVerificationEmail(
                savedUser.getEmail(),
                savedUser.getUsername(),
                token
        );

        // 8. Return response
        return RegisterResponse.builder()
                .message("Registration successful. Please verify your email.")
                .userId(savedUser.getId())
                .email(savedUser.getEmail())
                .build();
    }

    public String verifyEmail(String token) {

        VerificationToken verificationToken =
                verificationTokenRepository.findByToken(token)
                        .orElseThrow(() ->
                                new RuntimeException("Invalid verification token"));

        // Check expiry
        if (verificationToken.getExpiryDate().isBefore(LocalDateTime.now())) {

            verificationTokenRepository.delete(verificationToken);

            return "Verification token has expired";
        }

        User user = verificationToken.getUser();

        user.setEmailVerified(true);

        userRepository.save(user);

        // Token should not be reused
        verificationTokenRepository.delete(verificationToken);

        return "Email verified successfully";
    }
    public LoginResponse login(LoginRequest request) {

        User user = userRepository.findByEmail(request.getEmail())
                .orElse(null);

        // Email does not exist
        if (user == null) {
            throw new BadRequestException("Your email is incorrect");
        }

        // Email exists but is not verified
        if (!user.isEmailVerified()) {
            throw new BadRequestException(
                    "Please verify your email before login"
            );
        }

        // Check password
        boolean passwordMatches =
                passwordEncoder.matches(
                        request.getPassword(),
                        user.getPassword()
                );

        if (!passwordMatches) {
            throw new BadRequestException(
                    "Your password is incorrect"
            );
        }

        String token = jwtService.generateToken(user);

        return LoginResponse.builder()
                .message("Login successful")
                .token(token)
                .userId(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .role(user.getRole())
                .build();
    }
}