from openai import OpenAI
from swarm import Swarm, Agent
import gradio as gr

# Initialize Swarm client
ollama_client = OpenAI(
    base_url="http://localhost:11434/v1",        
    api_key="ollama"            
)

# Editor Agent to edit news
code_agent = Agent(
    name="Code developer",
    instructions="Write typescript code the given secnario or function.",
    model="deepseek-coder-v2"
)

review_agent = Agent(
    name="Code Reviewer",
    instructions="Review the typescript code for the given secnario or function and rewrite the code if needed.",
    model="deepseek-coder-v2"
)

testcase_agent = Agent(
    name="unit tester",
    instructions="write the test cases for the given secnario or function.",
    model="deepseek-coder-v2"
)

with gr.Blocks() as demo:
    def run_agents(instruction, chat_history):
        message = [{"role": "user", "content": instruction}] 

        code_response = client.run(
            agent=code_agent,
            messages=message,
            debug=True,
        )
        print(code_response)
        code = code_response.messages[-1]["content"]
        message.append({"role": "user", "content": code})
        review_response = client.run(
            agent=review_agent,
            messages=message,
            debug=True,
        )

        review = review_response.messages[-1]["content"]
        message.append({"role": "user", "content": review})
        test_response = client.run(
            agent=testcase_agent,
            messages=message,
            debug=True,
        )
        
        chat_history.append((instruction, review))
        chat_history.append((None, test_response.messages[-1]["content"]))
        return chat_history

    client = Swarm(client=ollama_client)
    chatbot = gr.Chatbot()
    instruction = gr.Textbox(label="Instruction")
    send_btn = gr.Button(value="Send")
    send_btn.click(run_agents, inputs=[instruction, chatbot], outputs = [chatbot])

demo.launch(share=True)