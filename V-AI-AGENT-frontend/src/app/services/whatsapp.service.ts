import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from './../environments/environment';

export interface WhatsappContact {

  id: number;

  name: string;

  phoneNumber: string;

  optedIn: boolean;

  createdAt: string;
}

export interface AddContactRequest {

  name: string;

  phoneNumber: string;

  optedIn: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class WhatsappContactService {

  private apiUrl =
    `${environment.apiUrl}/api/whatsapp/contacts`;

  constructor(
    private http: HttpClient
  ) {}

  // ADD CONTACT

  addContact(
    data: AddContactRequest
  ): Observable<WhatsappContact> {

    return this.http.post<WhatsappContact>(
      this.apiUrl,
      data
    );
  }

  // GET CONTACTS

  getContacts(): Observable<WhatsappContact[]> {

    return this.http.get<WhatsappContact[]>(
      this.apiUrl
    );
  }

  // DELETE CONTACT

  deleteContact(
    id: number
  ): Observable<void> {

    return this.http.delete<void>(
      `${this.apiUrl}/${id}`
    );
  }
}