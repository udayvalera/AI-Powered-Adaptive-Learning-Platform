import React, { useState, useEffect } from 'react';
import { Check, X, RefreshCw } from 'lucide-react';
import { quizService } from '../services/api';
import { quizCache } from './Roadmap';

interface Question {
  question_id: number;
  question: string;
  options: string[];
  correct_answer: string;
  explanation: string;
  related_chunks: string[];
}

interface QuizProps {
  quiz: {
    node_id: number;
    topic: string;
  };
}

export default function Quiz({ quiz }: QuizProps) {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<(number | null)[]>([]);
  const [hasSubmitted, setHasSubmitted] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (quiz.node_id) {
      loadQuiz();
    }
  }, [quiz.node_id]);

  const loadQuiz = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Check if quiz is in cache
      const cachedQuiz = quizCache[quiz.node_id];
      if (cachedQuiz) {
        setQuestions(cachedQuiz.quiz);
        setSelectedAnswers(new Array(cachedQuiz.quiz.length).fill(null));
        setCurrentQuestion(0);
        setHasSubmitted(false);
        setIsLoading(false);
        return;
      }
      
      // If not in cache, fetch from server
      const cookies = document.cookie.split(';');
      const roadmapCookie = cookies.find(cookie => cookie.trim().startsWith('roadmap_data='));
      if (!roadmapCookie) {
        throw new Error('Roadmap data not found');
      }
      
      const roadmapData = JSON.parse(roadmapCookie.split('=')[1]);
      const nodeData = roadmapData.roadmap.find((node: any) => node.node_id === quiz.node_id);
      if (!nodeData) {
        throw new Error('Node data not found');
      }

      const response = await quizService.getQuiz({ ...quiz, node_data: nodeData });
      setQuestions(response.quiz);
      setSelectedAnswers(new Array(response.quiz.length).fill(null));
      setCurrentQuestion(0);
      setHasSubmitted(false);
    } catch (err) {
      setError('Failed to load quiz. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnswer = (questionIndex: number, answerIndex: number) => {
    if (hasSubmitted) return;
    
    const newAnswers = [...selectedAnswers];
    newAnswers[questionIndex] = answerIndex;
    setSelectedAnswers(newAnswers);
  };

  const handleSubmit = () => {
    setHasSubmitted(true);
  };

  const resetQuiz = () => {
    setSelectedAnswers(new Array(questions.length).fill(null));
    setCurrentQuestion(0);
    setHasSubmitted(false);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] p-6">
        <p className="text-red-500 mb-4">{error}</p>
        <button
          onClick={loadQuiz}
          className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          Try Again
        </button>
      </div>
    );
  }

  const currentQ = questions[currentQuestion];
  const isAnswered = selectedAnswers[currentQuestion] !== null;
  const isCorrect = hasSubmitted && selectedAnswers[currentQuestion] === currentQ.options.indexOf(currentQ.correct_answer);
  const totalQuestions = questions.length;
  const answeredQuestions = selectedAnswers.filter(answer => answer !== null).length;
  const correctAnswers = hasSubmitted ? selectedAnswers.reduce((acc, answer, index) => {
    return acc + (answer === questions[index].options.indexOf(questions[index].correct_answer) ? 1 : 0);
  }, 0) : 0;

  return (
    <div className="space-y-6">
      {/* Progress Bar */}
      <div className="bg-gray-100 rounded-full h-2 mb-6">
        <div
          className="bg-blue-500 h-2 rounded-full transition-all"
          style={{ width: `${(answeredQuestions / totalQuestions) * 100}%` }}
        />
      </div>

      {/* Question */}
      <div className="space-y-4">
        <h3 className="text-lg font-medium text-gray-900">
          Question {currentQuestion + 1} of {totalQuestions}
        </h3>
        <p className="text-gray-700">{currentQ.question}</p>

        {/* Options */}
        <div className="space-y-2">
          {currentQ.options.map((option, index) => (
            <button
              key={index}
              onClick={() => handleAnswer(currentQuestion, index)}
              disabled={hasSubmitted}
              className={`w-full p-4 text-left rounded-lg border-2 transition-all ${hasSubmitted
                ? index === currentQ.options.indexOf(currentQ.correct_answer)
                  ? 'border-green-500 bg-green-50'
                  : selectedAnswers[currentQuestion] === index
                    ? 'border-red-500 bg-red-50'
                    : 'border-gray-200'
                : selectedAnswers[currentQuestion] === index
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-blue-200 hover:bg-blue-50'
              }`}
            >
              <div className="flex items-center justify-between">
                <span>{option}</span>
                {hasSubmitted && index === currentQ.options.indexOf(currentQ.correct_answer) && (
                  <Check className="w-5 h-5 text-green-500" />
                )}
                {hasSubmitted && selectedAnswers[currentQuestion] === index && 
                  index !== currentQ.options.indexOf(currentQ.correct_answer) && (
                  <X className="w-5 h-5 text-red-500" />
                )}
              </div>
            </button>
          ))}
        </div>

        {/* Explanation (shown after submission) */}
        {hasSubmitted && (
          <div className={`p-4 rounded-lg ${isCorrect ? 'bg-green-50' : 'bg-red-50'}`}>
            <p className="font-medium mb-2">{isCorrect ? 'Correct!' : 'Incorrect'}</p>
            <p className="text-sm">{currentQ.explanation}</p>
          </div>
        )}
      </div>

      {/* Navigation */}
      <div className="flex justify-between items-center pt-4 border-t border-gray-200">
        <div className="flex gap-4">
          <button
            onClick={() => setCurrentQuestion(prev => Math.max(0, prev - 1))}
            disabled={currentQuestion === 0}
            className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <button
            onClick={() => setCurrentQuestion(prev => Math.min(questions.length - 1, prev + 1))}
            disabled={currentQuestion === questions.length - 1}
            className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>

        <div className="flex items-center gap-4">
          {hasSubmitted ? (
            <>
              <span className="text-sm font-medium">
                Score: {correctAnswers}/{totalQuestions}
              </span>
              <button
                onClick={resetQuiz}
                className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
              >
                <RefreshCw className="w-4 h-4" />
                Try Again
              </button>
            </>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={selectedAnswers.includes(null)}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Submit
            </button>
          )}
        </div>
      </div>
    </div>
  );
}