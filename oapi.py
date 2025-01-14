from pydantic import BaseModel
from openai import OpenAI

class HybridLanguageTranslation(BaseModel):
    original: str
    hybrid: str
    translation: str

class WordData(BaseModel):
    word: str
    id: str
    # alternative_forms: list[str]
    pronunciation: list[str]
    definition: list[str]
    translations: list[str]

class WordList(BaseModel):
    wordlist: list[WordData]

class SinogramWordData(BaseModel):
    sinogram: str
    id: str
    pronunciation: list[str]
    definition: list[str]
    translations: list[str]

class SinogramWordList(BaseModel):
    wordlist: list[SinogramWordData]

class SiniticWordData(BaseModel):
    characters: str
    id: str
    pronunciation: list[str]
    definition: list[str]
    translations: list[str]

class SiniticWordList(BaseModel):
    wordlist: list[SiniticWordData]

oa_key = None  # replace with caution
DUMMY_RESPONSE_PATH = "sample_responses/dummy_response"
DEFAULT_RESP_PATH = "./output/responses/"
DEFAULT_OUTPUT_PATH = "./output/out_json/"
DEFAULT_TEXT_PATH = "./output/translations/"

# DEFAULT_SYSTEM_PROMPT = """
#     You are a tool to help the user with what they want.

#     Return response in the form of a JSON object.

#     class WordData(BaseModel):
#         word: str
#         id: str
#         alternative_forms: list[str]
#         pronunciation: list[str]
#         definition: list[str]
#         translations: list[str]

#     class WordList(BaseModel):
#         wordlist: list[WordData]
    
#     Examples: 

#     ```python
#     class SiniticWordData(BaseModel):
#         characters: str
#         id: str
#         pronunciation: list[str]
#         definition: list[str]
#         translations: list[str]

#     class SiniticWordList(BaseModel):
#         wordlist: list[SiniticWordData]
#     ```

#     ```json
#     {
#         "wordlist" : [
#             {
#                 "characters": "教育",
#                 "id": "1",
#                 "pronunciation": [
#                     "giáo dục"
#                 ],
#                 "definition": [
#                     "education"
#                 ],
#                 "translations": [
#                     "教育 (jiào-yù) - Chinese",
#                     "教育 (kyō-iku) - Japanese",
#                     "교육 (gyo-yuk) - Korean",
#                     "教育 (gaau-yuk) - Cantonese",
#                     "教育 (kàu-io̍k) - Taiwanese Hokkien",
#                     "教育 (jiao-yu) - Shanghainese"
#                 ]
#             },
#             ... // many more such entries
#         ]
#     }
#     ```

#     Create a WordList as required by the user.
#     Most importantly, remember to follow the number of entries indicated by the user.
# """
#    If the user asks for a sample instead, generate a new example on your own and perform the rest of the task.

DEFAULT_SYSTEM_PROMPT = """
    You are a tool to help the user with what they want.

    Return response in the form of a JSON object.

    class WordData(BaseModel):
        word: str
        id: str
        alternative_forms: list[str]
        pronunciation: list[str]
        definition: list[str]
        translations: list[str]

    class WordList(BaseModel):
        wordlist: list[WordData]

    Create a WordList as required by the user.
    Most importantly, remember to follow the number of entries indicated by the user.
"""



DEFAULT_USER_PROMPT = "Perform the following task: \n{input_text}"

def generate_formatted_response(input_text, oa_key=oa_key, dummy=False) -> dict:
    """
        Returns the response object and other convenient data in a dictionary.
    """
    if dummy:
        return generate_response(DEFAULT_SYSTEM_PROMPT, DEFAULT_USER_PROMPT.format(input_text=input_text), oa_key=oa_key, dummy=True)
    
    response = generate_response(DEFAULT_SYSTEM_PROMPT, DEFAULT_USER_PROMPT.format(input_text=input_text), oa_key=oa_key)
    
    out = response.choices[0].message.parsed

    out_full_json_dict = out.model_dump(mode="json")
    out_full_json_text = out.model_dump_json(indent=4)
    
    #out_text = out_full_json_dict["test"]
    
    # translation_obj = {
    #     "original" : hybridLangTL_full_json_dict["original"],
    #     "hybrid" : hybrid_text,
    #     "translation" : hybridLangTL_full_json_dict["translation"],
    #     "json_dict" : hybridLangTL_full_json_dict,
    #     "json_text" : hybridLangTL_full_json_text,
    #     "response" : response
    # }

    out_obj = {
        "json_dict" : out_full_json_dict,
        "json_text" : out_full_json_text,
        "response" : response
    }

    return out_obj


def generate_response(system_text, user_text, oa_key=oa_key, dummy=False):
    if dummy:
        return load_response_var(DUMMY_RESPONSE_PATH)
    if oa_key is None:
        raise ValueError("OpenAI API key is not set.")

    client = OpenAI(api_key=oa_key)

    response = client.beta.chat.completions.parse(
        # NOTE WHICH MODEL IS BEING USED !!!
        model="gpt-4o-mini",
        #model="gpt-4o",
        messages=[
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text},
        ],
        response_format=WordList,
    )

    return response


def save_output(output, id=None, filename=None):
    """
        Save output.json to file.
    """
    if filename is None:
        if id is None:
            import uuid
            filename = f"output_{uuid.uuid4()}.json"
        else:
            filename = f"output_{id}.json"
    
    with open(filename, "w") as f:
        f.write(output)

def save_text(text, id=None, filename=None):
    """
        Save text output to file.
    """
    if filename is None:
        if id is None:
            import uuid
            filename = f"neperlands_{uuid.uuid4()}.json"
        else:
            filename = f"neperlands_{id}.json"
    
    with open(filename, "w") as f:
        f.write(text)


def save_response_content_text(response, id=None, filename=None):
    if filename == None:
        if id == None:
            import uuid
            filename = f"response_content_text_{uuid.uuid4()}.txt"
        else:
            filename = f"response_content_text_{id}.txt"
    
    with open(filename, "w") as f:
        f.write(response.choices[0].message.content)


def save_response_text(response, id=None, filename=None):
    if filename == None:
        if id == None:
            import uuid
            filename = f"response_text_{uuid.uuid4()}.txt"
        else:
            filename = f"response_text_{id}.txt"
    
    with open(filename, "w") as f:
        f.write(repr(response))


def save_response_var(response, id=None, filename=None):
    import pickle

    if filename is None:
        if id is None:
            filename = "response.txt"
        else:
            filename = f"response_{id}.txt"

    with open(filename, "wb") as f:
        pickle.dump(response, f)


def load_response_var(filename):
    if filename is None:
        raise ValueError("load_response_var: filename is None.")

    import pickle
    try:
        with open(filename, "rb") as f:
            loaded_response = pickle.load(f)
        return loaded_response
    except FileNotFoundError as e:
        print(f"WARNING: load_response_var: File not found: {filename}")
        return None


def main():
    #generate_translation = generate_formatted_response
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--text", "-t", required=True, help="Input text to translate.")
    #DEFAULT_TL_TEXT = "This is a sample sentence of nep Dutch. It is very fun to do something like this!"
    #parser.add_argument("--text", "-t", type=str, default=DEFAULT_TL_TEXT, help="Input text to translate.")
    parser.add_argument("--dummy", "-D", action="store_true", default=False, help="Run in dummy mode.")
    #parser.add_argument("--save", "-s", action="store_true", default=False, help="Save the translation response.")
    parser.add_argument("--verbosity", "-v", type=int, default=5, help="Level of verbosity.")

    parser.add_argument("--path-translation-text", "-p", type=str, default=DEFAULT_TEXT_PATH, help="Set path to save the text outputs.")
    parser.add_argument("--path-translation-json", "-j", type=str, default=DEFAULT_OUTPUT_PATH, help="Set path to save the output JSON files.")
    parser.add_argument("--path-response", "-r", type=str, default=DEFAULT_RESP_PATH, help="Set path to save the responses.")
    parser.add_argument("--generate-response", "-g", dest="GEN_RES_SAVE", action="store_true", default=False, help="Save API response to file.")
    args = parser.parse_args()

    DUMMY = args.dummy
    #SAVE = args.save
    M_GEN_RES_SAVE = args.GEN_RES_SAVE
    OUTPUT_PATH = args.path_translation_json.strip()
    TEXT_PATH = args.path_translation_text.strip()
    RESP_PATH = args.path_response.strip()
    input_text = args.text.strip()
    verbosity = args.verbosity

    import os
    if os.path.exists(OUTPUT_PATH) == False:
        os.makedirs(OUTPUT_PATH)

    # load .env file to obtain OpenAI API key
    from dotenv import load_dotenv

    load_dotenv()
    oa_key = os.getenv("OPENAI_API_KEY")
    if oa_key is None:
        raise ValueError("Main: OpenAI API key is not set.")

    # obtain response
    if verbosity > 2:
        print("Sending request...")
    out_obj = generate_formatted_response(input_text, oa_key, dummy=DUMMY)
    if verbosity > 2:
        print("Response obtained.")
    print()

    # process output
    response = out_obj["response"]
    out_json = out_obj["json_text"]
    #hybrid_text = translation_obj["hybrid"]

    # print some results to terminal
    #formatted_output_text = ""
    formatted_output_text = out_obj["json_text"]

    # if verbosity > 3:
    #     print(f"English: {out_obj["original"]}\n")
    #     formatted_output_text = ''.join([formatted_output_text, f"English: {translation_obj["original"]}\n"])
    
    # print(f"Neperlands: {hybrid_text}\n")
    # formatted_output_text = ''.join([formatted_output_text, f"Neperlands: {hybrid_text}\n"])
    
    # if verbosity > 4:
    #     print(f"Dutch: {translation_obj["translation"]}\n")
    #     formatted_output_text = ''.join([formatted_output_text, f"Dutch: {translation_obj["translation"]}\n"])
    
    print(formatted_output_text)

    # save response to file
    import uuid
    file_uuid = str(uuid.uuid4())
    if DUMMY:
        file_uuid = "dummy_" + file_uuid
    filename_output = OUTPUT_PATH + f"out_{file_uuid}.json"
    filename_fot = TEXT_PATH + f"text_{file_uuid}.txt"

    #filename_var = RESP_PATH + f"response_{file_uuid}.txt"
    filename_text = RESP_PATH + f"response_text_{file_uuid}.txt"
    filename_content_text = RESP_PATH + f"response_content_text_{file_uuid}.txt"

    if M_GEN_RES_SAVE:
        #save_response_var(response, id=file_uuid, filename=filename_var)
        save_response_text(response, id=file_uuid, filename=filename_text)
        save_response_content_text(response, id=file_uuid, filename=filename_content_text)
    

    save_output(out_json, id=file_uuid, filename=filename_output)
    save_output(out_json, id=file_uuid, filename=OUTPUT_PATH + "out_latest.json")
    save_text(formatted_output_text, id=file_uuid, filename=filename_fot)

    print()
    print(f"file_uuid: {file_uuid}")

    return response


if __name__ == "__main__":
    main()
