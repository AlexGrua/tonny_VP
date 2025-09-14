// User types
export interface User {
  id: string;
  username: string;
  firstName: string;
  lastName?: string;
  language: 'en' | 'ru';
  theme: 'light' | 'dark';
}

// Plan types
export interface Plan {
  id: string;
  name: string;
  price: number;
  duration: number; // days
  features: string[];
  popular?: boolean;
}

// Transaction types
export interface Transaction {
  id: string;
  type: 'deposit' | 'purchase' | 'referral';
  amount: number;
  date: Date;
  description: string;
}

// Referral types
export interface ReferralData {
  referralId: string;
  referralLink: string;
  totalReferrals: number;
  totalEarned: number;
  availableForWithdraw: number;
  cooldownPeriod: number;
}

// App state types
export interface AppState {
  user: User | null;
  balance: number;
  currentPlan: Plan | null;
  vpnStatus: 'connected' | 'disconnected' | 'connecting';
  theme: 'light' | 'dark';
  language: 'en' | 'ru';
  referralData: ReferralData;
}

// Payment methods
export interface PaymentMethods {
  balance: boolean;
  telegramStars: boolean;
  usdt: boolean;
  ton: boolean;
  other: string[];
}
