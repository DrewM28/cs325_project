#Drew Milton 

import os
from huggingface_hub import InferenceClient

class HuggingFaceChat:
    def __init__(self, model_name, token=None):
        """
        Initialize the HuggingFaceChat class with model details and API token.
        """
        self.model_name = model_name
        self.token = token or os.getenv("HUGGINGFACE_API_TOKEN")
        if not self.token:
            raise ValueError("API token is required. Set it as an environment variable or pass it explicitly.")
        self.client = InferenceClient(self.model_name, token=self.token)

    def read_prompts(self, file_path):
        """
        Read prompts from a file.
        """
        try:
            with open(file_path, "r") as file:
                self.prompts = file.readlines()
        except FileNotFoundError:
            print(f"Error: {file_path} not found.")
            self.prompts = []
        except Exception as e:
            print(f"Unexpected error reading prompts: {e}")
            self.prompts = []

    def generate_responses(self, max_tokens=100, prompt_limit=10):
        """
        Generate responses for the prompts using the Hugging Face model.
        """
        if not hasattr(self, "prompts") or not self.prompts:
            print("No prompts available to process.")
            return []

        responses = []
        instruction = (
            "Analyze the following text and respond with 'positive', 'negative', or 'neutral' sentiment only: \n\n"
        )
        for prompt in self.prompts[:prompt_limit]:
            response_text = ""
            try:
                formatted_prompt = instruction + prompt.strip()
                for message in self.client.chat_completion(
                    messages=[{"role": "user", "content": formatted_prompt}],
                    max_tokens=max_tokens,
                    stream=True,
                ):
                    response_content = message.choices[0].delta.get("content", "")
                    if response_content:
                        response_text += response_content
                response_text = response_text.strip().lower()
                if response_text not in ["positive", "negative", "neutral"]:
                    response_text = "neutral" #defaults the response to neutral if the response is invalid

            except Exception as e:
                print(f"Error processing prompt: {prompt.strip()} - {e}")
                continue

            responses.append(response_text)
        self.responses = responses
        return responses

    def save_responses(self, output_path):
        """
        Save the generated responses to a file.
        """
        if not hasattr(self, "responses") or not self.responses:
            print("No responses available to save.")
            return

        try:
            with open(output_path, "w") as file:
                for i, (prompt, response) in enumerate(zip(self.prompts, self.responses), start=1):
                    file.write(f"Response to Prompt {i}:\n")
                    file.write(f"{prompt.strip()}\n")
                    file.write(f"{response}\n\n")
            print(f"Responses saved to {output_path}")
        except Exception as e:
            print(f"Error saving responses: {e}")

# Example usage
if __name__ == "__main__":
    # Replace with your actual token
    token = "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"
    chat_bot = HuggingFaceChat("microsoft/Phi-3-mini-4k-instruct", token=token)

    # File paths
    prompt_file = "prompts.txt"
    response_file = "responses.txt"

    # Process and save responses
    chat_bot.read_prompts(prompt_file)
    chat_bot.generate_responses(max_tokens=200, prompt_limit=3)
    chat_bot.save_responses(response_file)
