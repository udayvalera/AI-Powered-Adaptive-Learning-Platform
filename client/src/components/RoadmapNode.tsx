import React, { useState, lazy, Suspense } from 'react';
import { Clock, BookOpen, GraduationCap, Headphones, MessageSquare } from 'lucide-react';
import type { RoadmapNode as RoadmapNodeType } from '../types';
import { Modal } from './Modal';
import { LoadingSpinner } from './LoadingSpinner';

// Lazy loaded components
const AudioPlayer = lazy(() => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(import('./AudioPlayer'));
    }, 1000);
  });
});

const Quiz = lazy(() => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(import('./Quiz'));
    }, 1000);
  });
});

const Chat = lazy(() => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(import('./Chat'));
    }, 1000);
  });
});

interface RoadmapNodeProps {
  node: RoadmapNodeType;
  isLast: boolean;
  position: 'left' | 'right';
  index: number;
}

const difficultyColors = {
  Beginner: 'bg-green-100 text-green-800 border-green-200',
  Intermediate: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  Advanced: 'bg-red-100 text-red-800 border-red-200',
};

export function RoadmapNode({ node, isLast, position, index }: RoadmapNodeProps) {
  const isLeft = position === 'left';
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<'audio' | 'quiz' | 'chat'>('audio');

  return (
    <>
      <div className={`flex items-center gap-4 ${isLeft ? 'flex-row' : 'flex-row-reverse'} relative`}>
        {/* Connecting Lines */}
        {!isLast && (
          <div className="absolute top-1/2 w-8 h-[calc(100%+2rem)] border-2 border-blue-200 rounded-lg"
               style={{
                 [isLeft ? 'left' : 'right']: '2.5rem',
                 transform: 'translateY(1rem)',
                 borderTop: 'none',
                 borderBottom: 'none',
                 borderRight: isLeft ? 'none' : undefined,
                 borderLeft: isLeft ? undefined : 'none',
               }}
          />
        )}
        
        {/* Node Number */}
        <div className="relative z-10">
          <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold shadow-lg">
            {node.node_id}
          </div>
        </div>

        {/* Content Card */}
        <div 
          onClick={() => setIsModalOpen(true)}
          className={`flex-1 max-w-xl bg-white rounded-xl shadow-lg border-2 border-gray-100 p-6 my-4 transform transition-all duration-300 hover:scale-[1.02] hover:shadow-xl cursor-pointer ${
            isLeft ? 'hover:translate-x-2' : 'hover:-translate-x-2'
          }`}
        >
          <div className="flex justify-between items-start gap-4 mb-4">
            <h3 className="text-xl font-bold text-gray-900">{node.topic}</h3>
            <span className={`px-4 py-1.5 rounded-full text-sm font-medium border ${difficultyColors[node.difficulty]}`}>
              {node.difficulty}
            </span>
          </div>
          
          <p className="text-gray-600 mb-4">{node.summary}</p>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6 text-sm text-gray-500">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4" />
                <span>{node.estimated_time}</span>
              </div>
              <div className="flex items-center gap-2">
                <BookOpen className="w-4 h-4" />
                <span>Related: {node.related_chunks.join(', ')}</span>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <button className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors">
                <Headphones className="w-4 h-4" />
                Learn
              </button>
              {node.quiz && (
                <button className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors">
                  <GraduationCap className="w-4 h-4" />
                  Quiz
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <div className="p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">{node.topic}</h2>
          
          {/* Tabs */}
          <div className="border-b border-gray-200 mb-6">
            <div className="flex gap-4">
              <button
                onClick={() => setActiveTab('audio')}
                className={`pb-4 text-sm font-medium transition-colors relative ${
                  activeTab === 'audio' 
                    ? 'text-blue-600 border-b-2 border-blue-600' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Headphones className="w-4 h-4" />
                  Audio Lesson
                </div>
              </button>
              <button
                onClick={() => setActiveTab('quiz')}
                className={`pb-4 text-sm font-medium transition-colors relative ${
                  activeTab === 'quiz'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <div className="flex items-center gap-2">
                  <GraduationCap className="w-4 h-4" />
                  Quiz
                </div>
              </button>
              <button
                onClick={() => setActiveTab('chat')}
                className={`pb-4 text-sm font-medium transition-colors relative ${
                  activeTab === 'chat'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <div className="flex items-center gap-2">
                  <MessageSquare className="w-4 h-4" />
                  AI Chat
                </div>
              </button>
            </div>
          </div>

          {/* Tab Content */}
          <div className="min-h-[400px]">
            <Suspense fallback={<LoadingSpinner />}>
              {activeTab === 'audio' ? (
                <AudioPlayer topic={node.topic} />
              ) : activeTab === 'quiz' ? (
                <Quiz quiz={{ node_id: node.node_id, topic: node.topic }} />
              ) : (
                <Chat topic={node.topic} />
              )}
            </Suspense>
          </div>
        </div>
      </Modal>
    </>
  );
}