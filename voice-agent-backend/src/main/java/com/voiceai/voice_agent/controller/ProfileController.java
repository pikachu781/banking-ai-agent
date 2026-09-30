package com.voiceai.voice_agent.controller;

import com.voiceai.voice_agent.dto.ChangePasswordRequest;
import com.voiceai.voice_agent.dto.ProfileResponse;
import com.voiceai.voice_agent.dto.UpdateProfileRequest;
import com.voiceai.voice_agent.service.JwtService;
import com.voiceai.voice_agent.service.ProfileService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/profile")
@RequiredArgsConstructor
public class ProfileController {

    private final ProfileService profileService;
    private final JwtService jwtService;

    // =========================
    // GET PROFILE
    // =========================

    @GetMapping
    public ResponseEntity<ProfileResponse> getProfile(
            HttpServletRequest request) {

        Long userId = getUserIdFromToken(request);

        ProfileResponse profile =
                profileService.getProfile(userId);

        return ResponseEntity.ok(profile);
    }

    // =========================
    // UPDATE PROFILE
    // =========================

    @PutMapping
    public ResponseEntity<ProfileResponse> updateProfile(
            HttpServletRequest request,
            @Valid @RequestBody UpdateProfileRequest updateRequest) {

        Long userId = getUserIdFromToken(request);

        ProfileResponse profile =
                profileService.updateProfile(
                        userId,
                        updateRequest
                );

        return ResponseEntity.ok(profile);
    }

    // =========================
    // CHANGE PASSWORD
    // =========================

    @PutMapping("/password")
    public ResponseEntity<?> changePassword(
            HttpServletRequest request,
            @Valid @RequestBody ChangePasswordRequest passwordRequest) {

        Long userId = getUserIdFromToken(request);

        profileService.changePassword(
                userId,
                passwordRequest
        );

        return ResponseEntity.ok(
                Map.of(
                        "success", true,
                        "message", "Password changed successfully"
                )
        );
    }

    // =========================
    // GET USER ID FROM JWT
    // =========================

    private Long getUserIdFromToken(
            HttpServletRequest request) {

        String header =
                request.getHeader("Authorization");

        if (header == null || !header.startsWith("Bearer ")) {

            throw new RuntimeException(
                    "Authorization token is missing"
            );
        }

        String token =
                header.substring(7);

        if (!jwtService.isTokenValid(token)) {

            throw new RuntimeException(
                    "Invalid or expired token"
            );
        }

        return jwtService.extractUserId(token);
    }
}