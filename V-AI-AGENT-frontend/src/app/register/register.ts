import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CyberBgComponent } from '../background/cyber-bg.component';
import {
  AuthService,
  RegisterRequest
} from '../services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
     CyberBgComponent
  ],
  templateUrl: './register.html',
  styleUrl: './register.css'
})
export class RegisterComponent {

  private authService = inject(AuthService);

  username = '';
  email = '';
  password = '';
  confirmPassword = '';

  loading = false;
  successMessage = '';
  errorMessage = '';

  register(): void {

    this.successMessage = '';
    this.errorMessage = '';

    if (!this.username.trim()) {
      this.errorMessage = 'Username is required.';
      return;
    }

    if (!this.email.trim()) {
      this.errorMessage = 'Email is required.';
      return;
    }

    if (!this.isValidEmail(this.email)) {
      this.errorMessage = 'Please enter a valid email.';
      return;
    }

    if (!this.password) {
      this.errorMessage = 'Password is required.';
      return;
    }

    if (this.password.length < 6) {
      this.errorMessage =
        'Password must be at least 6 characters.';
      return;
    }

    if (this.password !== this.confirmPassword) {
      this.errorMessage = 'Passwords do not match.';
      return;
    }

    const request: RegisterRequest = {
      username: this.username.trim(),
      email: this.email.trim(),
      password: this.password,
      confirmPassword: this.confirmPassword
    };

    this.loading = true;

    this.authService.register(request).subscribe({

      next: (response) => {

        console.log('Registration response:', response);

        this.successMessage =
          response.message ||
          'Registration successful. Please verify your email.';

        this.username = '';
        this.email = '';
        this.password = '';
        this.confirmPassword = '';

        this.loading = false;
      },

      error: (error) => {

        console.error('Registration error:', error);

        this.errorMessage =
          error?.error?.message ||
          'Registration failed. Please try again.';

        this.loading = false;
      }

    });
  }

  private isValidEmail(email: string): boolean {

    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}