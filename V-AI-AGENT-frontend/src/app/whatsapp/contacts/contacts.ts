import { CommonModule, DatePipe } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

import {
  WhatsappContactService,
  WhatsappContact
} from '../../services/whatsapp.service';

@Component({
  selector: 'app-contacts',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    DatePipe
  ],
  templateUrl: './contacts.html',
  styleUrl: './contacts.css'
})
export class ContactsComponent implements OnInit {

  // =========================
  // FORM DATA
  // =========================

  name = '';
  phoneNumber = '';
  optedIn = true;

  // =========================
  // UI STATE
  // =========================

  loading = false;
  successMessage = '';
  errorMessage = '';

  // =========================
  // CONTACT LIST
  // =========================

  contacts: WhatsappContact[] = [];

  constructor(
    private whatsappContactService: WhatsappContactService
  ) {}

  // =========================
  // INIT
  // =========================

  ngOnInit(): void {
    this.loadContacts();
  }

  // =========================
  // ADD CONTACT
  // =========================

  saveContact(): void {

    this.successMessage = '';
    this.errorMessage = '';

    if (!this.name.trim()) {
      this.errorMessage = 'Name is required';
      return;
    }

    if (!this.phoneNumber.trim()) {
      this.errorMessage = 'Phone number is required';
      return;
    }

    this.loading = true;

    const request = {
      name: this.name.trim(),
      phoneNumber: this.phoneNumber.trim(),
      optedIn: this.optedIn
    };

    this.whatsappContactService.addContact(request).subscribe({

      next: (response) => {

        console.log('Contact saved:', response);

        this.successMessage = 'Contact added successfully';

        // Clear form
        this.name = '';
        this.phoneNumber = '';
        this.optedIn = true;

        this.loading = false;

        // Reload contacts
        this.loadContacts();
      },

      error: (error) => {

        console.error('Add contact error:', error);

        this.errorMessage =
          error?.error?.message ||
          'Failed to add contact';

        this.loading = false;
      }

    });
  }

  // =========================
  // LOAD CONTACTS
  // =========================

  loadContacts(): void {

    this.loading = true;

    this.whatsappContactService.getContacts().subscribe({

      next: (response) => {

        console.log('Contacts:', response);

        this.contacts = response;

        this.loading = false;
      },

      error: (error) => {

        console.error('Load contacts error:', error);

        this.errorMessage =
          error?.error?.message ||
          'Failed to load contacts';

        this.loading = false;
      }

    });
  }

  // =========================
  // DELETE CONTACT
  // =========================

  deleteContact(id: number): void {

    if (!confirm('Are you sure you want to delete this contact?')) {
      return;
    }

    this.whatsappContactService.deleteContact(id).subscribe({

      next: () => {

        this.successMessage = 'Contact deleted successfully';

        this.loadContacts();
      },

      error: (error) => {

        console.error('Delete contact error:', error);

        this.errorMessage =
          error?.error?.message ||
          'Failed to delete contact';
      }

    });
  }
}