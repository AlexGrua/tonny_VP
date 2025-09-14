import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { mockPlans } from '../constants/mockData';

const PlansPage: React.FC = () => {
  const navigate = useNavigate();
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null);

  const handleSelectPlan = (planId: string) => {
    setSelectedPlan(planId);
  };

  const handlePurchase = () => {
    if (selectedPlan) {
      navigate('/payment', { state: { planId: selectedPlan } });
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="px-4 py-6">
          <h1 className="text-2xl font-bold text-gray-900">VPN Plans</h1>
          <p className="text-gray-600">Choose the perfect plan for your needs</p>
        </div>
      </div>

      <div className="px-4 py-6 space-y-6">
        {/* Current Balance */}
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Current Balance</h3>
              <p className="text-2xl font-bold text-primary-500">$42.50</p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate('/balance')}
            >
              Top Up
            </Button>
          </div>
        </Card>

        {/* Current Plan */}
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Current Plan</h3>
              <p className="text-gray-600">Pro Plan - Active until Feb 10, 2024</p>
            </div>
            <span className="px-3 py-1 bg-green-100 text-green-800 text-sm font-medium rounded-full">
              Active
            </span>
          </div>
        </Card>

        {/* Plan Selector */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-900">Available Plans</h2>
          
          {mockPlans.map((plan) => (
            <Card
              key={plan.id}
              className={`cursor-pointer transition-all duration-200 ${
                selectedPlan === plan.id
                  ? 'ring-2 ring-primary-500 bg-primary-50'
                  : 'hover:shadow-md'
              } ${plan.popular ? 'border-primary-200' : ''}`}
              onClick={() => handleSelectPlan(plan.id)}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">{plan.name}</h3>
                    {plan.popular && (
                      <span className="px-2 py-1 bg-primary-500 text-white text-xs font-medium rounded-full">
                        Popular
                      </span>
                    )}
                  </div>
                  
                  <div className="mb-3">
                    <span className="text-3xl font-bold text-primary-500">${plan.price}</span>
                    <span className="text-gray-600">/month</span>
                  </div>
                  
                  <ul className="space-y-1">
                    {plan.features.map((feature, index) => (
                      <li key={index} className="flex items-center text-sm text-gray-600">
                        <svg className="w-4 h-4 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div className="ml-4">
                  <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                    selectedPlan === plan.id
                      ? 'border-primary-500 bg-primary-500'
                      : 'border-gray-300'
                  }`}>
                    {selectedPlan === plan.id && (
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    )}
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>

        {/* Purchase Button */}
        {selectedPlan && (
          <div className="sticky bottom-4">
            <Button
              variant="primary"
              size="lg"
              onClick={handlePurchase}
              className="w-full"
            >
              Purchase Selected Plan
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default PlansPage;
