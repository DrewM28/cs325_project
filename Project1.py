#Drew Milton

#reads prompts from prompts.txt file
def read_prompts(filepath):
    with open("prompts.txt", "r") as file:
        prompts = file.readlines()
        return prompts
        

#call the model


#pass prompts to the model


#get responses and transfer them to a new txt file


def main():
    filepath = "prompts.txt"
    prompts = read_prompts(filepath)
    
    print(prompts)



if __name__ == "__main__":
    main()

