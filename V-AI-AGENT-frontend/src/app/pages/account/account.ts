import { Component } from '@angular/core';

@Component({
  selector: 'app-account',
  standalone: true,
  imports: [],
  templateUrl: './account.html',
  styleUrl: './account.css'
})
export class AccountComponent {

  account = {
    name: 'Niranjana Barik',
    accountType: 'Savings Account',
    accountNumber: '•••• •••• 6789',
    balance: '₹75,000.00',
    branch: 'Bhubaneswar Main Branch',
    ifsc: 'DEMO0001234',
    accountSince: 'September 2023',
    status: 'Active'
  };

}