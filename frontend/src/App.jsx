import React from 'react';
import Dashboard from './components/Dashboard';

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <header className="mb-6 text-center">
        <h1 className="text-3xl font-bold">Surveillance IRM</h1>
        <p className="text-gray-600">Pression & Température en temps réel</p>
      </header>
      <main className="max-w-4xl mx-auto">
        <Dashboard />
      </main>
    </div>
  );
}