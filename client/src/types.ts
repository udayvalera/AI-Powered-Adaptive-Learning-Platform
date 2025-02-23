export interface RoadmapNode {
  node_id: number;
  topic: string;
  related_chunks: string[];
  summary: string;
  difficulty: "Beginner" | "Intermediate" | "Advanced";
  estimated_time: string;
  quiz?: {
    questions: {
      question: string;
      options: string[];
      correct: number;
    }[];
  };
}

export interface Roadmap {
  roadmap: RoadmapNode[];
}