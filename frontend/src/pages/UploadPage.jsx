import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileUp, Loader2, FileText, CheckCircle2 } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function UploadPage({ t }) {
  const [isDragActive, setIsDragActive] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [file, setFile] = useState(null);
  const [classificationPreview, setClassificationPreview] = useState(null);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragActive(true);
    } else if (e.type === 'dragleave') {
      setIsDragActive(false);
    }
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      await processSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = async (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      await processSelectedFile(e.target.files[0]);
    }
  };

  const processSelectedFile = async (selectedFile) => {
    setFile(selectedFile);
    setIsUploading(true);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('user_id', 'testing-demo-user-123'); // Demo user since we don't have auth context yet
    formData.append('user_language', 'en');

    try {
      const res = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");

      const data = await res.json();
      setClassificationPreview(data);
    } catch (err) {
      alert("Failed to upload document: " + err.message);
    } finally {
      setIsUploading(false);
    }
  };

  const startAnalysis = () => {
    if (!classificationPreview) return;
    if (classificationPreview.requires_payment) {
      navigate('/subscribe'); // Or standard checkout flow
    } else {
      navigate(`/processing/${classificationPreview.document_id}`);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto mt-6">
      {!classificationPreview ? (
        <div className="bg-white shadow-xl rounded-2xl p-10 border border-border_color transition-all">
          <h1 className="text-4xl font-extrabold text-navy text-center mb-4 leading-tight">{t('welcome', "Welcome to LegalClear")}</h1>
          <p className="text-center text-gray-500 mb-8 max-w-xl mx-auto">Upload any legal document, contract, or court form. Our AI will analyze it instantly, explain your rights, and scan for risks.</p>
          
          <div 
            className={`flex flex-col items-center justify-center border-2 border-dashed rounded-xl p-16 transition-colors cursor-pointer group ${isDragActive ? 'border-teal bg-teal bg-opacity-10' : 'border-gray-300 bg-surface hover:border-teal hover:bg-teal hover:bg-opacity-5'}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input 
              ref={fileInputRef} 
              type="file" 
              className="hidden" 
              accept=".pdf,.png,.jpg,.jpeg" 
              onChange={handleChange} 
            />
            {isUploading ? (
              <div className="flex flex-col items-center text-teal">
                <Loader2 className="w-16 h-16 animate-spin mb-4" />
                <h3 className="text-xl font-bold">Reading Document...</h3>
                <p className="text-gray-500 mt-2">Running OCR and Classification</p>
              </div>
            ) : (
              <div className="flex flex-col items-center text-gray-400 group-hover:text-teal transition-colors">
                <FileUp className="w-20 h-20 mb-6 group-hover:scale-110 transition-transform duration-300" />
                <h3 className="text-2xl font-bold text-navy mb-2">{t('drag_drop', "Drag and drop your document here")}</h3>
                <p className="text-gray-500">{t('paste_text', "Or click to browse files (PDF, PNG, JPG)")}</p>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="bg-white shadow-xl rounded-2xl p-10 border border-border_color animate-in fade-in slide-in-from-bottom-4 duration-500">
           <div className="flex items-center space-x-6 mb-8 border-b pb-8">
              <div className="bg-teal bg-opacity-20 p-6 rounded-full text-teal">
                 <FileText className="w-12 h-12" />
              </div>
              <div>
                <h2 className="text-3xl font-bold text-navy flex items-center">
                  Document Identified <CheckCircle2 className="w-6 h-6 text-green-500 ml-3" />
                </h2>
                <p className="text-gray-500 font-medium text-lg mt-1">{file?.name}</p>
              </div>
           </div>

           <div className="grid grid-cols-2 gap-6 mb-10">
              <div className="bg-surface p-6 rounded-xl">
                 <p className="text-sm text-gray-500 uppercase tracking-wider font-semibold mb-1">Category</p>
                 <p className="text-xl font-bold text-navy capitalize">{classificationPreview.classification?.document_category?.replace('_', ' ')}</p>
              </div>
              <div className="bg-surface p-6 rounded-xl">
                 <p className="text-sm text-gray-500 uppercase tracking-wider font-semibold mb-1">Jurisdiction</p>
                 <p className="text-xl font-bold text-navy">{classificationPreview.classification?.jurisdiction_name}</p>
              </div>
              <div className="bg-surface p-6 rounded-xl">
                 <p className="text-sm text-gray-500 uppercase tracking-wider font-semibold mb-1">Complexity</p>
                 <p className="text-xl font-bold text-navy capitalize">{classificationPreview.classification?.estimated_complexity}</p>
              </div>
              <div className="bg-surface p-6 rounded-xl">
                 <p className="text-sm text-gray-500 uppercase tracking-wider font-semibold mb-1">Processing Tier</p>
                 <p className="text-xl font-bold text-teal capitalize">{classificationPreview.price_tier?.label}</p>
              </div>
           </div>

           <div className="mt-8 flex justify-end space-x-4">
              <button 
                onClick={() => { setClassificationPreview(null); setFile(null); }}
                className="px-6 py-3 rounded-lg font-bold text-gray-600 hover:bg-gray-100 transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={startAnalysis}
                className="px-8 py-3 bg-navy text-white rounded-lg font-bold hover:bg-opacity-90 transition-colors shadow-lg flex items-center"
              >
                Start AI Analysis
              </button>
           </div>
        </div>
      )}
    </div>
  );
}
