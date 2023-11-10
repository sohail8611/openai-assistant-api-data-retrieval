from openai import OpenAI
import json
import time
client = OpenAI()




theUserInput = """
hi, do you have file called space.pdf? can you tell me what it have?
"""
# userinputfile = 'space.pdf'
userinputfile = ''


theUser = "sohail"  #Make sure this username exist in user.json file, and remove any thread that is assigned if you want a new thread to be assigned to user.
assistantId = "<Your Assistant ID here>"



if userinputfile:
    user_uploaded_file = client.files.create(
    file=open(userinputfile, "rb"),
    purpose='assistants'
    )
# Read the contents of the user.json file
with open('user.json', 'r') as file:
    user_data = json.load(file)



for i in user_data:
    if i['username'] == theUser and len(i['thread'])<1:
        thread = client.beta.threads.create()
        i['thread'] = thread.id
        with open('user.json', 'w') as file:
            json.dump(user_data, file, indent=4)
        break



with open('user.json', 'r') as file:
    user_data = json.load(file)

activeUserThreadId = ""
for i in user_data:
    if i['username'] == theUser:
        activeUserThreadId = i['thread']

if userinputfile:
    message = client.beta.threads.messages.create(
    thread_id=activeUserThreadId,
    role="user",
    content=theUserInput + "\nPlease read the attached file and help me out.." + userinputfile,
    file_ids=[user_uploaded_file.id]
    )
    
else:
    message = client.beta.threads.messages.create(
        thread_id=activeUserThreadId,
        role="user",
        content=theUserInput
    )


run = client.beta.threads.runs.create(
  thread_id=activeUserThreadId,
  assistant_id=assistantId,
  instructions=f"Please be humble."
)
# print(run)
while True:
    time.sleep(2)
    run = client.beta.threads.runs.retrieve(
    thread_id=activeUserThreadId,
    run_id=run.id
    )
    if run.status =='completed':
        break
    else:
        pass

messages = client.beta.threads.messages.list(
  thread_id=activeUserThreadId
)


print(f'{theUser} : {theUserInput}')
print(f'Assistant: {messages.data[0].content[0].text.value}')
# with open("output.txt",'w',encoding='utf-8') as file:
#     file.write(messages.data[0].content[0].text.value)


        



