package com.voiceai.voice_agent.controller;


import com.voiceai.voice_agent.entity.WhatsAppContact;
import com.voiceai.voice_agent.service.WhatsAppContactService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/whatsapp/contacts")
@RequiredArgsConstructor
public class WhatsAppContactController {

    private final WhatsAppContactService contactService;

    // =========================
    // ADD CONTACT
    // =========================
    @PostMapping
    public ResponseEntity<WhatsAppContact> addContact(
            @RequestBody WhatsAppContact contact
    ) {

        WhatsAppContact savedContact =
                contactService.addContact(contact);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(savedContact);
    }

    // =========================
    // GET ALL CONTACTS
    // =========================
    @GetMapping("/user/{userId}")
    public ResponseEntity<List<WhatsAppContact>> getContacts(
            @PathVariable Long userId
    ) {

        List<WhatsAppContact> contacts =
                contactService.getContactsByUser(userId);

        return ResponseEntity.ok(contacts);
    }

    // =========================
    // GET CONTACT BY ID
    // =========================
    @GetMapping("/{id}")
    public ResponseEntity<WhatsAppContact> getContact(
            @PathVariable Long id
    ) {

        WhatsAppContact contact =
                contactService.getContactById(id);

        return ResponseEntity.ok(contact);
    }

    // =========================
    // UPDATE CONTACT
    // =========================
    @PutMapping("/{id}")
    public ResponseEntity<WhatsAppContact> updateContact(
            @PathVariable Long id,
            @RequestBody WhatsAppContact contact
    ) {

        WhatsAppContact updatedContact =
                contactService.updateContact(id, contact);

        return ResponseEntity.ok(updatedContact);
    }

    // =========================
    // DELETE CONTACT
    // =========================
    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteContact(
            @PathVariable Long id
    ) {

        contactService.deleteContact(id);

        return ResponseEntity.ok(
                "WhatsApp contact deleted successfully"
        );
    }
}