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
  async sendMessage(message: string, nodeData: any) {
    try {
      const response = await axios.post('http://localhost:5000/chat-with-chunk', {
        query: message,
        node_data: nodeData
      }, {
        withCredentials: true
      });

      return response.data.response;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  async sendGlobalMessage(message: string) {
    try {
      const response = await axios.post('http://localhost:5000/chat', {
        query: message
      }, {
        withCredentials: true
      });

      return response.data.response;
    } catch (error) {
      console.error('Error sending global message:', error);
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