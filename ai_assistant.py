import speech_recognition as sr
import os
from openai import OpenAI
from io import BytesIO
import openai                 
from datetime import datetime
import base64                  # for decoding images if recieved in the reply
import requests                # for downloading images from URLs
from PIL import Image, ImageTk # pillow, for processing image types
import tkinter as tk           # for GUI thumbnails of what we got
from win32com.client import Dispatch
import webbrowser

chatstr = ""

# usecase - to talk with ai if not in selceted prompt
def chat(prompt):
    global chatstr
    chatstr+=f"User:{prompt} \nJarvis: "
    client = OpenAI(
    api_key="paste your API key here or make it enviornment variable"
    #you can get you api key throug openai website for learning you can go yt - https://youtu.be/nafDyRsVnXU?si=2SBbGT8IAflHL6Hg
    )
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
     
        {
            "role": "assistant",
            "content": chatstr,
        },
    ],
    )

    try:
        xy= response.model_dump()['choices'][0]['message']['content']
        print(chatstr)
        say(xy)
        chatstr+=xy+"\n"
        return xy
    except Exception as e:
        print("Jarvis could not understand what you said. Please try again")
# for text to voice;        
def say(text):
    speak = Dispatch("SAPI.SpVoice").Speak
    speak(f"{text}")

# for using this func say using artificial intelligence 
def ai(prompt):
    print(f"Prompt to AI: {prompt}")

    client = OpenAI(
    api_key="paste your API key here or make it enviornment variable"
    #you can get you api key throug openai website for learning you can go yt - https://youtu.be/nafDyRsVnXU?si=2SBbGT8IAflHL6Hg
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
     
        {
            "role": "assistant",
            "content": prompt,
        },
    ],
    )
    print("OpenAI Response:")
    xy= completion.model_dump()['choices'][0]['message']['content']
    print(xy)
    say(xy)
    #below step is to store data history in ai
    if not os.path.exists("openai"):
        os.mkdir("openai")
    with open(f"openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt","w") as f:
        f.write(xy)
        
# used DALLE module for creating image through prompt sat draw in prompt to use this function        
def draw(prompt):

    client = OpenAI(
        api_key="paste your API key here or make it enviornment variable"
    #you can get you api key throug openai website for learning you can go yt - https://youtu.be/nafDyRsVnXU?si=2SBbGT8IAflHL6Hg
        
    )  
    image_params = {
        "model": "dall-e-2",  
        "n": 1,               
        "size": "1024x1024",  # 256x256, 512x512 only for DALL-E 2 - not much cheaper
        "prompt": prompt,     # DALL-E 3: max 4000 characters, DALL-E 2: max 1000
        "user": "myName",     # pass a customer ID to OpenAI for abuse monitoring
    }

    image_params.update({"response_format": "b64_json"}) 
    try:
        images_response = client.images.generate(**image_params)
    except openai.APIConnectionError as e:
        print(f"Server connection error: {e.__cause__}")  # from httpx.
        raise
    except openai.RateLimitError as e:
        print(f"OpenAI RATE LIMIT error {e.status_code}: (e.response)")
        raise
    except openai.APIStatusError as e:
        print(f"OpenAI STATUS error {e.status_code}: (e.response)")
        raise
    except openai.BadRequestError as e:
        print(f"OpenAI BAD REQUEST error {e.status_code}: (e.response)")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

    # make a file name prefix from date-time of response
    images_dt = datetime.utcfromtimestamp(images_response.created)
    img_filename = images_dt.strftime('DALLE-%Y%m%d_%H%M%S')  # like 'DALLE-20231111_144356'

    # get the prompt used if rewritten by dall-e-3, null if unchanged by AI
    revised_prompt = images_response.data[0].revised_prompt

    # get out all the images in API return, whether url or base64
    # note the use of pydantic "model.data" style reference and its model_dump() method
    image_url_list = []
    image_data_list = []
    for image in images_response.data:
        image_url_list.append(image.model_dump()["url"])
        image_data_list.append(image.model_dump()["b64_json"])

    # Initialize an empty list to store the Image objects
    image_objects = []

    # Check whether lists contain urls that must be downloaded or b64_json images
    if image_url_list and all(image_url_list):
        # Download images from the urls
        for i, url in enumerate(image_url_list):
            while True:
                try:
                    print(f"getting URL: {url}")
                    response = requests.get(url)
                    response.raise_for_status()  # Raises stored HTTPError, if one occurred.
                except requests.HTTPError as e:
                    print(f"Failed to download image from {url}. Error: {e.response.status_code}")
                    retry = input("Retry? (y/n): ")  # ask script user if image url is bad
                    if retry.lower() in ["n", "no"]:  # could wait a bit if not ready
                        raise
                    else:
                        continue
                    break
                image_objects.append(Image.open(BytesIO(response.content)))  # Append the Image object to the list
                image_objects[i].save(f"{img_filename}_{i}.png")
                print(f"{img_filename}_{i}.png was saved")
    elif image_data_list and all(image_data_list):  # if there is b64 data
        # Convert "b64_json" data to png file
        for i, data in enumerate(image_data_list):
            image_objects.append(Image.open(BytesIO(base64.b64decode(data))))  # Append the Image object to the list
            image_objects[i].save(f"{img_filename}_{i}.png")
            print(f"{img_filename}_{i}.png was saved")
    else:
        print("No image data was obtained. Maybe bad code?")

    ## -- extra fun: pop up some thumbnails in your GUI if you want to see what was saved

    if image_objects:
        # Create a new window for each image
        for i, img in enumerate(image_objects):
            # Resize image if necessary
            if img.width > 512 or img.height > 512:
                img.thumbnail((512, 512))  # Resize while keeping aspect ratio

            # Create a new tkinter window
            window = tk.Tk()
            window.title(f"Image {i}")

            # Convert PIL Image object to PhotoImage object
            tk_image = ImageTk.PhotoImage(img)

            # Create a label and add the image to it
            label = tk.Label(window, image=tk_image)
            label.pack()

            # Run the tkinter main loop - this will block the script until images are closed
            window.mainloop()

#take order from user in form of voice command
def takeorder():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = .8
        voice = r.listen(source)
        try:
          print("Recognizing")  
          query = r.recognize_google(voice,  language= "en-in")
          print(f"User said: {query}")
          return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"
    
if __name__ == '__main__':
    x = " Namstey Sir "
    say(x)
    while True:
            print("Listening...")
            query = takeorder()
            if "open" in query.lower():
              webbrowser.open(f"https://{query[5:]}.com")
            elif "start" in query.lower ():
                #this is program locations that i want to open you can change the location
                os.system(f'start "" "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\{query[6:]}.lnk"')
            elif "the time" in query.lower():
                a = datetime.now().strftime("%H:%M:%S")  
                say(a)    
            elif "using artificial intelligence".lower() in query.lower():
                ai(prompt=query)
            elif "Draw".lower() in query.lower():
                draw(prompt=query) 
            elif "jarvis exit".lower() in query.lower():
                exit() 
            else:
                chat(prompt=query)        
            print(f"user said {query}")
                
