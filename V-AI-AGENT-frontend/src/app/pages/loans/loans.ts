import { Component } from '@angular/core';

@Component({
  selector: 'app-loans',
  standalone: true,
  imports: [],
  templateUrl: './loans.html',
  styleUrl: './loans.css'
})
export class LoansComponent {

  loan = {
    type: 'PERSONAL LOAN',
    loanNumber: '•••• •••• 4521',
    sanctioned: '₹5,00,000',
    outstanding: '₹5,00,000',
    interestRate: '9.00%',
    tenure: '60 Months',
    emi: '₹10,379',
    status: 'Active'
  };

  loanProgress = {
    paid: '₹0',
    remaining: '₹5,00,000',
    percentage: 0
  };

  actions = [
    {
      title: 'Loan Details',
      subtitle: 'View complete details',
      icon: 'bi-file-earmark-text'
    },
    {
      title: 'Pay EMI',
      subtitle: 'Make your payment',
      icon: 'bi-credit-card'
    },
    {
      title: 'EMI Calculator',
      subtitle: 'Calculate your EMI',
      icon: 'bi-calculator'
    },
    {
      title: 'Download Statement',
      subtitle: 'Get loan statement',
      icon: 'bi-download'
    }
  ];

  payments = [
    {
      title: 'Upcoming EMI',
      date: '05 Oct 2026',
      amount: '₹10,379',
      status: 'Upcoming',
      icon: 'bi-calendar-event'
    },
    {
      title: 'Loan Disbursement',
      date: '28 Sep 2026',
      amount: '₹5,00,000',
      status: 'Completed',
      icon: 'bi-check-circle'
    }
  ];

  loanTypes = [
    {
      title: 'Personal Loan',
      description: 'Flexible funds for your personal needs.',
      rate: 'From 9.00%',
      icon: 'bi-person'
    },
    {
      title: 'Home Loan',
      description: 'Finance your dream home with flexible terms.',
      rate: 'From 8.50%',
      icon: 'bi-house'
    },
    {
      title: 'Education Loan',
      description: 'Support your higher education journey.',
      rate: 'From 8.25%',
      icon: 'bi-mortarboard'
    }
  ];
}