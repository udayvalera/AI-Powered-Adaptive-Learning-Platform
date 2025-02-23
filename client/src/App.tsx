import React, { useState, useCallback } from 'react';
import { Roadmap } from './components/Roadmap';
import { Upload, FileText, Loader2 } from 'lucide-react';
import { documentService, roadmapService } from './services/api';

export default function App() {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadPhase, setUploadPhase] = useState<'uploading' | 'creating' | null>(null);
  const [showRoadmap, setShowRoadmap] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [roadmapData, setRoadmapData] = useState(null);
  const [error, setError] = useState<string | null>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files[0];
    if (file) {
      await handleFileUpload(file);
    }
  }, []);

  const handleFileSelect = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      await handleFileUpload(file);
    }
  }, []);

  const handleFileUpload = async (file: File) => {
    setIsUploading(true);
    setError(null);
    setUploadPhase('uploading');
    
    try {
      // Process the document
      await documentService.processDocument(file);
      
      // Update phase to creating roadmap
      setUploadPhase('creating');
      
      // Fetch the generated roadmap
      const roadmap = await roadmapService.getRoadmap();
      setRoadmapData(roadmap);
      // Store roadmap data in cookie
      document.cookie = `roadmap_data=${JSON.stringify(roadmap)}; path=/; max-age=3600`;
      setShowRoadmap(true);
    } catch (error) {
      console.error('Error processing file:', error);
      setError('There was an error processing your document. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  if (showRoadmap && roadmapData) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Roadmap data={roadmapData} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 flex flex-col items-center justify-center p-4">
      <div className="max-w-2xl w-full text-center mb-8">
        <h1 className="text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 mb-6 tracking-tight hover:scale-105 transition-transform duration-300">
          Edunova
        </h1>
        <p className="text-lg text-gray-600">
          Upload your document and get a personalized learning roadmap with quizzes and progress tracking
        </p>
      </div>

      <div
        className={`
          w-full max-w-xl bg-white rounded-xl shadow-xl p-8 transition-all duration-300
          ${isDragging ? 'border-2 border-blue-500 bg-blue-50' : 'border-2 border-dashed border-gray-300'}
          ${isUploading ? 'opacity-75' : ''}
        `}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {isUploading ? (
          <div className="flex flex-col items-center justify-center py-8">
            <Loader2 className="w-12 h-12 text-blue-500 animate-spin mb-4" />
            <p className="text-lg font-medium text-gray-900">
              {uploadPhase === 'uploading' ? 'Uploading your document' : 'Creating your learning roadmap'}
            </p>
            <p className="text-sm text-gray-500 mt-2">
              {uploadPhase === 'uploading' ? 'Uploading and processing your file...' : 'Analyzing content and generating roadmap...'}
            </p>
          </div>
        ) : (
          <>
            <div className="flex flex-col items-center justify-center py-8">
              <div className="bg-blue-50 rounded-full p-4 mb-6">
                <Upload className="w-8 h-8 text-blue-500" />
              </div>
              <p className="text-lg font-medium text-gray-900 mb-2">
                Drag and drop your document here
              </p>
              <p className="text-sm text-gray-500 mb-6">
                or click to select a file
              </p>
              <label className="relative">
                <input
                  type="file"
                  className="hidden"
                  onChange={handleFileSelect}
                  accept=".pdf,.doc,.docx,.txt"
                />
                <span className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg cursor-pointer transition-colors inline-flex items-center">
                  <FileText className="w-5 h-5 mr-2" />
                  Choose File
                </span>
              </label>
            </div>
            <div className="border-t border-gray-200 pt-6 mt-2">
              <p className="text-sm text-gray-500 text-center">
                Supported formats: PDF, DOC, DOCX, TXT
              </p>
            </div>
          </>
        )}
        {error && (
          <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}