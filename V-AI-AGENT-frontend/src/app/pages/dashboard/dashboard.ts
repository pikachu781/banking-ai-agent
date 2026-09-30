import { Component } from '@angular/core';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [DecimalPipe],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class DashboardComponent {

  balance = 75000;

  recentTransactions = [
    {
      title: 'Salary Credit',
      date: 'Today, 10:30 AM',
      amount: '+ ₹35,000',
      type: 'credit',
      icon: 'bi-arrow-down-left'
    },
    {
      title: 'UPI Payment',
      date: 'Yesterday, 06:45 PM',
      amount: '- ₹500',
      type: 'debit',
      icon: 'bi-arrow-up-right'
    },
    {
      title: 'Electricity Bill',
      date: '24 Sep 2026',
      amount: '- ₹1,200',
      type: 'debit',
      icon: 'bi-lightning-charge'
    }
  ];

  quickActions = [
    {
      title: 'Send Money',
      subtitle: 'Transfer funds',
      icon: 'bi-send'
    },
    {
      title: 'Pay Bills',
      subtitle: 'Electricity & more',
      icon: 'bi-receipt'
    },
    {
      title: 'My Cards',
      subtitle: 'Manage cards',
      icon: 'bi-credit-card'
    },
    {
      title: 'Loans',
      subtitle: 'View loans',
      icon: 'bi-bank'
    }
  ];

}