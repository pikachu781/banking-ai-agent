import { Component } from '@angular/core';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-transactions',
  standalone: true,
  imports: [DecimalPipe],
  templateUrl: './transactions.html',
  styleUrl: './transactions.css'
})
export class TransactionsComponent {

  selectedFilter = 'All';

  filters = [
    'All',
    'Income',
    'Expenses'
  ];

  transactions = [
    {
      title: 'Salary Credit',
      description: 'Monthly Salary',
      date: '28 Sep 2026',
      time: '10:30 AM',
      amount: 35000,
      type: 'credit',
      category: 'Income',
      icon: 'bi-arrow-down-left'
    },
    {
      title: 'UPI Payment',
      description: 'UPI Transfer',
      date: '27 Sep 2026',
      time: '06:45 PM',
      amount: 500,
      type: 'debit',
      category: 'Shopping',
      icon: 'bi-phone'
    },
    {
      title: 'Electricity Bill',
      description: 'Electricity Payment',
      date: '24 Sep 2026',
      time: '09:20 AM',
      amount: 1200,
      type: 'debit',
      category: 'Bills',
      icon: 'bi-lightning-charge'
    },
    {
      title: 'Online Shopping',
      description: 'Shopping Payment',
      date: '22 Sep 2026',
      time: '08:12 PM',
      amount: 2000,
      type: 'debit',
      category: 'Shopping',
      icon: 'bi-bag'
    },
    {
      title: 'Cash Deposit',
      description: 'Branch Cash Deposit',
      date: '20 Sep 2026',
      time: '02:15 PM',
      amount: 5000,
      type: 'credit',
      category: 'Income',
      icon: 'bi-cash-stack'
    }
  ];

  get filteredTransactions() {

    if (this.selectedFilter === 'All') {
      return this.transactions;
    }

    if (this.selectedFilter === 'Income') {
      return this.transactions.filter(
        transaction => transaction.type === 'credit'
      );
    }

    return this.transactions.filter(
      transaction => transaction.type === 'debit'
    );
  }

  selectFilter(filter: string) {
    this.selectedFilter = filter;
  }

}