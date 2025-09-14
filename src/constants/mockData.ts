import { User, Plan, Transaction, ReferralData } from '../types';

// Mock user data
export const mockUser: User = {
  id: '1',
  username: 'alexgrua',
  firstName: 'Alex',
  lastName: 'Grua',
  language: 'en',
  theme: 'light'
};

// Mock plans
export const mockPlans: Plan[] = [
  {
    id: '1',
    name: 'Basic',
    price: 5.99,
    duration: 30,
    features: [
      'Unlimited bandwidth',
      '5 server locations',
      'Basic support',
      'No logs policy'
    ]
  },
  {
    id: '2',
    name: 'Pro',
    price: 9.99,
    duration: 30,
    features: [
      'Unlimited bandwidth',
      '15 server locations',
      'Priority support',
      'No logs policy',
      'Kill switch',
      'Ad blocker'
    ],
    popular: true
  },
  {
    id: '3',
    name: 'Premium',
    price: 14.99,
    duration: 30,
    features: [
      'Unlimited bandwidth',
      '50+ server locations',
      '24/7 premium support',
      'No logs policy',
      'Kill switch',
      'Ad blocker',
      'Dedicated IP',
      'Split tunneling'
    ]
  }
];

// Mock transactions
export const mockTransactions: Transaction[] = [
  {
    id: '1',
    type: 'deposit',
    amount: 50,
    date: new Date('2024-01-15'),
    description: 'Deposit via Telegram Stars'
  },
  {
    id: '2',
    type: 'purchase',
    amount: -9.99,
    date: new Date('2024-01-10'),
    description: 'Pro Plan subscription'
  },
  {
    id: '3',
    type: 'referral',
    amount: 2.50,
    date: new Date('2024-01-05'),
    description: 'Referral bonus from user123'
  }
];

// Mock referral data
export const mockReferralData: ReferralData = {
  referralId: 'REF123456',
  referralLink: 'https://t.me/duna_vpn_bot?start=ref123456',
  totalReferrals: 12,
  totalEarned: 25.50,
  availableForWithdraw: 15.00,
  cooldownPeriod: 7
};
