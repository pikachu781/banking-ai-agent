import { Component } from '@angular/core';

@Component({
  selector: 'app-loan-details',
  standalone: true,
  imports: [],
  templateUrl: './loan-details.html',
  styleUrl: './loan-details.css'
})
export class LoanDetails {

  loan = {
    type: 'PERSONAL LOAN',
    loanNumber: '•••• •••• 4521',
    status: 'Active',
    sanctionedAmount: '₹5,00,000',
    outstandingAmount: '₹5,00,000',
    interestRate: '9.00%',
    tenure: '60 Months',
    emi: '₹10,379',
    startDate: '28 Sep 2026',
    nextDueDate: '05 Oct 2026'
  };

  repayment = {
    principal: '₹5,00,000',
    interest: '₹1,22,740',
    totalPayable: '₹6,22,740',
    paidAmount: '₹0',
    remainingAmount: '₹6,22,740',
    progress: 0
  };

  schedule = [
    {
      month: 'October 2026',
      date: '05 Oct 2026',
      emi: '₹10,379',
      principal: '₹6,629',
      interest: '₹3,750',
      status: 'Upcoming'
    },
    {
      month: 'November 2026',
      date: '05 Nov 2026',
      emi: '₹10,379',
      principal: '₹6,679',
      interest: '₹3,700',
      status: 'Upcoming'
    },
    {
      month: 'December 2026',
      date: '05 Dec 2026',
      emi: '₹10,379',
      principal: '₹6,729',
      interest: '₹3,650',
      status: 'Upcoming'
    }
  ];

  details = [
    {
      label: 'Loan Type',
      value: 'Personal Loan',
      icon: 'bi-person-vcard'
    },
    {
      label: 'Interest Type',
      value: 'Fixed Rate',
      icon: 'bi-percent'
    },
    {
      label: 'Repayment Frequency',
      value: 'Monthly',
      icon: 'bi-calendar3'
    },
    {
      label: 'Tenure',
      value: '60 Months',
      icon: 'bi-clock'
    },
    {
      label: 'Processing Fee',
      value: '₹5,000',
      icon: 'bi-receipt'
    },
    {
      label: 'Loan Status',
      value: 'Active',
      icon: 'bi-check-circle'
    }
  ];

  actions = [
    {
      title: 'Pay EMI',
      subtitle: 'Make your payment',
      icon: 'bi-credit-card'
    },
    {
      title: 'EMI Calculator',
      subtitle: 'Calculate repayment',
      icon: 'bi-calculator'
    },
    {
      title: 'Download Statement',
      subtitle: 'Get loan statement',
      icon: 'bi-download'
    },
    {
      title: 'Contact Support',
      subtitle: 'Get assistance',
      icon: 'bi-headset'
    }
  ];
}