import axios from 'axios';

// Create an axios instance with default config
const api = axios.create({
  baseURL: 'https://api.openai.com/v1',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`
  }
});

export const chatService = {
  async sendMessage(message: string) {
    try {
      const response = await api.post('/chat/completions', {
        model: "gpt-3.5-turbo",
        messages: [
          {
            role: "system",
            content: "You are a helpful educational assistant that provides clear, concise explanations with examples."
          },
          {
            role: "user",
            content: message
          }
        ],
        temperature: 0.7,
        max_tokens: 500
      });

      return response.data.choices[0].message.content;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }
};

export const documentService = {
  async processDocument(file: File) {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('http://localhost:5000/ingest', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        withCredentials: true
      });

      return response.data;
    } catch (error) {
      console.error('Error processing document:', error);
      throw error;
    }
  }
};

export const roadmapService = {
  async getRoadmap() {
    try {
      const response = await axios.get('http://localhost:5000/roadmap', {
        withCredentials: true
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching roadmap:', error);
      throw error;
    }
  }
};

export const quizService = {
  async getQuiz(nodeData: any) {
    try {
      const response = await axios.post('http://localhost:5000/quiz', nodeData, {
        withCredentials: true
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching quiz:', error);
      throw error;
    }
  }
};