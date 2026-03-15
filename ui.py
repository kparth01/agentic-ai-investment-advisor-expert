import gradio as gr
from graph import app as agent_graph
from fastapi import FastAPI
from gradio.routes import mount_gradio_app

def chat(message, history):
    result = agent_graph.invoke({"user_input": message})
    return result["aggregator_agent"]


demo = gr.ChatInterface(
    fn=chat,
    title="💬 Investment Advisor Agent",
    textbox=gr.Textbox(placeholder="Ask about investments...")
)
# .launch()

app = FastAPI()

app = mount_gradio_app(app, demo, path="/")