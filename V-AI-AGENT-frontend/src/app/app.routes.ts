import { Routes } from '@angular/router';

import { authGuard } from './guards/auth.guard';

export const routes: Routes = [

  {
    path: 'login',
    loadComponent: () =>
      import('./login/login')
        .then(m => m.LoginComponent)
  },

  {
    path: 'register',
    loadComponent: () =>
      import('./register/register')
        .then(m => m.RegisterComponent)
  },

  {
    path: 'chat',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./chat/chat')
        .then(m => m.ChatComponent)
  },

  {
  path: 'profile',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./profile/profile')
      .then(m => m.ProfileComponent)
},

  {
    path: 'whatsapp/contacts',
    loadComponent: () =>
      import('./whatsapp/contacts/contacts')
        .then(m => m.ContactsComponent)
  },

  // ================================
  // DASHBOARD
  // ================================
  {
    path: 'dashboard',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./pages/dashboard/dashboard')
        .then(m => m.DashboardComponent)
  },
 {
  path: 'account',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./pages/account/account')
      .then(m => m.AccountComponent)

    },

    {
  path: 'transactions',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./pages/transactions/transactions')
      .then(m => m.TransactionsComponent)
  },
    {
  path: 'cards',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./pages/cards/cards')
      .then(m => m.CardsComponent)
},
    {
  path: 'credit-cards',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./pages/credit-cards/credit-cards')
      .then(m => m.CreditCardsComponent)
},
    {
  path: 'loans',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./pages/loans/loans')
      .then(m => m.LoansComponent)
},
    {
  path: 'loans/details',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./pages/loan-details/loan-details')
      .then(m => m.LoanDetails)
},

{
  path: 'fd',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./pages/fd/fd')
      .then(m => m.Fd)
},

{
  path: 'fd/details',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./pages/fd-details/fd-details')
      .then(m => m.FdDetails)
},

{
  path: 'emi-calculator',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./pages/emi-calculator/emi-calculator')
      .then(m => m.EmiCalculator)
},

{
  path: 'kyc',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./pages/kyc/kyc')
      .then(m => m.Kyc)
},
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },

  {
    path: '**',
    redirectTo: 'login'
  }

];