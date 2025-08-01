import json
from itertools import chain
from tempfile import template

from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

import re

def clean_text(text):
    # Remove unpaired surrogates and invalid characters
    return text.encode("utf-16", "surrogatepass").decode("utf-16", "ignore")

def process_posts(raw_file_path , processed_file_path) :

   with open(raw_file_path,encoding="utf-8") as file :
       posts= json.load(file)
       enriched_posts = []

       for post in posts:
           post['text'] = clean_text(post['text'])  # <-- sanitize input
           metadata = extract_metadata(post['text'])

           post_with_metadata = post | metadata
           enriched_posts.append(post_with_metadata)
           
       unified_tags = get_unified_tags(enriched_posts)

       for post in enriched_posts :
           current_tags = post['tags']

           new_tags = {unified_tags[tag] for tag in current_tags}
           post['tags'] = list(new_tags)

       with open(processed_file_path, encoding='utf-8' , mode="w") as outfile:
           json.dump(enriched_posts, outfile,indent=4)

def get_unified_tags(post_with_metadata) :
    unique_tags = set()
    for post in post_with_metadata :
        unique_tags.update(post['tags'])

    unique_tags_list = ','.join(unique_tags)

    template = '''I will give you a list of tags. You need to unify tags with the following requirements,
        1. Tags are unified and merged to create a shorter list. 
           Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
           Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
           Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
           Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
        2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
        3. Output should be a JSON object, No preamble
        3. Output should have mapping of original tag and the unified tag. 
           For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation}}

        Here is the list of tags: 
        {tags}
        '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": str(unique_tags_list)})

    # print("LLM response:\n", response.content)

    # try:
    #     json_parser = JsonOutputParser()
    #     res = json_parser.parse(response.content)
    # except OutputParserException:
    #     raise OutputParserException("Context too big. Unable to parse jobs.")
    # return res

    raw_content = response.content

    # Extract JSON object using regex
    match = re.search(r"\{.*\}", raw_content, re.DOTALL)
    if not match:
        raise OutputParserException("Could not extract JSON from the LLM response.")

    json_string = match.group(0)

    try:
        res = json.loads(json_string)
    except json.JSONDecodeError as e:
        raise OutputParserException("Failed to parse JSON.") from e

    return res


def extract_metadata(post):
    template = '''
    You are given a LinkedIn post. Extract metadata in **strict JSON** format with no explanations or extra text.

    Requirements:
    1. Output only a valid JSON object — no notes, no comments, no preamble or suffix.
    2. JSON must have exactly these three keys: line_count (int), language (string), tags (array of max 2 strings).
    3. Tags should be relevant keywords extracted from the post.
    4. Language should be either "English" or "Hinglish".

    Here is the post:
    {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'post': post})

    # to check what is output by llama
    print("LLM response:\n", response.content)

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise  OutputParserException("Context too big. Unable to parse jobs.")
    return res



if __name__ == "__main__" :
    process_posts(raw_file_path="data/raw_posts.json" , processed_file_path="data/processed_posts.json")