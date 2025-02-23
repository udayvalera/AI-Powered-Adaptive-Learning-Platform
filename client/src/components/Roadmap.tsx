import React, { useState } from 'react';
import type { Roadmap } from '../types';
import { RoadmapNode } from './RoadmapNode';
import { Map, MessageSquare } from 'lucide-react';
import { Modal } from './Modal';
import Chat from './Chat';

interface RoadmapProps {
  data: Roadmap;
}

export function Roadmap({ data }: RoadmapProps) {
  const [isGlobalChatOpen, setIsGlobalChatOpen] = useState(false);

  return (
    <div className="max-w-6xl mx-auto py-12 px-4">
      <div className="text-center mb-12 relative">
        <div className="flex items-center justify-center gap-3 mb-4">
          <Map className="w-8 h-8 text-blue-500" />
          <h1 className="text-4xl font-bold text-gray-900">Learning Roadmap</h1>
        </div>
        <p className="text-lg text-gray-600 mb-6">Follow this personalized learning path to master the subject</p>
        
        <button
          onClick={() => setIsGlobalChatOpen(true)}
          className="mx-auto flex items-center gap-2 px-6 py-3 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors shadow-lg"
        >
          <MessageSquare className="w-5 h-5" />
          <span>Chat with AI about the Roadmap</span>
        </button>
      </div>

      <div className="relative">
        <div className="absolute left-1/2 top-0 bottom-0 w-1 bg-blue-200 transform -translate-x-1/2" />
        
        <div className="space-y-8">
          {data.roadmap.map((node, index) => (
            <RoadmapNode
              key={node.node_id}
              node={node}
              isLast={index === data.roadmap.length - 1}
              position={index % 2 === 0 ? 'left' : 'right'}
              index={index}
            />
          ))}
        </div>
      </div>

      <Modal isOpen={isGlobalChatOpen} onClose={() => setIsGlobalChatOpen(false)}>
        <div className="p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Chat about the Entire Roadmap</h2>
          <Chat topic="the entire learning roadmap" />
        </div>
      </Modal>
    </div>
  );
}