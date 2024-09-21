#Drew Milton


#reads prompts from prompts.txt file
def read_prompts(filepath):
    with open(filepath, "r") as file:
        prompts = file.readlines()
        return prompts
        

#call the model


#pass prompts to the model
# Use a pipeline as a high-level helper
def pass_prompts():
    from transformers import pipeline

    messages = [
        {"content": prompts},
    ]
    pipe = pipeline("text-generation", model="microsoft/Phi-3-mini-128k-instruct", trust_remote_code=True)
    return pipe


#get responses and transfer them to a new txt file


def main():
    filepath = "prompts.txt"
    prompts = read_prompts(filepath)
    
    print(prompts)

    messages = pass_prompts()
    print(messages)



if __name__ == "__main__":
    main()
