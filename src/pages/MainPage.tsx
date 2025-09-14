import React from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { mockUser, mockReferralData } from '../constants/mockData';

const MainPage: React.FC = () => {
  const navigate = useNavigate();

  // Mock data
  const balance = 42.50;
  const isVPNActive = false;
  const hasActivePlan = true;

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Duna VPN</h1>
              <p className="text-gray-600">Welcome back, {mockUser.firstName}!</p>
            </div>
            <div className="w-12 h-12 bg-primary-500 rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-lg">
                {mockUser.firstName[0]}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="px-4 py-6 space-y-6">
        {/* Current Balance Card */}
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Current Balance</h3>
              <p className="text-3xl font-bold text-primary-500">${balance}</p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate('/balance')}
            >
              View Details
            </Button>
          </div>
        </Card>

        {/* VPN Connection Card */}
        <Card>
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center bg-gray-100">
              <svg className="w-8 h-8 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {isVPNActive ? 'VPN Connected' : 'VPN Disconnected'}
            </h3>
            <p className="text-gray-600 mb-4">
              {isVPNActive 
                ? 'Your connection is secure and private' 
                : hasActivePlan 
                  ? 'Click to connect to VPN' 
                  : 'Purchase a plan to start using VPN'
              }
            </p>
            <Button
              variant="primary"
              size="lg"
              onClick={() => navigate(hasActivePlan ? '/connect' : '/plans')}
              className="w-full"
            >
              {hasActivePlan ? 'Connect VPN' : 'Buy VPN Plan'}
            </Button>
          </div>
        </Card>

        {/* Invite Friend Card */}
        <Card>
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
              </svg>
            </div>
            <div className="flex-1">
              <h3 className="font-semibold text-gray-900">Invite Friends</h3>
              <p className="text-sm text-gray-600">
                Earn ${mockReferralData.totalEarned} from {mockReferralData.totalReferrals} referrals
              </p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate('/referral')}
            >
              Invite
            </Button>
          </div>
        </Card>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 gap-4">
          <Card>
            <div className="text-center">
              <p className="text-2xl font-bold text-primary-500">7</p>
              <p className="text-sm text-gray-600">Days Active</p>
            </div>
          </Card>
          <Card>
            <div className="text-center">
              <p className="text-2xl font-bold text-primary-500">2.1GB</p>
              <p className="text-sm text-gray-600">Data Used</p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default MainPage;
