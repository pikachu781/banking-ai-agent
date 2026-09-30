import { Component } from '@angular/core';

@Component({
  selector: 'app-fd-details',
  standalone: true,
  imports: [],
  templateUrl: './fd-details.html',
  styleUrl: './fd-details.css'
})
export class FdDetails {

  fd = {
    type: 'REGULAR FIXED DEPOSIT',
    number: '•••• •••• 7821',
    status: 'Active',
    principal: '₹1,00,000',
    interestRate: '7.00%',
    tenure: '24 Months',
    maturityAmount: '₹1,14,889',
    interestEarned: '₹14,889',
    startDate: '28 Sep 2026',
    maturityDate: '28 Sep 2028',
    payout: 'At Maturity',
    compounding: 'Quarterly'
  };

  timeline = [
    {
      title: 'FD Created',
      date: '28 Sep 2026',
      description: 'Fixed deposit account opened successfully.',
      status: 'completed',
      icon: 'bi-check-circle'
    },
    {
      title: 'Investment Active',
      date: '28 Sep 2026',
      description: 'Your principal amount is earning interest.',
      status: 'active',
      icon: 'bi-graph-up-arrow'
    },
    {
      title: 'Maturity',
      date: '28 Sep 2028',
      description: 'Principal and interest become payable.',
      status: 'upcoming',
      icon: 'bi-calendar-check'
    }
  ];

  breakdown = [
    {
      label: 'Principal Amount',
      value: '₹1,00,000',
      percentage: 87.0
    },
    {
      label: 'Interest Earned',
      value: '₹14,889',
      percentage: 13.0
    }
  ];

  actions = [
    {
      title: 'Renew FD',
      subtitle: 'Continue your investment',
      icon: 'bi-arrow-repeat'
    },
    {
      title: 'Download Receipt',
      subtitle: 'Get deposit certificate',
      icon: 'bi-download'
    },
    {
      title: 'FD Calculator',
      subtitle: 'Calculate returns',
      icon: 'bi-calculator'
    },
    {
      title: 'Contact Support',
      subtitle: 'Get assistance',
      icon: 'bi-headset'
    }
  ];
}