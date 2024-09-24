#using hugging face connects to AI using API
from huggingface_hub import InferenceClient


#reads the prompts in from the prompts text file
with open("prompts.txt", "r") as file: #with open, opens prompts.txt and r means to read in the prompts
    prompts = file.readlines() #file.readlines reads the prompts in the file and stores it in prompts

#calls Phi-3 with a token
#got this from hugging face
client = InferenceClient(
    "microsoft/Phi-3-mini-4k-instruct",
    token="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",
)

#gets the responses and outputs them in the terminal
responses = [] #stores responses into a list
for prompt in prompts[:3]: #shows only the first 3 prompts

    for message in client.chat_completion(
	    messages=[{"role": "user", "content": prompt}],
	    max_tokens=100, 
	    stream=True,
):
        #this is what gets the responses from phi-3
        response_content = message.choices[0].delta.get("content", "")
        if response_content:
            responses.append(response_content)
        #print(message.choices[0].delta.content, end="") #optional print statement to make sure code was working



#sends the responses to the responses text file
with open("responses.txt", "w") as response_file: #with open, opens the responses.txt file and w means to write to it
    response = ''.join(responses) #turns the list of responses into a string called response
    response_file.write(f"Response to Prompt: \n") #these write to the responses.txt file
    response_file.write(response + "\n\n")