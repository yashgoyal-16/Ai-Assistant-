  <h1>Jarvis - Your Personal Assistant</h1>

  <p>Jarvis is a simple personal assistant script developed in Python that leverages the power of OpenAI's GPT-3.5 Turbo
    and DALL-E models. It allows users to interact with AI through voice commands, opening websites, starting programs,
    checking the time, having a chat, and even generating images based on prompts.</p>

  <h2>Getting Started</h2>

  <p>To use Jarvis, you'll need an API key from OpenAI. You can obtain one by following the instructions in this <a
      href="https://youtu.be/nafDyRsVnXU?si=2SBbGT8IAflHL6Hg" target="_blank">YouTube tutorial</a>. Once you have the API
    key, replace the placeholder in the code with your actual API key.</p>

  <h3>Prerequisites</h3>

  <ul>
    <li>Python 3.x</li>
    <li>SpeechRecognition library</li>
    <li>OpenAI library</li>
    <li>PIL (Pillow) library</li>
    <li>Tkinter library</li>
    <li>win32com.client library</li>
    <li>Requests library</li>
  </ul>

  <p>Install the required libraries using:</p>

  <pre>
    <code>pip install SpeechRecognition
pip install openai
pip install Pillow
pip install tk
pip install pypiwin32
pip install requests
    </code>
  </pre>

  <h2>Usage</h2>

  <ol>
    <li>Run the script in a Python environment.</li>
    <li>Jarvis will greet you with a welcome message.</li>
    <li>Start giving voice commands.</li>
  </ol>

  <h3>Available Commands</h3>

  <ul>
    <li><strong>Open [website]</strong> - Opens the specified website.</li>
    <li><strong>Start [program]</strong> - Starts the specified program.</li>
    <li><strong>What's the time?</strong> - Tells you the current time.</li>
    <li><strong>Using artificial intelligence</strong> - Engages in a conversation using OpenAI GPT-3.5 Turbo.</li>
    <li><strong>Draw [prompt]</strong> - Generates an image based on the given prompt using OpenAI DALL-E.</li>
    <li><strong>Jarvis exit</strong> - Exits the script.</li>
  </ul>

  <h2>Additional Notes</h2>

  <ul>
    <li>Ensure you have a stable internet connection for interacting with OpenAI APIs.</li>
    <li>The script saves AI conversation history in the "openai" directory.</li>
  </ul>

  <p>Feel free to modify and customize the script according to your needs. Enjoy using Jarvis!</p>

  <p><strong>Note:</strong> This script is for educational purposes only, and it's essential to comply with OpenAI's
    usage policies.</p>
