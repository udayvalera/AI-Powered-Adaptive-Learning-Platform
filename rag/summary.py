from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from models import Models
from prompts import SUMMARY_TEMPLATE
model = Models()
summary_model = model.summary_model


class Summary(BaseModel):
    topic: str = Field(..., description="The main topic of the chunk")
    keywords: str = Field(..., description="Keywords that describe the chunk. IMPORTANT: Return keywords as a COMMA-SEPARATED string, NOT a list.")
    summary: str = Field(..., description="A summary of the chunk in 50 words or less")

parser = PydanticOutputParser(pydantic_object=Summary)

prompt = SUMMARY_TEMPLATE.partial(
    format_instructions=parser.get_format_instructions()
)

chain = prompt | summary_model | parser

def summarize_chunk(text):
    """
    Summarize the input text and return the result as JSON.
    
    Args:
        text (str): The text to be summarized.
    
    Returns:
        dict: The summary result as a JSON object.
    """
    try:
        result = chain.invoke({"text": text})
        return result
    except Exception as e:
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    text_to_summarize = """
    textual entailment and learning task-independent sentence representations [4, 22, 23, 19].
End-to-end memory networks are based on a recurrent attention mechanism instead of sequence-
aligned recurrence and have been shown to perform well on simple-language question answering and
language modeling tasks [28].
To the best of our knowledge, however, the Transformer is the ﬁrst transduction model relying
entirely on self-attention to compute representations of its input and output without using sequence-
aligned RNNs or convolution. In the following sections, we will describe the Transformer, motivate
self-attention and discuss its advantages over models such as [14, 15] and [8].
3 Model Architecture
Most competitive neural sequence transduction models have an encoder-decoder structure [ 5,2,29].
Here, the encoder maps an input sequence of symbol representations (x1,...,x n)to a sequence
of continuous representations z= (z1,...,z n). Given z, the decoder then generates an output
    """
    summary_result = summarize_chunk(text_to_summarize)
    print(summary_result)
    print(summary_result.topic)
    print(summary_result.keywords)
    print(summary_result.summary)