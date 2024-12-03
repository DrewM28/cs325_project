#Drew Milton 

import os
from huggingface_hub import InferenceClient
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

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
            with open(file_path, "r", encoding = "utf-8", errors="ignore") as file:
                return file.readlines()
        except FileNotFoundError:
            print(f"Error: {file_path} not found.")
            return []
        except Exception as e:
            print(f"Unexpected error reading {file_path}: {e}")
            return []

    def generate_responses(self, prompts, max_tokens=100):
        """
        Generate responses for the prompts using the Hugging Face model,
        ensuring the output is classified as positive, negative, or neutral.
        """
        if not prompts:
            print("No prompts available to process.")
            return []

        responses = []
        instruction = (
            "Analyze the following text and respond with 'positive', 'negative', or 'neutral' sentiment only:\n\n"
        )

        for prompt in prompts:
            response_text = ""
            try:
                # Add the instruction to the prompt
                formatted_prompt = instruction + prompt.strip()
                for message in self.client.chat_completion(
                    messages=[{"role": "user", "content": formatted_prompt}],
                    max_tokens=max_tokens,
                    stream=True,
                ):
                    response_content = message.choices[0].delta.get("content", "")
                    if response_content:
                        response_text += response_content

                # Post-process to ensure the output is valid
                response_text = response_text.strip().lower()
                if response_text not in ["positive", "negative", "neutral"]:
                    response_text = "neutral"  # Default to neutral if the response is invalid

            except Exception as e:
                print(f"Error processing prompt: {prompt.strip()} - {e}")
                response_text = "neutral"  # Default to neutral on error

            responses.append(response_text)
        return responses

    def save_responses(self, prompts, responses, output_path):
        """
        Save the generated responses to a file.
        """
        try:
            with open(output_path, "w", encoding="utf-8", errors="ignore") as file:
                for i, (prompt, response) in enumerate(zip(prompts, responses), start=1):
                    file.write(f"Response to Prompt {i}:\n")
                    file.write(f"{prompt.strip()}\n")
                    file.write(f"{response}\n\n")
            print(f"Responses saved to {output_path}")
        except Exception as e:
            print(f"Error saving responses to {output_path}: {e}")

    def process_multiple_files(self, input_files, output_files, max_tokens=100):
        """
        Process multiple input files and save responses to corresponding output files.
        """
        if len(input_files) != len(output_files):
            print("Error: Number of input files must match number of output files.")
            return

        for input_file, output_file in zip(input_files, output_files):
            print(f"Processing {input_file} -> {output_file}")
            prompts = self.read_prompts(input_file)
            responses = self.generate_responses(prompts, max_tokens=max_tokens)
            self.save_responses(prompts, responses, output_file)


def plot_sentiment_distribution(device_sentiments, output_path=None):
    """
    Create a grouped bar graph showing the sentiment distribution across devices.

    Args:
        device_sentiments (dict): A dictionary where keys are device names and values are lists of sentiment labels.
        output_path (str, optional): Path to save the plot. If None, the plot is displayed.
    """
    # Sentiment categories
    categories = ["positive", "negative", "neutral"]

    # Prepare data for plotting
    device_labels = list(device_sentiments.keys())
    sentiment_counts = [
        [Counter(device_sentiments[device]).get(category, 0) for device in device_labels]
        for category in categories
    ]

    # Bar positions
    x = np.arange(len(device_labels))
    bar_width = 0.2

    # Plot the data
    plt.figure(figsize=(10, 6))
    for i, counts in enumerate(sentiment_counts):
        plt.bar(
            x + i * bar_width,
            counts,
            width=bar_width,
            label=categories[i],  # Sentiment as the legend label
            alpha=0.7,
        )

    # Configure the plot
    plt.title("Sentiment Distribution by Device", fontsize=16)
    plt.xlabel("Devices", fontsize=14)
    plt.ylabel("Count", fontsize=14)
    plt.xticks(x + bar_width, device_labels, fontsize=12)  # X-axis labels are devices
    plt.legend(title="Sentiments", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Save or display the graph
    if output_path:
        plt.savefig(output_path, format="png")
        print(f"Grouped bar graph saved to {output_path}")
    else:
        plt.show()


if __name__ == "__main__":
    # Replace with your actual token
    token = "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"
    chat_bot = HuggingFaceChat("microsoft/Phi-3-mini-4k-instruct", token=token)

    # Input and output file lists
    input_files = ["review1.txt", "review2.txt", "review3.txt", "review4.txt"]
    output_files = ["responses1.txt", "responses2.txt", "responses3.txt", "responses4.txt"]

    # Process files
    chat_bot.process_multiple_files(input_files, output_files, max_tokens=100)

    #Device names
    device_sentiments = {
        "Apple Watch 9": ["positive", "negative", "positive"],
        "Apple Watch 10": ["negative"],
        "Apple Watch 3": ["neutral"],
        "Apple Watch SE": ["positive"]
    }

    #Function call to plot data
    plot_sentiment_distribution(device_sentiments, output_path="test_graph.png")
