# Basic-Oobabooga-Chatbot
An example of a basic chatbot with a persistent conversation list using the Oobabooga Api and Llama 2 from my youtube tutorial. (Not released as of now)

If you find this code usefull consider checking out my main Ai Assistant project: https://github.com/libraryofcelsus/Aetherius_AI_Assistant

If you want more code tutorials like this, follow me on github and youtube: https://www.youtube.com/@LibraryofCelsus

(Channel isn't launched yet, I have multiple scripts like this written, but am still working on a video production format.  Subscribe for its Launch!)

## Window's Installation
1. Install Git
2. Install Python 3.10.6, Make sure you add it to PATH
3. Install the Oobabooga Web-Ui.  This can be done with a one-click installer found on their Github page: https://github.com/oobabooga/text-generation-webui
4. Launch the Web-Ui and navigate to the sessions tab, click both Api boxes and then click apply and restart.
5. Now navigate to the models tab and enter: "TheBloke/Llama-2-7b-Chat-GPTQ" or "TheBloke/Llama-2-13B-chat-GPTQ".  (If using cpu use the GMML Version)
6. Once the model is downloaded, change the Model loader to ExLlama and set the gpu-split parameter to .5gb under your GPU's limit.  Next set the max_seq_len to 4096.
7. Open Git Bash Program
8. Run git clone: **git clone https://github.com/libraryofcelsus/Basic-Oobabooga-Chatbot**
9. Open the Command Line as admin and navigate to the project install folder with **cd <PATH TO INSTALL>**
10. Create a virtual environment: python -m venv venv
11. Activate the virtual enviornment with: .\venv\Scripts\activate
12. Install the requirements with **pip install -r requirements.txt**
13. Edit and set your username and chatbot name in the .txt files
14. Edit and set your main prompt and greeting in the .txt files
15. Run Aetherius with **python Oobabooga_chat_api.py**
 
*Note, you will need to run .\venv\Scripts\activate every time you exit the command line to reactivate the virtual enviornment.

-----

My Ai research is self-funded, consider supporting me if you find it useful :)

<a href='https://ko-fi.com/R6R2NRB0S' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi3.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

-----

# Contact
Discord: libraryofcelsus      -> Old Username Style: Celsus#0262

MEGA Chat: https://mega.nz/C!pmNmEIZQ

Email: libraryofcelsusofficial@gmail.com
