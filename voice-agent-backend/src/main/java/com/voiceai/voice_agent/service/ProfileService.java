package com.voiceai.voice_agent.service;

import com.voiceai.voice_agent.dto.ChangePasswordRequest;
import com.voiceai.voice_agent.dto.ProfileResponse;
import com.voiceai.voice_agent.dto.UpdateProfileRequest;
import com.voiceai.voice_agent.entity.User;
import com.voiceai.voice_agent.exception.BadRequestException;
import com.voiceai.voice_agent.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ProfileService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    // =========================
    // GET PROFILE
    // =========================

    public ProfileResponse getProfile(Long userId) {

        User user = userRepository.findById(userId)
                .orElseThrow(() ->
                        new BadRequestException("User not found")
                );

        return mapToProfileResponse(user);
    }

    // =========================
    // UPDATE PROFILE
    // =========================

    public ProfileResponse updateProfile(
            Long userId,
            UpdateProfileRequest request) {

        User user = userRepository.findById(userId)
                .orElseThrow(() ->
                        new BadRequestException("User not found")
                );

        // Check username only if it is being changed
        if (!user.getUsername().equals(request.getUsername())
                && userRepository.existsByUsername(request.getUsername())) {

            throw new BadRequestException(
                    "Username is already taken"
            );
        }

        user.setUsername(request.getUsername());

        User updatedUser = userRepository.save(user);

        return mapToProfileResponse(updatedUser);
    }

    // =========================
    // CHANGE PASSWORD
    // =========================

    public void changePassword(
            Long userId,
            ChangePasswordRequest request) {

        User user = userRepository.findById(userId)
                .orElseThrow(() ->
                        new BadRequestException("User not found")
                );

        // Check current password
        boolean currentPasswordMatches =
                passwordEncoder.matches(
                        request.getCurrentPassword(),
                        user.getPassword()
                );

        if (!currentPasswordMatches) {
            throw new BadRequestException(
                    "Current password is incorrect"
            );
        }

        // Prevent same password
        if (passwordEncoder.matches(
                request.getNewPassword(),
                user.getPassword())) {

            throw new BadRequestException(
                    "New password must be different from current password"
            );
        }

        // Encode new password
        user.setPassword(
                passwordEncoder.encode(
                        request.getNewPassword()
                )
        );

        userRepository.save(user);
    }

    // =========================
    // MAP USER → PROFILE
    // =========================

    private ProfileResponse mapToProfileResponse(User user) {

        return ProfileResponse.builder()
                .id(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .emailVerified(user.isEmailVerified())
                .role(user.getRole())
                .createdAt(user.getCreatedAt())
                .build();
    }
}