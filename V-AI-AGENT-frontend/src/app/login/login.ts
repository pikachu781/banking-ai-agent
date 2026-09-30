import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';  
@Component({
  selector: 'app-login',
  standalone: true,
   
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class LoginComponent {

  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);

  loginForm: FormGroup;

  loading = false;
  errorMessage = '';

  constructor() {

    this.loginForm = this.fb.group({

      email: [
        '',
        [
          Validators.required,
          Validators.email
        ]
      ],

      password: [
        '',
        [
          Validators.required,
          Validators.minLength(6)
        ]
      ]

    });

  }
login(): void {

  if (this.loginForm.invalid) {
    this.loginForm.markAllAsTouched();
    return;
  }

  this.loading = true;
  this.errorMessage = '';

  this.authService.login(this.loginForm.value).subscribe({

    next: (response) => {

      console.log('Login successful:', response);

      this.authService.saveLogin(response);

      this.loading = false;

      this.router.navigate(['/chat']);
    },
error: (error: HttpErrorResponse) => {

  console.log('BEFORE:', this.errorMessage);

  this.loading = false;

  this.errorMessage =
    error.error?.message ||
    'Something went wrong. Please try again.';

  console.log('AFTER:', this.errorMessage);

  setTimeout(() => {
    console.log('AFTER 1 SECOND:', this.errorMessage);
  }, 1000);
}
  });
}
}