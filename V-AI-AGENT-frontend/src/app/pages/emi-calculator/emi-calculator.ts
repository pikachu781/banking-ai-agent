import { Component } from '@angular/core';
import { DecimalPipe } from '@angular/common';
 
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-emi-calculator',
  standalone: true,
  imports: [DecimalPipe, FormsModule],
  templateUrl: './emi-calculator.html',
  styleUrl: './emi-calculator.css'
})
export class EmiCalculator {

  loanAmount = 500000;
  interestRate = 9;
  tenure = 60;

  get monthlyEMI(): number {
    const principal = this.loanAmount;
    const monthlyRate = this.interestRate / 12 / 100;
    const months = this.tenure;

    if (monthlyRate === 0) {
      return principal / months;
    }

    const emi =
      principal *
      monthlyRate *
      Math.pow(1 + monthlyRate, months) /
      (Math.pow(1 + monthlyRate, months) - 1);

    return emi;
  }

  get totalPayment(): number {
    return this.monthlyEMI * this.tenure;
  }

  get totalInterest(): number {
    return this.totalPayment - this.loanAmount;
  }

  get principalPercentage(): number {
    return (this.loanAmount / this.totalPayment) * 100;
  }

  get interestPercentage(): number {
    return (this.totalInterest / this.totalPayment) * 100;
  }

  calculate() {
    // Values are calculated automatically through getters.
  }

  reset() {
    this.loanAmount = 500000;
    this.interestRate = 9;
    this.tenure = 60;
  }
}