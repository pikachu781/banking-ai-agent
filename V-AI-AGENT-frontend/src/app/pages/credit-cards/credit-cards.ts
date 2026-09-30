import { Component } from '@angular/core';

@Component({
  selector: 'app-credit-cards',
  standalone: true,
  imports: [],
  templateUrl: './credit-cards.html',
  styleUrl: './credit-cards.css'
})
export class CreditCardsComponent {

  creditCard = {
    type: 'PLATINUM CREDIT',
    number: '•••• •••• •••• 8842',
    holder: 'NIRANJANA BARIK',
    expiry: '11/30',
    availableLimit: '₹1,81,250',
    totalLimit: '₹2,00,000',
    used: '₹18,750'
  };

  benefits = [
    {
      icon: 'bi-percent',
      title: 'Reward Points',
      value: '2,450',
      description: 'Available points'
    },
    {
      icon: 'bi-cash-coin',
      title: 'Cashback',
      value: '₹1,240',
      description: 'Earned this year'
    },
    {
      icon: 'bi-airplane',
      title: 'Travel Benefits',
      value: '12',
      description: 'Partner offers'
    }
  ];

  transactions = [
    {
      merchant: 'Amazon',
      category: 'Shopping',
      date: '27 Sep 2026',
      amount: '₹2,000',
      icon: 'bi-bag'
    },
    {
      merchant: 'Swiggy',
      category: 'Food & Dining',
      date: '26 Sep 2026',
      amount: '₹640',
      icon: 'bi-cup-hot'
    },
    {
      merchant: 'Uber',
      category: 'Transport',
      date: '24 Sep 2026',
      amount: '₹380',
      icon: 'bi-car-front'
    }
  ];

  actions = [
    {
      title: 'Pay Credit Card',
      subtitle: 'Make a payment',
      icon: 'bi-wallet2'
    },
    {
      title: 'View Statement',
      subtitle: 'Download statement',
      icon: 'bi-file-earmark-text'
    },
    {
      title: 'Reward Points',
      subtitle: 'Redeem rewards',
      icon: 'bi-stars'
    },
    {
      title: 'Card Settings',
      subtitle: 'Manage card',
      icon: 'bi-sliders'
    }
  ];
}