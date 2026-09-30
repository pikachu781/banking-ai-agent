package com.voiceai.voice_agent.repository;


import com.voiceai.voice_agent.entity.WhatsAppContact;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface WhatsAppContactRepository
        extends JpaRepository<WhatsAppContact, Long> {

    // Get all WhatsApp contacts belonging to a user
    List<WhatsAppContact> findByUserId(Long userId);

    // Find a specific contact by user and phone number
    Optional<WhatsAppContact> findByUserIdAndPhoneNumber(
            Long userId,
            String phoneNumber
    );

    // Check whether a phone number already exists for a user
    boolean existsByUserIdAndPhoneNumber(
            Long userId,
            String phoneNumber
    );
}