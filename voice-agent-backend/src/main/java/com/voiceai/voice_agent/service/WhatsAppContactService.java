package com.voiceai.voice_agent.service;


import com.voiceai.voice_agent.entity.WhatsAppContact;
import com.voiceai.voice_agent.repository.WhatsAppContactRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class WhatsAppContactService {

    private final WhatsAppContactRepository contactRepository;

    // =========================
    // ADD CONTACT
    // =========================
    public WhatsAppContact addContact(WhatsAppContact contact) {

        // Prevent duplicate phone number for the same user
        boolean exists = contactRepository.existsByUserIdAndPhoneNumber(
                contact.getUserId(),
                contact.getPhoneNumber()
        );

        if (exists) {
            throw new RuntimeException(
                    "This WhatsApp number already exists"
            );
        }

        // Default opted-in value
        if (contact.getOptedIn() == null) {
            contact.setOptedIn(false);
        }

        return contactRepository.save(contact);
    }

    // =========================
    // GET ALL CONTACTS OF USER
    // =========================
    public List<WhatsAppContact> getContactsByUser(Long userId) {

        return contactRepository.findByUserId(userId);
    }

    // =========================
    // GET CONTACT BY ID
    // =========================
    public WhatsAppContact getContactById(Long id) {

        return contactRepository.findById(id)
                .orElseThrow(() ->
                        new RuntimeException("WhatsApp contact not found")
                );
    }

    // =========================
    // UPDATE CONTACT
    // =========================
    public WhatsAppContact updateContact(
            Long id,
            WhatsAppContact updatedContact
    ) {

        WhatsAppContact existingContact =
                contactRepository.findById(id)
                        .orElseThrow(() ->
                                new RuntimeException(
                                        "WhatsApp contact not found"
                                )
                        );

        existingContact.setName(updatedContact.getName());
        existingContact.setPhoneNumber(updatedContact.getPhoneNumber());
        existingContact.setOptedIn(updatedContact.getOptedIn());

        return contactRepository.save(existingContact);
    }

    // =========================
    // DELETE CONTACT
    // =========================
    public void deleteContact(Long id) {

        WhatsAppContact contact =
                contactRepository.findById(id)
                        .orElseThrow(() ->
                                new RuntimeException(
                                        "WhatsApp contact not found"
                                )
                        );

        contactRepository.delete(contact);
    }
}