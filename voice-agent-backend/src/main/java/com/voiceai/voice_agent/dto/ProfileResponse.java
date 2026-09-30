package com.voiceai.voice_agent.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;

@Getter
@Builder
@AllArgsConstructor
public class ProfileResponse {

    private Long id;
    private String username;
    private String email;
    private boolean emailVerified;
    private String role;
    private LocalDateTime createdAt;
}