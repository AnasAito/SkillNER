# How to use custom skill list

To accommodate the various differences between skill lists, the preprocessing confirguration for a specific list needs to be hard-coded (hence not yet non-prorammer friendly) in the `preprocess_skills.py` file as a child class of an abstract class called `BaseSkillProcessor`.

In this tutorial, the skill list from EmPath Proficiency Library (EPL) will be used as an example. 

1. Convert the original skill list to a json records with the following format, with "id" and "name" being the obligatory unique string fields for each skill, "type" optional:

   ```
   [
       {
           "id":"tmwrkepl",
           "name":"Working as a Team",
           "type":"Leadership"
       },
       {
           "id":"designthepl",
           "name":"Design Thinking Process",
           "type":"Leadership"
       },
       {
           "id":"Couchbaseepl",
           "name":"Couchbase",
           "type":"Technology"
       },
       ...
   ]
   ```

2. Save the json skill list to, e.g. [/buckets/epl_raw_skills.json](/buckets/epl_raw_skills.json)
3. In [preprocess_skills.py](/skills_processor/preprocess_skills.py), create a subclass of `BaseSkillProcessor`, e.g. `EPLSkillProcessor`, which has at least the following mandatory fields/methods:
   * `skill_list_name`: str name of the skill list
   * `fetch_raw_skill_list()`: method to load and return the json skill list created in Step 1
   * `_get_abbr()`: method to extract abbreviation information from a skill dict in the json records; returns an empty string if such field is not provided
   * All other modularized methods can be overridden if needed; e.g. `EPLSkillProcessor` implements a slightly different version of `_add_initial_high_low_surfaces_forms`
4. Once the subclass is created, test the code out with the following snippet (very similar to the [README.md](/README.md)):
    ```python
    import en_core_web_lg
    
    from skills_processor.preprocess_skills import EPLSkillProcessor
    from spacy.matcher import PhraseMatcher
    from skillNer.skill_extractor_class import SkillExtractor

    # instantiate processor based on the skill list to use
    esp = EPLSkillProcessor()
    skill_processed = esp.generate_final_skill_list()

    # init params of skill extractor
    nlp = en_core_web_lg.load()

    # init skill extractor
    skill_extractor = SkillExtractor(nlp, skill_processed, PhraseMatcher)

    # extract skills from job_description
    job_description = """
     have experience with Python. and have the initiative to take ownership. 
     familiarity with REST framework. experience implementing APIs. 
     Familiar with Agile Development. Experience with Web Development. 
     Comfortable working in a team.
     """

    annotations = skill_extractor.annotate(job_description)
    ```

# Directory Structures

Currently, the code creates a `/skill_db_relax_20.json` file in the project root whenever we run the extractor sample code. This would not work very well when we'd like to support multiple skill lists.

Here's a proposed new structure to accommodate multiple skill lists (as implemented in this fork):

- Raw skill lists can either come directly from an third-party API request (EMSI) or from bucket/ (EPL)

- The preprocessed files will be saved at `/skill_data` as follows, e.g. if we've processed both EMSI and EPL lists:

  ```
  skill_data
  ├── EMSI
  │   ├── skill_db_relax_20.json
  │   ├── skills_processed.json
  │   └── token_dist.json
  └── EPL
      ├── skill_db_relax_20.json
      ├── skills_processed.json
      └── token_dist.json
  ```

What do you think? Please see following subsection if you like this idea.

## File and Code Clean Up

If you are ok with the proposed repository structure above, then we could:

* delete the 3 preprocessed files under [buckets/](/buckets); these can all be found in [skill_data/EMSI/](/skill_data/EMSI)

* delete the `from skillNer.general_params import SKILL_DB` from docstrings in [matcher_class.py](/skillNer/matcher_class.py)

* modify/delete code in [general_params.py](/skillNer/general_params.py) that attempts to load SKILL_DB and TOKEN_DIST to avoid errors fetching the deleted files
  * maybe delete the TOKEN_DIST import in utils.py bc it's not used anywhere?

* modify [README.md](/README.md), where the use of imported SKILL_DB is involved; you can now instruct the user to instead use e.g. 

  ```
  from skills_processor.preprocess_skills import EPLSkillProcessor
  SKILL_DB = EPLSkillProcessor().generate_final_skill_list()
  ```

* ...anywhere else you could think of where the use of the 3 preprocessed files are used.

LMK if you'd like me to do it and/or if you have any suggestions!
  

# Future Directions
## Enable Bucket to Fetch Custom Skill List

If you'd like to keep the custom skill list in the buckets for future development/testing, please: 

1. (DONE) upload [epl_raw_skills.json](/buckets/epl_raw_skills.json) to buckets/
2. in `remote_db.py`, make sure the `EPL_SKILL_LIST` value can be retrieved using `bucket` correctly like other files
3. in `preprocess_skills.py`, make sure the method `EPLSkillProcessor.fetch_raw_skill_list` uses bucket to load the raw EPL skill list

## Optimize code for high and low surface form creation

The code in `BaseSkillProcessor.generate_final_skill_list` and `BaseSkillProcessor._add_initial_high_low_surfaces_forms` directly use the code provided in how_new_db.md. 

However, part of the code has comments saying it's to be deleted ([part 1](https://github.com/yonglin-wang/SkillNER/blob/e486ce726e8186511f99181a6e1e5e562b3399f7/skills_processor/preprocess_skills.py#L161) and [part 2](https://github.com/yonglin-wang/SkillNER/blob/e486ce726e8186511f99181a6e1e5e562b3399f7/skills_processor/preprocess_skills.py#L296)). Could you look into the code and decide if you'd like to delete them now?

## Support .describe()

Currently we cannot use .describe() for the custom list because the color scheme is hard-coded (see [here](https://github.com/yonglin-wang/SkillNER/blob/e486ce726e8186511f99181a6e1e5e562b3399f7/skillNer/general_params.py#L10) and [here](https://github.com/yonglin-wang/SkillNER/blob/e486ce726e8186511f99181a6e1e5e562b3399f7/skillNer/general_params.py#L18)). Can we maybe find a fall back color (grey?) for type values that don't have a preset color? 

## Potential Fix for... 
When the code was tested on EPL list, there have been some interesting mismatches alongside the already amazing smartness of the tool. It would be great if the code could be improved to account for these mismatches in future.

### False Negatives
* It would probably be reasonable to expect a skill titled "Working as a team" to be extracted from "work in a team" or "work in teams", but it's not, and there's no low surface forms for this skill at all.
  * proposal: for skills with len > 2, can we add a stopword-less, lemmatized/stemmed form of the skill title as a low form? e.g. "work team" will be a low surface form for the skill, and hopefully matched with the stopword-less, lemmatized/stemmed text?


### False Positives
This one seems harder to solve, but discussions are welcome!
* In the sample code used in [How to Use Custom Skill List](#how-to-use-custom-skill-list), a skill named "mobile web development" was extracted from text "web development".. but being able to extract skill "Agile Development Practices" from "agile development" is a really nice feature. How can we prevent the code from extracting skills that are too narrow (mobile web dev), while still extracting skills with same meaning (agile dev practices)?






