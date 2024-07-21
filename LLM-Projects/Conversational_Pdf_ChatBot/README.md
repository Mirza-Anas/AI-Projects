<H1>Conversational PDF Chatbot built on LLM model Meta-Llama-3-8B-Instruct</H1>

<h3>The Easiest way to check the running model is to visit huggingface spaces where it is live: https://huggingface.co/spaces/mirzanas/Conversation_Pdf_ChatBot</h3>

<h4>To run the model locally:
  <ol>
    <li>First clone the repository on the local computer</li>
    <li>create a new .env file in the root folder</li>
    <li>Add hugging face token in the .env file : HUGGINGFACEHUB_API_TOKEN=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 (Temporary token) or you can use your own huggingface token with access of llama-3-8B-Instruct model</li>
    <li>Open the root folder in the terminal and run: pip install -r requirements.txt</li>
    <li>After all the downloads are completed run: streamlit run app.py</li>
    <li>Wait a few second app will be live at localhost:8501</li>
  </ol>
</h4>

