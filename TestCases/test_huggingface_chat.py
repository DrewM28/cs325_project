#Test Case 1
import pytest
from huggingface_hub import InferenceClient
from main_script import HuggingFaceChat  # Replace `main_script` with the name of your Python file

def test_initialization():
    with pytest.raises(ValueError, match="API token is required"):
        HuggingFaceChat("model_name", token=None)
    
    chat_bot = HuggingFaceChat("model_name", token="dummy_token")
    assert chat_bot.model_name == "model_name"
    assert isinstance(chat_bot.client, InferenceClient)

#Test Case 2
import os

def test_read_prompts(tmp_path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("This is a test prompt.\nAnother prompt here.")

    chat_bot = HuggingFaceChat("model_name", token="dummy_token")
    
    # Valid file
    prompts = chat_bot.read_prompts(test_file)
    assert len(prompts) == 2
    assert prompts[0].strip() == "This is a test prompt."

    # Non-existent file
    prompts = chat_bot.read_prompts("non_existent_file.txt")
    assert prompts == []

#Test Case 3
def test_generate_responses(mocker):
    mocker.patch.object(
        InferenceClient, "chat_completion",
        return_value=[{"choices": [{"delta": {"content": "positive"}}]}]
    )

    chat_bot = HuggingFaceChat("model_name", token="dummy_token")
    prompts = ["This is a positive review.", "This is a negative review."]
    responses = chat_bot.generate_responses(prompts)
    
    assert len(responses) == 2
    assert responses == ["positive", "positive"]

#Test Case 4
import matplotlib.pyplot as plt

def test_plot_sentiment_distribution(tmp_path):
    device_sentiments = {
        "Device A": ["positive", "positive", "neutral"],
        "Device B": ["negative", "negative", "neutral"],
        "Device C": ["positive", "neutral", "neutral"],
    }
    output_path = tmp_path / "test_graph.png"

    plot_sentiment_distribution(device_sentiments, output_path=str(output_path))
    assert output_path.exists()

    # Clean up plot
    plt.close()
