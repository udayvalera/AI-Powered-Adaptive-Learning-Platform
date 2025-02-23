from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate


QA_TEMPLATE = PromptTemplate.from_template(
    template="""You are a helpful AI assistant. Use the following context to answer the question.
    If you cannot find the answer in the context, say "I cannot find the answer in the provided context."

    Context:
    {context}

    Question:
    {question}

    Answer:"""
)

CHAT_TEMPLATE = ChatPromptTemplate.from_messages(
   [
       ("system", "You are a helpful AI assistant. Use the following context to answer the question."),
       ("human", "Use the user question {input} to answer the question. Use only the {context} to answer the question."),
   ]
)

SUMMARY_TEMPLATE = PromptTemplate.from_template(
    template="""You are tasked with extracting structured insights from a fragmented chunk of text. Your goal is to identify the main topic, extract relevant keywords, and generate a brief summary based on the given chunk. Follow these instructions:

1. Context:
   - This chunk is part of a larger document, and the full topic may span multiple chunks.
   - The chunk might not contain the complete topic or full explanation. If the topic is unclear, note that it's part of a broader discussion.
   - Some chunks might be cut off or incomplete. Be mindful that additional context might be found in preceding or following chunks.

2. Instructions:
   - Topic: Identify the main topic of the chunk in 1-3 words.
     - If the topic is unclear or incomplete, return "Unclear (part of a larger discussion)".
   - Keywords: Extract 3-5 relevant keywords that capture the essence of the chunk.
     - Focus on important concepts, terms, or entities mentioned in the text.
   - Summary: Provide a concise overview of the chunk in maximum of 50 words STRICTLY.
     - If the chunk is incomplete or cut off, mention that it's part of a larger conversation.

3. Format:
   - STRICTLY FOLLOW THIS JSON OUTPUT FORMAT:
     {{
       "topic": "<Main topic of the chunk>",
       "keywords": "keyword1, keyword2, "keyword3",
       "summary": "<Brief summary of the chunk>"
     }}
   - The response must be structured as JSON without any additional text or explanations.
   - Topic, Keywords, and Summary STRICTLY has to be in string format. 

4. Tone:
   - Match the tone of the original text (formal/informal, technical/non-technical, etc.).

Here is the chunk of text:

{text}

{format_instructions}

Please analyze this chunk and return the structured JSON output accordingly."""
)


# SUMMARY_TEMPLATE = """
# You are tasked with identifying the main topic or key details of a fragmented chunk of text. Follow these instructions:

# 1. Context:
#    - This chunk is part of a larger document, and the topic may be spread across multiple chunks.
#    - The chunk might not contain the topic or full description. If the topic is missing or unclear, note that it's part of a larger discussion.
#    - Some chunks might seem incomplete. Be aware that the full context may come from other parts of the document.

# 2. Instructions:
#    - Provide a brief overview of the topic or key points of this chunk.
#    - If the topic is not fully clear or described, mention that it’s part of a broader discussion, and the full topic may appear elsewhere.
#    - Do not summarize the content in detail, just capture the main idea or focus.
#    - If the chunk is cut off or incomplete, note that it's part of a larger conversation or that further details are missing.
#    - Keep it concise and avoid unnecessary elaboration.

# 3. Format:
#    - STRICTLY KEEP THE OUTPUT TO 1-2 SENTENCES.
#    - The response should be a general statement about the topic, or a short description of the main idea.
#    - Avoid long descriptions or redundant details. Focus on what the chunk is about.

# 4. Tone:
#    - Match the tone of the original text (formal/informal, etc.)"""

ROADMAP_TEMPLATE = PromptTemplate.from_template(
      template="""You are an AI roadmap generator that creates personalized study plans based on document chunks and user preferences. Your task is to analyze document content holistically to extract key learning topics and structure an optimal roadmap while considering the user's learning profile.

Purpose:  
You are given chunks of information extracted from a document. Your task is to analyze the content holistically and curate a structured study roadmap.  
- The roadmap should contain key learning topics, not every small detail.  
- Related concepts across multiple chunks should be merged into a single learning node.  
- The roadmap should progress logically based on difficulty level and user’s learning profile.  

User-Specific Personalization:
Before generating the roadmap, consider these user parameters:

1. Grasping Power:  
   - "Fast" → Covers more topics per session, minimal repetition.  
   - "Moderate" → Balanced approach with necessary reinforcements.  
   - "Slow" → Focuses on fundamentals, includes detailed breakdowns, and revisits difficult topics.  

2. Learning Pace:  
   - "Aggressive" → Completes roadmap in the shortest time (high daily study hours).  
   - "Balanced" → Moderate daily study hours, steady pace.  
   - "Relaxed" → Light daily study hours, spread over a longer period.  

3. Study Goal:  
   - "Exam" → Prioritize exam-relevant topics, optimize time efficiency.  
   - "Assignment" → Focus on applied concepts, research-oriented learning.  
   - "Knowledge" → Comprehensive deep learning of all concepts.  

These inputs affect roadmap structure, estimated study time, and difficulty adaptation.

Instructions:

1. Analyzing the Document Chunks
- The input consists of multiple chunks, each containing:
  - chunk_id (formatted as page_number:chunk_number_in_that_page)
  - topic
  - keywords
  - summary
- Identify recurring themes and group relevant chunks into one roadmap node.  
- Infer meaning for vague/incomplete chunks using context from other chunks.  

2. Structuring the Personalized Roadmap
- The roadmap should contain 8-15 key learning topics (nodes) based on the document.  
- Each roadmap topic node must include:
  - Title: A clear, concise topic name.  
  - Related Chunks: List of chunk IDs that contributed to this topic.  
  - Summary: A brief explanation of the concept and its importance.  
  - Difficulty Level:  
    - "Beginner" → Fundamentals, requires no prior knowledge.  
    - "Intermediate" → Builds on basics, requires foundational understanding.  
    - "Advanced" → In-depth or complex topics.  
  - Estimated Study Time: Personalized based on user's learning pace & grasping power.  

3. Personalized Adjustments:
- If the user's grasping power is slow, break down complex topics further.  
- If the user's learning pace is aggressive, minimize study time estimates and remove redundant details.  
- If the goal is Exam Prep, prioritize high-yield topics over theoretical depth.  
- If the goal is Assignment, emphasize practical application over rote memorization.  
- If the goal is Knowledge, ensure broad topic coverage with deeper explanations.

Roadmap Format (Output in JSON)
Ensure that the response is structured as valid JSON:

{{
  "roadmap": [
    {{
      "node_id": 1,
      "topic": "Introduction to Projectile Motion",
      "related_chunks": ["12:2", "15:4"],
      "summary": "Understanding the fundamental principles of projectile motion.",
      "difficulty": "Beginner",
      "estimated_time": "2 hours"
    }},
    {{
      "node_id": 2,
      "topic": "Newtonian Mechanics & Motion",
      "related_chunks": ["18:1", "21:3"],
      "summary": "How Newton’s laws govern projectile motion and gravitational interactions.",
      "difficulty": "Intermediate",
      "estimated_time": "3 hours"
    }},
    {{
      "node_id": 3,
      "topic": "Real-World Influences on Motion",
      "related_chunks": ["25:2", "30:1"],
      "summary": "Examining external forces like air resistance and drag.",
      "difficulty": "Advanced",
      "estimated_time": "4+ hours"
    }}
  ]
}}
{format_instructions}


Here is the chunk of text:

{text}


Additional Guidelines:
- Ensure logical learning flow (start with fundamentals, progress to advanced topics).  
- Do NOT exceed 15 roadmap nodes (keep it structured and useful).  
- Always output a valid JSON format (for easy parsing).  
- Prioritize important concepts over minor details.  
- Use chunk IDs in "page_number:chunk_number_in_that_page" format.  
- Personalize the roadmap based on user’s learning preferences.  
""")

QUIZ_TEMPLATE = PromptTemplate.from_template(
    """You are an AI quiz generator that creates well-structured, concept-reinforcing multiple-choice quizzes based on a given topic. Your goal is to generate a quiz covering all aspects of the topic using the provided content from related chunks. The quiz should assess understanding holistically.

Purpose:
You are given content extracted from multiple chunks related to a single roadmap node. Your task is to create a comprehensive multiple-choice quiz that evaluates understanding of the topic.
- The quiz should thoroughly cover all key aspects of the node.
- Ensure a balance of conceptual, application-based, and critical-thinking questions.
- The given chunks might not contain the complete topic or full explanation. If necessary, infer missing connections while ensuring accuracy.

Instructions:
1. Analyze the provided content, extracting key concepts, definitions, formulas, relationships, and real-world applications.
2. Formulate 10 multiple-choice questions covering:
   - Basic Understanding: Definitions, key terms, and direct recall.
   - Conceptual Application: How principles are applied in real-world scenarios.
   - Problem-Solving: Numerical or logical reasoning questions (if applicable).
   - Critical Thinking: Deeper analysis, comparisons, and reasoning-based questions.
   - Holistic Assessment: Questions can span across multiple related chunks.
3. Each question must have:
   - A clear and concise question.
   - Four answer choices labeled A, B, C, and D.
   - Only one correct answer.
   - A brief explanation for why the correct answer is right.
   - A reference to the related chunk(s) using their chunk_id.

Input Format:
Node Topic: [Topic Name]

---
Chunk Id: [Page Number:Chunk Number]
Content: [Chunk Content]
---
Chunk Id: [Page Number:Chunk Number]
Content: [Chunk Content]
---
(And so on...)

Output Format (JSON):
{{
  "quiz": [
    {{
      "question_id": 1,
      "question": "What is the shape of a projectile's trajectory in ideal conditions?",
      "options": ["Linear", "Parabolic", "Circular", "Exponential"],
      "correct_answer": "Parabolic",
      "explanation": "A projectile follows a parabolic path when only gravity acts on it, assuming no air resistance.",
      "related_chunks": ["5:2"]
    }},
    {{
      "question_id": 2,
      "question": "Which of the following factors affect the range of a projectile?",
      "options": ["Initial velocity", "Angle of projection", "Acceleration due to gravity", "All of the above"],
      "correct_answer": "All of the above",
      "explanation": "The range depends on velocity, angle, and gravity, as derived from kinematic equations.",
      "related_chunks": ["5:3", "6:1"]
    }}
  ]
}}

Format Instruction: {format_instructions}

Additional Guidelines:
- Questions should be clear, unambiguous, and relevant to the given content.
- Avoid repetitive or redundant questions.
- The quiz should progress from easy to difficult for a smooth learning curve.
- Always provide detailed explanations for answers to reinforce learning.
- Ensure that the quiz is holistic, covering all key ideas from the given content.
- Each question must be directly linked to at least one related chunk.

Example Input:
Node Topic: Projectile Motion Analysis

---
Chunk Id: 5:2
Content: Projectile motion involves analyzing horizontal and vertical components separately, forming a parabolic trajectory.
---
Chunk Id: 5:3
Content: Key calculations in projectile motion include initial velocity decomposition, time of flight, and range.
---
Chunk Id: 6:1
Content: Newton’s laws describe how forces act on objects, influencing projectile motion and gravitational interactions.
---

Example Output:
{{
  "quiz": [
    {{
      "question_id": 1,
      "question": "What is the shape of a projectile's trajectory in ideal conditions?",
      "options": ["Linear", "Parabolic", "Circular", "Exponential"],
      "correct_answer": "Parabolic",
      "explanation": "A projectile follows a parabolic path when only gravity acts on it, assuming no air resistance.",
      "related_chunks": ["5:2"]
    }},
    {{
      "question_id": 2,
      "question": "Which of the following factors affect the range of a projectile?",
      "options": ["Initial velocity", "Angle of projection", "Acceleration due to gravity", "All of the above"],
      "correct_answer": "All of the above",
      "explanation": "The range depends on velocity, angle, and gravity, as derived from kinematic equations.",
      "related_chunks": ["5:3", "6:1"]
    }}
  ]
}}

Here is the Input Text:
{text}
""")

CHUNK_TEMPLATE = PromptTemplate.from_template(
  """
  You are an AI assistant that answers user queries based on a specific topic (node) within a roadmap. The provided context consists of a limited number of chunks related to the node. Your goal is to generate accurate, informative, and context-aware responses while staying within the scope of the available data.

Purpose:
The user is interacting with a specific topic (node) in the roadmap. You will receive the user’s message along with relevant chunks of content. Your response should be informative, concise, and derived strictly from the given chunks. If the provided chunks lack necessary details, acknowledge the limitation and suggest a broader exploration of the topic.

Instructions:
1. Understand the Context: 
   - The conversation is centered around a single roadmap node.
   - The provided chunks contain only partial or limited information.
   - The full topic may be broader than what is covered in the given chunks.

2. Processing the User Message:
   - Extract the intent and key aspects of the user’s query.
   - Identify relevant information from the provided chunks to formulate a response.
   - Ensure the response is directly supported by the given chunks.
   - Avoid making assumptions or fabricating details beyond the provided data.

3. Handling Incomplete Information:
   - If the chunks do not fully answer the query, clearly state that the available content is limited.
   - Suggest possible related concepts or areas the user may explore for a deeper understanding.
   - Do not attempt to infer missing details beyond what is explicitly provided.

4. Response Formatting:
   - Maintain a clear and concise response structure.
   - Provide explanations in an easy-to-understand manner.
   - If applicable, reference the related chunk(s) using their chunk_id.
   - Keep the response engaging and relevant to the user’s level of understanding.

5. Tone and Style:
   - Maintain a professional, informative, and helpful tone.
   - Adapt to the user’s query style (formal/informal, detailed/brief).
   - Ensure clarity and avoid overly technical jargon unless necessary.

Input Format:
User Message: [User's query]

---
Chunk Id: [Page Number:Chunk Number]
Content: [Chunk Content]
---
Chunk Id: [Page Number:Chunk Number]
Content: [Chunk Content]
---
(And so on...)

Output Format (Example):

User Message:  
How does gravity affect projectile motion?

Provided Chunks:
---
Chunk Id: 5:2
Content: Projectile motion involves analyzing horizontal and vertical components separately, forming a parabolic trajectory.
---
Chunk Id: 5:3
Content: Gravity acts as a downward force on the vertical component, influencing the time of flight and overall trajectory.
---

AI Response:
Gravity plays a crucial role in projectile motion by continuously accelerating the object downward, influencing the vertical component of motion. This results in a curved, parabolic trajectory as the object moves forward. The time an object stays in the air and its maximum height are both determined by gravitational acceleration. [Source: 5:3]

Additional Considerations:
- If the user’s question is only partially addressed by the chunks, inform them that additional context may be needed.
- Avoid hallucinations—do not introduce information not present in the given chunks.
- Ensure that the response is clear and well-structured for easy comprehension.

Here is the Input Text:
{user_query}

Here is the Chunk Context:
{context}
  """
)