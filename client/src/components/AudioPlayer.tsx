import React from 'react';
import { Play, Pause, Volume2 } from 'lucide-react';

interface AudioPlayerProps {
  topic: string;
}

export default function AudioPlayer({ topic }: AudioPlayerProps) {
  const [isPlaying, setIsPlaying] = React.useState(false);
  const [progress, setProgress] = React.useState(0);

  React.useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isPlaying) {
      interval = setInterval(() => {
        setProgress(prev => Math.min(prev + 1, 100));
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isPlaying]);

  return (
    <div className="space-y-6">
      <div className="bg-gray-50 rounded-xl p-6">
        <h3 className="text-lg font-semibold mb-4">Audio Lesson: {topic}</h3>
        
        {/* Progress Bar */}
        <div className="h-1.5 bg-gray-200 rounded-full mb-4">
          <div 
            className="h-full bg-blue-500 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Controls */}
        <div className="flex items-center justify-between">
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="p-3 rounded-full bg-blue-500 text-white hover:bg-blue-600 transition-colors"
          >
            {isPlaying ? (
              <Pause className="w-6 h-6" />
            ) : (
              <Play className="w-6 h-6" />
            )}
          </button>

          <div className="flex items-center gap-4">
            <Volume2 className="w-5 h-5 text-gray-500" />
            <input
              type="range"
              min="0"
              max="100"
              className="w-24 h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
          </div>
        </div>
      </div>

      {/* Transcript */}
      <div>
        <h4 className="font-medium text-gray-900 mb-3">Transcript</h4>
        <div className="bg-gray-50 rounded-lg p-4 text-gray-600 text-sm leading-relaxed">
          This is a sample transcript for the audio lesson about {topic}. 
          The actual content would be generated based on the topic and learning materials.
        </div>
      </div>
    </div>
  );
}