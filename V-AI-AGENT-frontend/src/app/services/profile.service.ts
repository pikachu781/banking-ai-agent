import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

export interface ProfileResponse {
  id: number;
  username: string;
  email: string;
  emailVerified: boolean;
  role: string;
  createdAt: string;
}

export interface UpdateProfileRequest {
  username: string;
}

export interface ChangePasswordRequest {
  currentPassword: string;
  newPassword: string;
}

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  private http = inject(HttpClient);

  private apiUrl = `${environment.apiUrl}/api/profile`;

  // Get logged-in user's profile
  getProfile(): Observable<ProfileResponse> {
    return this.http.get<ProfileResponse>(this.apiUrl);
  }

  // Update username
  updateProfile(
    data: UpdateProfileRequest
  ): Observable<ProfileResponse> {

    return this.http.put<ProfileResponse>(
      this.apiUrl,
      data
    );
  }

  // Change password
  changePassword(
    data: ChangePasswordRequest
  ): Observable<any> {

    return this.http.put(
      `${this.apiUrl}/password`,
      data
    );
  }
}