import { Component } from '@angular/core';

@Component({
  selector: 'app-kyc',
  standalone: true,
  imports: [],
  templateUrl: './kyc.html',
  styleUrl: './kyc.css'
})
export class Kyc {

  kycStatus = {
    status: 'Verified',
    verifiedOn: '15 Sep 2026',
    nextReview: '15 Sep 2028'
  };

  personalInfo = {
    name: 'Niranjana Barik',
    dateOfBirth: '12 May 2005',
    mobile: '+91 98******42',
    email: 'niranjana@example.com',
    address: 'Bhubaneswar, Odisha'
  };

  documents = [
    {
      title: 'Aadhaar Card',
      number: 'XXXX XXXX 7821',
      type: 'Identity Proof',
      status: 'Verified',
      icon: 'bi-person-vcard',
      date: '15 Sep 2026'
    },
    {
      title: 'PAN Card',
      number: 'ABCDE****F',
      type: 'Tax Identity',
      status: 'Verified',
      icon: 'bi-credit-card-2-front',
      date: '15 Sep 2026'
    },
    {
      title: 'Address Proof',
      number: 'Verified Address',
      type: 'Address Verification',
      status: 'Verified',
      icon: 'bi-house-check',
      date: '15 Sep 2026'
    },
    {
      title: 'Photograph',
      number: 'Profile Photo',
      type: 'Identity Verification',
      status: 'Verified',
      icon: 'bi-camera',
      date: '15 Sep 2026'
    }
  ];

  timeline = [
    {
      title: 'KYC Verification Completed',
      description: 'Your identity documents were successfully verified.',
      date: '15 Sep 2026',
      icon: 'bi-check-circle-fill',
      completed: true
    },
    {
      title: 'Documents Submitted',
      description: 'Identity and address documents were submitted.',
      date: '14 Sep 2026',
      icon: 'bi-file-earmark-check',
      completed: true
    },
    {
      title: 'Profile Verification',
      description: 'Personal information was verified successfully.',
      date: '14 Sep 2026',
      icon: 'bi-person-check',
      completed: true
    }
  ];

  securityItems = [
    {
      title: 'Identity Protected',
      description: 'Your KYC information is securely stored.',
      icon: 'bi-shield-lock'
    },
    {
      title: 'Encrypted Documents',
      description: 'Uploaded documents are protected with encryption.',
      icon: 'bi-lock'
    },
    {
      title: 'Privacy Controlled',
      description: 'Your information is only used for banking services.',
      icon: 'bi-eye-slash'
    }
  ];
}