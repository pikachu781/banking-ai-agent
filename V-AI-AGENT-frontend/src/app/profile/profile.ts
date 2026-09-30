import {
  Component,
  OnInit,
  inject,
  ChangeDetectorRef
} from '@angular/core';

import { CommonModule } from '@angular/common';

import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';

import { HttpErrorResponse } from '@angular/common/http';

import {
  ProfileService,
  ProfileResponse
} from '../services/profile.service';


@Component({
  selector: 'app-profile',
  standalone: true,

  imports: [
    CommonModule,
    ReactiveFormsModule
  ],

  templateUrl: './profile.html',
  styleUrl: './profile.css'
})


export class ProfileComponent implements OnInit {

  // =========================
  // SERVICES
  // =========================

  private fb = inject(FormBuilder);

  private profileService = inject(ProfileService);

  // IMPORTANT:
  // Used to manually refresh Angular UI
  private cdr = inject(ChangeDetectorRef);


  // =========================
  // PROFILE DATA
  // =========================

  profile: ProfileResponse | null = null;


  // =========================
  // PASSWORD VISIBILITY
  // =========================

  showCurrentPassword = false;

  showNewPassword = false;


  // =========================
  // LOADING STATES
  // =========================

  loading = true;

  updating = false;

  changingPassword = false;


  // =========================
  // MESSAGES
  // =========================

  errorMessage = '';

  successMessage = '';


  // =========================
  // FORMS
  // =========================

  profileForm: FormGroup;

  passwordForm: FormGroup;


  // =========================
  // CONSTRUCTOR
  // =========================

  constructor() {

    // PROFILE FORM

    this.profileForm = this.fb.group({

      username: [
        '',
        [
          Validators.required,
          Validators.minLength(3),
          Validators.maxLength(50)
        ]
      ]

    });


    // PASSWORD FORM

    this.passwordForm = this.fb.group({

      currentPassword: [
        '',
        [
          Validators.required
        ]
      ],

      newPassword: [
        '',
        [
          Validators.required,
          Validators.minLength(6)
        ]
      ]

    });

  }


  // =========================
  // INIT
  // =========================

  ngOnInit(): void {

    this.loadProfile();

  }


  // =========================
  // LOAD PROFILE
  // =========================

  loadProfile(): void {

    this.loading = true;

    this.errorMessage = '';

    this.successMessage = '';


    console.log('Calling Profile API...');


    this.profileService
      .getProfile()
      .subscribe({

        next: (response) => {

          console.log(
            'Profile Response:',
            response
          );


          // Store profile

          this.profile = response;


          // Set username in form

          this.profileForm.patchValue({

            username: response.username

          });


          // Stop loading

          this.loading = false;


          // IMPORTANT
          // Force Angular to update UI

          this.cdr.detectChanges();


          console.log(
            'Profile loaded successfully'
          );

        },


        error: (error: HttpErrorResponse) => {

          console.error(
            'Profile error:',
            error
          );


          this.loading = false;


          this.errorMessage =
            error.error?.message ||
            'Unable to load profile.';


          // Force UI update

          this.cdr.detectChanges();

        }

      });

  }


  // =========================
  // UPDATE PROFILE
  // =========================

  updateProfile(): void {

    if (this.profileForm.invalid) {

      this.profileForm.markAllAsTouched();

      return;

    }


    this.updating = true;

    this.errorMessage = '';

    this.successMessage = '';


    this.profileService

      .updateProfile(
        this.profileForm.value
      )

      .subscribe({

        next: (response) => {

          console.log(
            'Updated profile:',
            response
          );


          // Update profile data

          this.profile = response;


          // Stop loading

          this.updating = false;


          // Success message

          this.successMessage =
            'Profile updated successfully.';


          // IMPORTANT

          this.cdr.detectChanges();

        },


        error: (error: HttpErrorResponse) => {

          console.error(
            'Update profile error:',
            error
          );


          this.updating = false;


          this.errorMessage =
            error.error?.message ||
            'Unable to update profile.';


          // IMPORTANT

          this.cdr.detectChanges();

        }

      });

  }


  // =========================
  // CHANGE PASSWORD
  // =========================

  changePassword(): void {

    if (this.passwordForm.invalid) {

      this.passwordForm.markAllAsTouched();

      return;

    }


    this.changingPassword = true;

    this.errorMessage = '';

    this.successMessage = '';


    this.profileService

      .changePassword(
        this.passwordForm.value
      )

      .subscribe({

        next: () => {

          console.log(
            'Password changed successfully'
          );


          // Stop loading

          this.changingPassword = false;


          // Clear password fields

          this.passwordForm.reset();


          // Hide passwords again

          this.showCurrentPassword = false;

          this.showNewPassword = false;


          // Success message

          this.successMessage =
            'Password changed successfully.';


          // IMPORTANT

          this.cdr.detectChanges();

        },


        error: (error: HttpErrorResponse) => {

          console.error(
            'Change password error:',
            error
          );


          this.changingPassword = false;


          this.errorMessage =
            error.error?.message ||
            'Unable to change password.';


          // IMPORTANT

          this.cdr.detectChanges();

        }

      });

  }

}