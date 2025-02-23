import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, Lightbulb, BookOpen, Loader2 } from 'lucide-react';
import { chatService } from '../services/api';

interface Message {
  id: string;
  type: 'user' | 'ai';
  content: string;
}

const SimpleMarkdownRenderer = ({ content = '' }) => {
  if (!content) return null;
  
  const textContent = String(content);
  
  const parseContent = (text) => {
    const blocks = text.split(/\r?\n\r?\n/);
    
    return blocks.map((block, blockIndex) => {
      if (!block.trim()) return null;

      if (block.startsWith('# ')) {
        return <h1 key={blockIndex} className="text-2xl font-bold my-4">{block.slice(2)}</h1>;
      }
      if (block.startsWith('## ')) {
        return <h2 key={blockIndex} className="text-xl font-bold my-3">{block.slice(3)}</h2>;
      }
      if (block.startsWith('### ')) {
        return <h3 key={blockIndex} className="text-lg font-bold my-2">{block.slice(4)}</h3>;
      }

      if (block.startsWith('```')) {
        const code = block.slice(3, -3).trim();
        return (
          <pre key={blockIndex} className="bg-gray-100 p-4 rounded-lg my-2 font-mono text-sm overflow-auto">
            <code>{code}</code>
          </pre>
        );
      }

      if (block.startsWith('> ')) {
        return (
          <blockquote key={blockIndex} className="border-l-4 border-blue-500 pl-4 my-2 italic">
            {block.slice(2)}
          </blockquote>
        );
      }

      const lines = block.split(/\r?\n/);
      
      if (lines.every(line => line.trim().startsWith('- '))) {
        const items = lines.map(line => line.trim().slice(2));
        return (
          <ul key={blockIndex} className="list-disc pl-5 my-2">
            {items.map((item, i) => <li key={i}>{item}</li>)}
          </ul>
        );
      }

      if (lines.every(line => /^\d+\.\s/.test(line.trim()))) {
        const items = lines.map(line => line.trim().replace(/^\d+\.\s/, ''));
        return (
          <ol key={blockIndex} className="list-decimal pl-5 my-2">
            {items.map((item, i) => <li key={i}>{item}</li>)}
          </ol>
        );
      }

      const processInlineCode = (text) => {
        if (!text.includes('`')) return text;
        const parts = text.split('`');
        return parts.map((part, i) => {
          if (i % 2 === 1) {
            return <code key={i} className="bg-gray-100 px-1 rounded">{part}</code>;
          }
          return part;
        });
      };

      return <p key={blockIndex} className="my-2">{processInlineCode(block)}</p>;
    }).filter(Boolean);
  };

  return <div className="markdown-content">{parseContent(textContent)}</div>;
};

export default function Chat({ topic }: { topic: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await chatService.sendMessage(
        `Context: The topic is ${topic}. Question: ${input}`
      );

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: response
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: "I apologize, but I'm having trouble processing your request right now. Please try again later."
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] bg-white">
      {/* Educational Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 rounded-t-lg">
        <div className="flex items-center gap-3 mb-2">
          <BookOpen className="w-6 h-6" />
          <h2 className="text-xl font-semibold">Learning Assistant</h2>
        </div>
        <p className="text-blue-100">
          Ask questions about {topic} to deepen your understanding
        </p>
      </div>

      {/* Chat Content */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center text-gray-500">
            <Lightbulb className="w-12 h-12 mb-4 text-blue-500" />
            <h3 className="text-lg font-medium mb-2">Start Learning</h3>
            <p className="max-w-sm">
              Ask questions about concepts, request explanations, or seek clarification about {topic}
            </p>
          </div>
        ) : (
          messages.map(message => (
            <div
              key={message.id}
              className={`${
                message.type === 'user' ? 'ml-auto' : ''
              }`}
            >
              <div className={`
                max-w-[80%] rounded-lg p-4
                ${message.type === 'user'
                  ? 'bg-blue-500 text-white ml-auto'
                  : 'bg-gray-50 border border-gray-200'
                }
              `}>
                {message.type === 'user' ? (
                  <p>{message.content}</p>
                ) : (
                  <div className="prose prose-sm max-w-none">
                    <div className="flex items-center gap-2 mb-3">
                      <Bot className="w-5 h-5 text-blue-500" />
                      <span className="font-medium text-blue-500">Learning Assistant</span>
                    </div>
                    <SimpleMarkdownRenderer content={message.content} />
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex items-center gap-2 text-gray-500">
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>Generating response...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Question Input */}
      <div className="border-t border-gray-200 p-6 bg-gray-50">
        <form onSubmit={handleSubmit} className="flex gap-4">
          <div className="flex-1">
            <label htmlFor="question" className="block text-sm font-medium text-gray-700 mb-2">
              Your Question
            </label>
            <input
              id="question"
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={`Ask about ${topic}...`}
              disabled={isLoading}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
            />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="self-end px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors flex items-center gap-2 disabled:bg-blue-300 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Processing...' : 'Ask'}
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}