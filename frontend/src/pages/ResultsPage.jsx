import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { ShieldCheck, ShieldAlert, FileText, Info, AlertTriangle, AlertCircle, PlayCircle, BookOpen } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function ResultsPage({ t }) {
  const { documentId } = useParams();
  const [doc, setDoc] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('summary');

  useEffect(() => {
    fetch(`${API_URL}/document/${documentId}`)
      .then(r => r.json())
      .then(data => {
        setDoc(data);
        setLoading(false);
      })
      .catch(err => {
        alert("Failed to load results: " + err);
        setLoading(false);
      });
  }, [documentId]);

  if (loading) {
    return <div className="text-center mt-20 p-10"><p className="text-xl">Loading your results...</p></div>;
  }

  if (!doc || !doc.explanation) {
    return <div className="text-center mt-20 p-10"><p className="text-xl text-red-500">Document analysis not found or incomplete.</p></div>;
  }

  const expl = doc.explanation;
  const risk = doc.risk_scan;
  const guide = doc.form_guide;

  return (
    <div className="w-full max-w-6xl mx-auto flex flex-col md:flex-row gap-8">
      {/* Sidebar Navigation */}
      <div className="w-full md:w-64 flex-shrink-0">
        <div className="bg-white rounded-xl shadow border border-gray-200 overflow-hidden sticky top-6">
          <div className="p-4 bg-navy text-white">
            <h3 className="font-bold">Document Analysis</h3>
          </div>
          <div className="flex flex-col p-2 space-y-1">
            <button onClick={() => setActiveTab('summary')} className={`px-4 py-3 text-left rounded-lg font-medium transition-colors flex items-center space-x-3 ${activeTab === 'summary' ? 'bg-teal bg-opacity-10 text-teal' : 'text-gray-600 hover:bg-gray-50'}`}>
              <BookOpen className="w-5 h-5" /> <span>Summary</span>
            </button>
            <button onClick={() => setActiveTab('risks')} className={`px-4 py-3 text-left rounded-lg font-medium transition-colors flex items-center space-x-3 ${activeTab === 'risks' ? 'bg-teal bg-opacity-10 text-teal' : 'text-gray-600 hover:bg-gray-50'}`}>
              <ShieldAlert className="w-5 h-5" /> <span>Risk Scan</span>
            </button>
            {guide && guide.sections && guide.sections.length > 0 && (
              <button onClick={() => setActiveTab('forms')} className={`px-4 py-3 text-left rounded-lg font-medium transition-colors flex items-center space-x-3 ${activeTab === 'forms' ? 'bg-teal bg-opacity-10 text-teal' : 'text-gray-600 hover:bg-gray-50'}`}>
                <FileText className="w-5 h-5" /> <span>Form Guide</span>
              </button>
            )}
            <button onClick={() => setActiveTab('chat')} className={`px-4 py-3 text-left rounded-lg font-medium transition-colors flex items-center space-x-3 ${activeTab === 'chat' ? 'bg-teal bg-opacity-10 text-teal' : 'text-gray-600 hover:bg-gray-50'}`}>
              <Info className="w-5 h-5" /> <span>Ask Questions</span>
            </button>
          </div>
        </div>
      </div>

      {/* Content Area */}
      <div className="flex-grow">
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden min-h-[600px]">
          
          {/* Summary Tab */}
          {activeTab === 'summary' && (
            <div className="p-8 animate-in fade-in duration-300">
              <h2 className="text-3xl font-extrabold text-navy mb-6">Plain English Explanation</h2>
              
              <div className="bg-teal bg-opacity-5 border-l-4 border-teal p-6 rounded-r-xl mb-8">
                <h3 className="text-xl font-bold text-navy mb-3">Overall Summary</h3>
                <p className="text-lg text-gray-700 leading-relaxed">{expl.summary}</p>
              </div>

              <div className="grid md:grid-cols-2 gap-8 mb-8">
                 <div>
                    <h3 className="text-xl font-bold text-navy mb-4 flex items-center"><PlayCircle className="w-6 h-6 mr-2 text-teal"/> What this means for you</h3>
                    <p className="text-gray-600 leading-relaxed bg-gray-50 p-5 rounded-xl">{expl.what_this_means_for_you}</p>
                 </div>
                 <div>
                    <h3 className="text-xl font-bold text-navy mb-4">Questions you should ask</h3>
                    <ul className="space-y-3">
                      {expl.questions_to_ask?.map((q, i) => (
                        <li key={i} className="flex items-start bg-blue-50 p-3 rounded-lg border border-blue-100">
                          <span className="bg-blue-200 text-blue-800 rounded-full w-6 h-6 flex items-center justify-center font-bold text-sm mr-3 shrink-0">{i+1}</span>
                          <span className="text-blue-900">{q}</span>
                        </li>
                      ))}
                    </ul>
                 </div>
              </div>

              <div className="grid md:grid-cols-2 gap-8">
                 <div>
                    <h3 className="text-lg font-bold text-navy mb-3 border-b pb-2">Your Rights</h3>
                    <ul className="list-disc pl-5 text-gray-600 space-y-2">
                       {expl.your_rights?.map((r, i) => <li key={i}>{r}</li>)}
                    </ul>
                 </div>
                 <div>
                    <h3 className="text-lg font-bold text-navy mb-3 border-b pb-2">Your Obligations</h3>
                    <ul className="list-disc pl-5 text-gray-600 space-y-2">
                       {expl.your_obligations?.map((r, i) => <li key={i}>{r}</li>)}
                    </ul>
                 </div>
              </div>
            </div>
          )}

          {/* Risk Scan Tab */}
          {activeTab === 'risks' && (
            <div className="p-8 animate-in fade-in duration-300">
              <div className="flex justify-between items-end border-b pb-6 mb-8">
                <div>
                  <h2 className="text-3xl font-extrabold text-navy mb-2">Risk Analysis</h2>
                  <p className="text-gray-600">{risk?.risk_summary}</p>
                </div>
                <div className={`px-6 py-3 rounded-xl font-bold flex items-center ${risk?.overall_risk_level === 'HIGH' ? 'bg-red-100 text-red-700' : risk?.overall_risk_level === 'MEDIUM' ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'}`}>
                  {risk?.overall_risk_level === 'HIGH' ? <AlertTriangle className="mr-2" /> : risk?.overall_risk_level === 'MEDIUM' ? <AlertCircle className="mr-2" /> : <ShieldCheck className="mr-2" />}
                  OVERALL RISK: {risk?.overall_risk_level}
                </div>
              </div>

              <div className="space-y-6">
                {risk?.clauses?.map((c, i) => (
                  <div key={i} className={`p-6 rounded-xl border ${c.risk_level === 'RED' ? 'bg-red-50 border-red-200' : c.risk_level === 'YELLOW' ? 'bg-yellow-50 border-yellow-200' : 'bg-green-50 border-green-200'}`}>
                    <div className="flex items-start justify-between mb-3">
                      <h3 className={`text-lg font-bold ${c.risk_level === 'RED' ? 'text-red-800' : c.risk_level === 'YELLOW' ? 'text-yellow-800' : 'text-green-800'}`}>
                        {c.clause_title}
                      </h3>
                      <span className={`text-xs font-bold px-3 py-1 rounded-full ${c.risk_level === 'RED' ? 'bg-red-200 text-red-800' : c.risk_level === 'YELLOW' ? 'bg-yellow-200 text-yellow-800' : 'bg-green-200 text-green-800'}`}>
                        {c.risk_level}
                      </span>
                    </div>
                    <p className="text-gray-800 font-medium mb-2">{c.what_it_says}</p>
                    <p className="text-gray-600 text-sm mb-4"><span className="font-bold">Why it matters:</span> {c.why_it_matters}</p>
                    
                    <div className="bg-white bg-opacity-50 p-4 rounded-lg">
                      <p className="text-sm font-semibold mb-1">What you should do:</p>
                      <p className="text-sm">{c.what_to_do}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Form Guide Tab */}
          {activeTab === 'forms' && guide && (
             <div className="p-8 animate-in fade-in duration-300">
               <h2 className="text-3xl font-extrabold text-navy mb-6">Form Completion Guide</h2>
               <p className="text-gray-600 mb-8">{guide.form_overview}</p>

               <div className="space-y-8">
                 {guide.sections?.map((sec, i) => (
                    <div key={i} className="border border-gray-200 rounded-xl overflow-hidden">
                       <div className="bg-gray-50 border-b border-gray-200 p-4">
                          <h3 className="font-bold text-navy text-lg">{sec.section_name}</h3>
                          <p className="text-gray-500 text-sm mt-1">{sec.description}</p>
                       </div>
                       <div className="p-0">
                          <table className="w-full text-left text-sm">
                             <thead className="bg-gray-50 text-gray-500 uppercase">
                               <tr>
                                 <th className="px-6 py-3 border-b">Field</th>
                                 <th className="px-6 py-3 border-b">Instructions</th>
                                 <th className="px-6 py-3 border-b">Example</th>
                               </tr>
                             </thead>
                             <tbody>
                               {sec.fields?.map((f, j) => (
                                 <tr key={j} className="border-b last:border-0 hover:bg-gray-50">
                                   <td className="px-6 py-4 font-medium text-navy">{f.plain_label} {f.required && <span className="text-red-500">*</span>}</td>
                                   <td className="px-6 py-4 text-gray-600">{f.instructions}</td>
                                   <td className="px-6 py-4 text-gray-500 italic">{f.example}</td>
                                 </tr>
                               ))}
                             </tbody>
                          </table>
                       </div>
                    </div>
                 ))}
               </div>
             </div>
          )}

          {/* Chat Tab Stub */}
          {activeTab === 'chat' && (
             <div className="p-8 animate-in fade-in duration-300 flex flex-col h-full">
               <h2 className="text-3xl font-extrabold text-navy mb-2">Have specific questions?</h2>
               <p className="text-gray-500 mb-8">Ask our AI explainer anything about your document.</p>
               
               <div className="flex-grow bg-gray-50 rounded-xl border border-gray-200 flex items-center justify-center text-gray-400 italic">
                  Chat interface rendering...
               </div>
               
               <div className="mt-4 flex gap-2">
                 <input type="text" className="flex-grow border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-teal" placeholder="e.g. Can I cancel this contract tomorrow?" />
                 <button className="bg-teal text-white px-6 py-3 rounded-lg font-bold">Ask</button>
               </div>
             </div>
          )}

        </div>
      </div>
    </div>
  );
}
