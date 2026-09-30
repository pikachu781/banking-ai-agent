import { Component } from '@angular/core';

@Component({
  selector: 'app-fd',
  standalone: true,
  imports: [],
  templateUrl: './fd.html',
  styleUrl: './fd.css'
})
export class Fd {

  fd = {
    type: 'FIXED DEPOSIT',
    number: '•••• •••• 7821',
    principal: '₹1,00,000',
    interestRate: '7.00%',
    tenure: '24 Months',
    maturityAmount: '₹1,14,889',
    interestEarned: '₹14,889',
    startDate: '28 Sep 2026',
    maturityDate: '28 Sep 2028',
    status: 'Active'
  };

  summary = [
    {
      title: 'Principal Amount',
      value: '₹1,00,000',
      icon: 'bi-wallet2',
      className: 'blue'
    },
    {
      title: 'Interest Rate',
      value: '7.00%',
      icon: 'bi-percent',
      className: 'green'
    },
    {
      title: 'Interest Earned',
      value: '₹14,889',
      icon: 'bi-graph-up-arrow',
      className: 'purple'
    },
    {
      title: 'Maturity Amount',
      value: '₹1,14,889',
      icon: 'bi-cash-stack',
      className: 'orange'
    }
  ];

  details = [
    {
      label: 'Deposit Type',
      value: 'Regular Fixed Deposit',
      icon: 'bi-bank'
    },
    {
      label: 'Interest Payout',
      value: 'At Maturity',
      icon: 'bi-calendar-check'
    },
    {
      label: 'Tenure',
      value: '24 Months',
      icon: 'bi-clock'
    },
    {
      label: 'Compounding',
      value: 'Quarterly',
      icon: 'bi-arrow-repeat'
    },
    {
      label: 'Start Date',
      value: '28 Sep 2026',
      icon: 'bi-calendar-plus'
    },
    {
      label: 'Maturity Date',
      value: '28 Sep 2028',
      icon: 'bi-calendar-event'
    }
  ];

  actions = [
    {
      title: 'FD Details',
      subtitle: 'View complete details',
      icon: 'bi-file-earmark-text'
    },
    {
      title: 'FD Calculator',
      subtitle: 'Calculate returns',
      icon: 'bi-calculator'
    },
    {
      title: 'Renew FD',
      subtitle: 'Plan maturity renewal',
      icon: 'bi-arrow-repeat'
    },
    {
      title: 'Download Receipt',
      subtitle: 'Get FD certificate',
      icon: 'bi-download'
    }
  ];

  benefits = [
    'Guaranteed returns',
    'Flexible tenure options',
    'Quarterly compounding',
    'Secure investment'
  ];
}