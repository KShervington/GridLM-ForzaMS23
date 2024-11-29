from questeval.questeval_metric import QuestEval
import os

# Initialize the metric (English is the default language)
questeval = QuestEval(no_cuda=False)  # Set `no_cuda=True` if you don't have a GPU

# Define source and hypothesis texts
sources = []
hypothesis = []

path_to_llm_outputs = os.path.join(os.getcwd(), "src", "experiments", "llm_outputs")

# Model responses to compare (names of the folders in llm_outputs/ folder)
model_1 = "gpt-4o-mini-2024-07-18"
model_2 = "llama_3-2_3b_instruct"

# Add source and hypothesis texts from files in llm_outputs/ folder
for i in range(4):
    source_file = f"llm_assessment_{i}.md"
    hypothesis_file = f"llm_assessment_{i+4}.md"

    source_file_path = os.path.join(path_to_llm_outputs, model_1, source_file)
    hypothesis_file_path = os.path.join(path_to_llm_outputs, model_2, hypothesis_file)

    try:
        with open(source_file_path, "r") as f:
            # Read the file
            data = f.read()

            sources.append(data)
            
            f.close()

        with open(hypothesis_file_path, "r") as f:
            # Read the file
            data = f.read()

            hypothesis.append(data)
            
            f.close()
    except Exception as e:
        print(f"Error reading LLM response from file\n{e}")

# Compute similarity score
score = questeval.corpus_questeval(sources=sources, hypothesis=hypothesis)

# Display the result
print(f"Similarity Score: {score}")
