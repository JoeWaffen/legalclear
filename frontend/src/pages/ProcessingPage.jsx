import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Loader2, BrainCircuit, ShieldAlert, Sparkles, Wand2 } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function ProcessingPage({ t }) {
  const { documentId } = useParams();
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    { icon: <BrainCircuit className="w-8 h-8" />, title: "Reading Document..." },
    { icon: <Wand2 className="w-8 h-8" />, title: "Translating to Plain English..." },
    { icon: <ShieldAlert className="w-8 h-8" />, title: "Scanning for Risks..." },
    { icon: <Sparkles className="w-8 h-8" />, title: "Preparing Final Report..." }
  ];

  useEffect(() => {
    // Cycle through visual steps for UI sugar
    const interval = setInterval(() => {
      setCurrentStep(s => Math.min(s + 1, steps.length - 1));
    }, 2500);

    // Actual API Call
    fetch(`${API_URL}/process/${documentId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    })
      .then(res => res.json())
      .then(data => {
        clearInterval(interval);
        if (data.status === "complete" || data.document_id) {
           navigate(`/results/${documentId}`);
        } else {
           alert("Processing did not complete cleanly.");
        }
      })
      .catch(err => {
        clearInterval(interval);
        alert("Processing Error: " + err.message);
      });

    return () => clearInterval(interval);
  }, [documentId, navigate]);

  return (
    <div className="w-full max-w-2xl mx-auto mt-20 text-center">
      <div className="bg-white shadow-2xl rounded-3xl p-16 border border-border_color relative overflow-hidden">
        {/* Animated Background Blob */}
        <div className="absolute top-0 left-0 w-full h-full overflow-hidden opacity-20 pointer-events-none">
           <div className="absolute -top-[50%] -left-[50%] w-[200%] h-[200%] animate-spin-slow bg-gradient-to-r from-teal via-white to-navy mix-blend-multiply filter blur-3xl opacity-30"></div>
        </div>

        <div className="relative z-10">
          <Loader2 className="w-24 h-24 text-teal animate-spin mx-auto mb-10" />
          
          <h2 className="text-3xl font-extrabold text-navy mb-8 transition-all duration-300">
            {steps[currentStep].title}
          </h2>

          <div className="flex justify-center items-center space-x-6">
            {steps.map((step, idx) => (
              <div 
                key={idx} 
                className={`transition-all duration-500 rounded-full p-4 ${idx === currentStep ? 'bg-teal text-white scale-110 shadow-lg' : idx < currentStep ? 'bg-green-100 text-green-500' : 'bg-gray-100 text-gray-400'}`}
              >
                {step.icon}
              </div>
            ))}
          </div>
          
          <p className="text-gray-500 mt-10 font-medium">This usually takes about 10-15 seconds. Please don't close this window.</p>
        </div>
      </div>
    </div>
  );
}
