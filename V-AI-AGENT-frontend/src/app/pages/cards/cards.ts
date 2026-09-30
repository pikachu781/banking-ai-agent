import { Component } from '@angular/core';

@Component({
  selector: 'app-cards',
  standalone: true,
  imports: [],
  templateUrl: './cards.html',
  styleUrl: './cards.css'
})
export class CardsComponent {

  card = {
    type: 'DEBIT CARD',
    number: '•••• •••• •••• 1234',
    holder: 'NIRANJANA BARIK',
    expiry: '09/29',
    status: 'Active',
    network: 'VISA'
  };

  cardStats = {
    monthlyLimit: 100000,
    used: 18750,
    available: 81250
  };

  activities = [
    {
      title: 'Online Shopping',
      merchant: 'Amazon',
      date: '27 Sep 2026',
      amount: '- ₹2,000',
      icon: 'bi-bag'
    },
    {
      title: 'UPI Payment',
      merchant: 'Google Pay',
      date: '25 Sep 2026',
      amount: '- ₹500',
      icon: 'bi-phone'
    },
    {
      title: 'Electricity Bill',
      merchant: 'BESCOM',
      date: '24 Sep 2026',
      amount: '- ₹1,200',
      icon: 'bi-lightning-charge'
    }
  ];

  cardActions = [
    {
      title: 'Freeze Card',
      subtitle: 'Temporarily block',
      icon: 'bi-snow'
    },
    {
      title: 'Card Details',
      subtitle: 'View information',
      icon: 'bi-eye'
    },
    {
      title: 'Card Settings',
      subtitle: 'Manage controls',
      icon: 'bi-sliders'
    },
    {
      title: 'Set Limit',
      subtitle: 'Control spending',
      icon: 'bi-speedometer2'
    }
  ];
}