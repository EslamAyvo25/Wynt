import openai
import multiprocessing
import os 

api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    print("No API is Set!\n")


MODEL = "gpt-4-mini"  # or "gpt-4-1106-preview" for the latest version

def process_gpt_4o_turbo(conn, text, agent):
    try:
        completion = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": agent},
                {"role": "user", "content": text},
            ],
            stream=True
        )


# real time part to strem but to other process this is child process 
        for chunk in completion:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if 'content' in delta:
                    conn.send(delta.content) # use con as child process and send to sream somthings to it 

        conn.send(None)  # Signal end of response and this is after send everything 


    except Exception as e:
        conn.send(f"Error: {str(e)}")
        conn.send(None) # we have to kill this process any way 



# main to use it in the main code with other classes or main function 
def main():
    parent_conn, child_conn = multiprocessing.Pipe() # read and write to anf from 
    
    # Example usage
    agent = "You are a helpful assistant."
    text = "Tell me a short joke."

    process = multiprocessing.Process(target=process_gpt_4o_turbo, args=(child_conn, text, agent))
    process.start()

    # Read from the pipe
    while True:
        chunk = parent_conn.recv() # the child process get the data streaming and the parent rec the data from the child then print it to the user 
        if chunk is None:
            break
        print(chunk, end='', flush=True) ## 

    process.join()

if __name__ == "__main__":
    main()