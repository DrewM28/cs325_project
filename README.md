Drew Milton
Project 1
CS 325

Using phi-3 mini to pass along three prompts and get the responses from the sLLM and put them into a new txt file

First step I imported the hugging face inference client to call Phi-3. The second step was reading in the prompts from my prompts.txt file. I used a with open on my prompts.txt file and r to just read the file. I then use a prompts variable to store the results I get from using file.readlines() which reads everything. The third step is to call Phi-3. I did this using hugging face and got the code using an inference API. It then stores the responses into a list. I set it only have max tokens of 100. Response_content then get the responses so that they can append to each other and make a solid sentence. My final step is to open my new response file and use a w to write to the file. i use a ''.join(responses) because my to turn the responses from the list into a string to write them to the file.