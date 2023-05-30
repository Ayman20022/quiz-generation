from __future__ import print_function
import openai
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import speech_recognition as sr




def create_quiz(text):

    text += '''the quiz should look like this : 1) What is 5 + 10?
    a) 12
    b) 14
    c) 15
    d) 18
    Answer: c) 15'''
    openai.api_key = "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"
    chat = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "user", "content": text},
        ]
    )
    # whisper resoponse 
    whisper_response = chat.choices[0].message.content


    print("whisper response : ",whisper_response)


    list_dict={}
    c=0
    list=[]
    for line in whisper_response.splitlines():
        if line != '':
            list.append(line)
        else : 
            list_dict[str(c)]=list
            c+=1
            list = []
    list_dict[str(c+1)]=list

    extracted_question = []
    extracted_choices = []
    extracted_answers = []
    for list in list_dict.values():
        question = list[0][3:]
        choices =[]
        for choice in list[1:-1]: 
            choices.append(choice[3:])
        answer = list[-1][11:]
        extracted_choices.append(choices)
        extracted_answers.append(answer)
        extracted_question.append(question)



    SCOPES = "https://www.googleapis.com/auth/forms.body"
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

    store = file.Storage('token.json')
    creds = None
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('key.json', SCOPES)
        creds = tools.run_flow(flow, store)

    form_service = discovery.build('forms', 'v1', http=creds.authorize(
        Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)
    # Request body for creating a form
    NEW_FORM = {
        "info": {
            "title": "Quiz",
        }
    }

    result = form_service.forms().create(body=NEW_FORM).execute()
    for question , choices  in zip(extracted_question,extracted_choices):
        NEW_QUESTION = {
        "requests": [{
            "createItem": {
                "item": {
                    "title": question,
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [ {"value":choice} for choice in choices],
                                "shuffle": True
                            }
                        }
                    },
                },
                "location": {
                    "index": 0
                }
            }
        }]
        }
        question_setting = form_service.forms().batchUpdate(formId=result["formId"], body=NEW_QUESTION).execute()
    # Prints the result to show the question has been added
    get_result = form_service.forms().get(formId=result["formId"]).execute()
    form_url = get_result['responderUri']
    return form_url




















