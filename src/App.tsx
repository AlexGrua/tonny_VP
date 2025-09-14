import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import BottomNavigation from './components/layout/BottomNavigation';
import MainPage from './pages/MainPage';
import PlansPage from './pages/PlansPage';
import SettingsPage from './pages/SettingsPage';

// Placeholder components for additional pages
const BalancePage = () => (
  <div className="min-h-screen bg-gray-50 pb-20 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Balance Page</h1>
      <p className="text-gray-600">Coming soon...</p>
    </div>
  </div>
);

const ConnectPage = () => (
  <div className="min-h-screen bg-gray-50 pb-20 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Connect VPN</h1>
      <p className="text-gray-600">Coming soon...</p>
    </div>
  </div>
);

const ReferralPage = () => (
  <div className="min-h-screen bg-gray-50 pb-20 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Referral Program</h1>
      <p className="text-gray-600">Coming soon...</p>
    </div>
  </div>
);

const PaymentPage = () => (
  <div className="min-h-screen bg-gray-50 pb-20 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Payment</h1>
      <p className="text-gray-600">Coming soon...</p>
    </div>
  </div>
);

const HowToUsePage = () => (
  <div className="min-h-screen bg-gray-50 pb-20 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">How to Use</h1>
      <p className="text-gray-600">Coming soon...</p>
    </div>
  </div>
);

const AboutPage = () => (
  <div className="min-h-screen bg-gray-50 pb-20 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">About Us</h1>
      <p className="text-gray-600">Coming soon...</p>
    </div>
  </div>
);

const ContactPage = () => (
  <div className="min-h-screen bg-gray-50 pb-20 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Contact Us</h1>
      <p className="text-gray-600">Coming soon...</p>
    </div>
  </div>
);

const PrivacyPolicyPage = () => (
  <div className="min-h-screen bg-gray-50 pb-20 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Privacy Policy</h1>
      <p className="text-gray-600">Coming soon...</p>
    </div>
  </div>
);

const TermsPage = () => (
  <div className="min-h-screen bg-gray-50 pb-20 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Terms of Use</h1>
      <p className="text-gray-600">Coming soon...</p>
    </div>
  </div>
);

const RefundPolicyPage = () => (
  <div className="min-h-screen bg-gray-50 pb-20 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Refund Policy</h1>
      <p className="text-gray-600">Coming soon...</p>
    </div>
  </div>
);

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Main navigation routes */}
          <Route path="/" element={<MainPage />} />
          <Route path="/plans" element={<PlansPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          
          {/* Additional pages */}
          <Route path="/balance" element={<BalancePage />} />
          <Route path="/connect" element={<ConnectPage />} />
          <Route path="/referral" element={<ReferralPage />} />
          <Route path="/payment" element={<PaymentPage />} />
          <Route path="/how-to-use" element={<HowToUsePage />} />
          <Route path="/about-us" element={<AboutPage />} />
          <Route path="/contact-us" element={<ContactPage />} />
          <Route path="/privacy-policy" element={<PrivacyPolicyPage />} />
          <Route path="/terms-of-use" element={<TermsPage />} />
          <Route path="/refund-policy" element={<RefundPolicyPage />} />
        </Routes>
        
        {/* Bottom Navigation - only show on main pages */}
        <Routes>
          <Route path="/" element={<BottomNavigation />} />
          <Route path="/plans" element={<BottomNavigation />} />
          <Route path="/settings" element={<BottomNavigation />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
