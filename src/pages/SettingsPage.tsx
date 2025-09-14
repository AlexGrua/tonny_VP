import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { mockUser } from '../constants/mockData';

const SettingsPage: React.FC = () => {
  const navigate = useNavigate();
  const [language, setLanguage] = useState<'en' | 'ru'>(mockUser.language);
  const [theme, setTheme] = useState<'light' | 'dark'>(mockUser.theme);

  const settingsItems = [
    {
      id: 'balance',
      title: 'Balance & Transactions',
      description: 'View your balance and transaction history',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
        </svg>
      ),
      onClick: () => navigate('/balance')
    },
    {
      id: 'referral',
      title: 'Referral Program',
      description: 'Invite friends and earn rewards',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
        </svg>
      ),
      onClick: () => navigate('/referral')
    },
    {
      id: 'how-to-use',
      title: 'How to Use',
      description: 'Learn how to set up and use VPN',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      onClick: () => navigate('/how-to-use')
    },
    {
      id: 'about',
      title: 'About Us',
      description: 'Learn more about Duna VPN',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      onClick: () => navigate('/about-us')
    },
    {
      id: 'contact',
      title: 'Contact Us',
      description: 'Get help and support',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      ),
      onClick: () => navigate('/contact-us')
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="px-4 py-6">
          <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
          <p className="text-gray-600">Manage your account and preferences</p>
        </div>
      </div>

      <div className="px-4 py-6 space-y-6">
        {/* User Profile */}
        <Card>
          <div className="flex items-center space-x-4">
            <div className="w-16 h-16 bg-primary-500 rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-xl">
                {mockUser.firstName[0]}
              </span>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                {mockUser.firstName} {mockUser.lastName}
              </h3>
              <p className="text-gray-600">@{mockUser.username}</p>
            </div>
          </div>
        </Card>

        {/* Language Switch */}
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Language</h3>
              <p className="text-gray-600">Choose your preferred language</p>
            </div>
            <div className="flex space-x-2">
              <Button
                variant={language === 'en' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setLanguage('en')}
              >
                EN
              </Button>
              <Button
                variant={language === 'ru' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setLanguage('ru')}
              >
                RU
              </Button>
            </div>
          </div>
        </Card>

        {/* Theme Switch */}
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Theme</h3>
              <p className="text-gray-600">Choose your preferred theme</p>
            </div>
            <div className="flex space-x-2">
              <Button
                variant={theme === 'light' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setTheme('light')}
              >
                Light
              </Button>
              <Button
                variant={theme === 'dark' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setTheme('dark')}
              >
                Dark
              </Button>
            </div>
          </div>
        </Card>

        {/* Settings Menu */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-900">Account & Support</h2>
          
          {settingsItems.map((item) => (
            <Card
              key={item.id}
              className="cursor-pointer hover:shadow-md transition-shadow duration-200"
              onClick={item.onClick}
            >
              <div className="flex items-center space-x-4">
                <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center text-primary-500">
                  {item.icon}
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900">{item.title}</h3>
                  <p className="text-sm text-gray-600">{item.description}</p>
                </div>
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </Card>
          ))}
        </div>

        {/* Legal Links */}
        <div className="space-y-2">
          <h2 className="text-xl font-semibold text-gray-900">Legal</h2>
          <div className="space-y-2">
            <button
              onClick={() => navigate('/privacy-policy')}
              className="w-full text-left text-primary-500 hover:text-primary-600 py-2"
            >
              Privacy Policy
            </button>
            <button
              onClick={() => navigate('/terms-of-use')}
              className="w-full text-left text-primary-500 hover:text-primary-600 py-2"
            >
              Terms of Use
            </button>
            <button
              onClick={() => navigate('/refund-policy')}
              className="w-full text-left text-primary-500 hover:text-primary-600 py-2"
            >
              Refund Policy
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
