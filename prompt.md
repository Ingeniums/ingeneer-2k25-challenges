**Instructions for LLM to Generate `challenge.yml`**

Your task is to generate a `challenge.yml` file based on the following CTFd ctfcli template and the user-provided information. Adhere strictly to the rules below.

**Template:**

```yaml
name: "name"
author: "author"
# DO NOT CHANGE
category: {{category}}
description: |
  This is a sample description,
  with multiple lines
attribution: Written by [author]
# {{warmup}}/{{easy}}/{{medium}}/{{hard}}/{{tough}}
value: {{difficulty}}
type: standard
# for web challenges
protocol: http
# info on how to connect to a challenge, use {{port}} for port, and {{host}} for host
# for WEB challenges with http access set to {{url}}
# remove if not needed
connection_info: nc {{host}} {{port}}
# remove if unused
flags:
    # A static case sensitive flag
    -  1ng3neer2k25{3xampl3}
    # A static case insensitive flag
    - {
        type: "static",
        content: "1ng3neer2k25{wat}",
        data: "case_insensitive",
    }
# difficulty, category ARE MANDATORY may be other things you see fit
tags:
    # warmup/easy/medium/hard/tough
    - difficulty
    # DO NOT CHANGE
    - {{category}}
# Can be removed if unused
hints:
    - {
        content: "This hint costs points",
        cost: 10
    }
    - This hint is free
state: hidden
version: "0.1"
# remove if unused
topics:
    - topic1
    - topic2
# only for design challenges
# submit: drive
```

**Rules for Generation:**

1.  **Category:** Ignore any specific category provided in the input. The `category` field in the output YAML **must** be `{{category}}`. This is intentional and will be filled later based on the file path. Add `{{category}}` to the `tags` list as shown in the template.
2.  **Tags:** The `tags` list **must** include `difficulty` and `{{category}}` first. Then, add any additional tags provided in the input. **Do not** add the author's name to the tags list.
3.  **Attribution:** Set the `attribution` field to `Written by [author_name]`, where `author_name` is the author provided in the input.
4.  **Flag Format:** When a flag is provided, check if it matches the format `1ng3neer2k25{flag}`.
      * If it does NOT match this format, issue a warning *before* generating the YAML stating that the provided flag does not match the expected `1ng3neer2k25{flag}` format.
      * **CRITICAL:** Do not modify the `1ng3neer2k25{}` part of the flag. Only replace the content inside the curly braces with the user's flag content.
      * Handle case sensitivity as described in Rule 6.
5.  **Difficulty:** The difficulty provided in the input **must** be added to the `tags` list and also set as the value for the `value` field in the format `{{diff}}`, where `diff` is the input difficulty (e.g., `{{easy}}`, `{{hard}}`).
6.  **Flag Case Sensitivity:**
      * If the input specifies the flag is case-insensitive, use the following format under the `flags` key:
        ```yaml
        flags:
            - {
                type: "static",
                content: "1ng3neer2k25{wat}", # Replace 'wat' with the user's flag content
                data: "case_insensitive",
            }
        ```
      * Otherwise (case-sensitive or not specified), use the simplified format:
        ```yaml
        flags:
            -  1ng3neer2k25{flag} # Replace 'flag' with the user's flag content
        ```
7.  **Web Challenge Connection Info:**
      * If the input specifies the challenge `type` as `web` AND no `connection_info` is provided, set the `connection_info` field to the string `"{{url}}"`.
      * If the input specifies the challenge `type` as `web` AND `connection_info` *is* provided, issue a prominent warning *before* generating the YAML stating:
        ```
        ████ WARNING: WEB CHALLENGES SHOULD TYPICALLY USE '{{url}}' FOR CONNECTION_INFO ████
        Continuing with the provided connection_info...
        ```
        Then, process the provided `connection_info` according to Rule 15.
8.  **Design Challenge:** If the input specifies the challenge `type` as `design`:
      * Ignore any `connection_info` provided in the input and ensure the `connection_info` field is **not** included in the output YAML.
      * Add the field `submit: drive` to the root level of the YAML.
9.  **Files Section:** Ignore any `files` section provided in the input. Do **not** include a `files` section in the output YAML. After generating the YAML, provide the following instruction to the user:
    ````
    Please place any files for the challenge directly under a `files` directory in the same location as `challenge.yml`. All files should be at the first level within the `files` directory (e.g., `src/file.txt` should be moved to `files/file.txt`).

    Example folder structure:
    ```bash
    .
    ├── challenge
    │   ├── compose.yaml
    │   └── Dockerfile
    ├── challenge.yml
    ├── files
    │   └── file1.txt
    └── solution
    ````
10. **Challenge Folder Name:** After generating the YAML, provide the following instruction to the user regarding the challenge folder name:
    ```
    Remember not to use spaces in your challenge folder name. Use hyphens (-) or underscores (_) instead. Do not include the difficulty in the folder name.
    ```
11. **Topics:** If `topics` are provided in the input, include a `topics` list in the output YAML and add each provided topic as a list item. If no topics are provided, the `topics` field should not be included.
12. **Hints:** Process the `hints` provided in the input. Ensure each hint is in one of the two accepted formats:
      * Costed hint:
        ```yaml
        {
            content: "Hint content", # Use the provided hint text
            cost: 10 # Use the provided cost, or 10 if not specified
        }
        ```
        If a costed hint is provided but is missing the `content` or `cost` keys, or they are not properly formatted, correct them to match the structure above using the provided data.
      * Free hint:
        ```yaml
        "Free hint content" # Use the provided hint text
        ```
        Ensure free hints are formatted as a simple string list item.
13. **Category Explanation:** After generating the YAML, remind the user about the category field:
    ```
    Note that the 'category' field is deliberately set to '{{category}}'. This is a placeholder that ctfcli will automatically fill in based on the directory structure when the challenge is deployed.
    ```
14. **Connection Info Explanation (if asked):** If the user specifically asks about `connection_info`, explain:
    ```
    The `connection_info` field is used to tell players how to connect to your challenge service (e.g., `nc <host> <port>` or `ssh <host> <port>`). For web challenges, it is typically set to `{{url}}`.
    ```
    (Only provide this explanation if directly asked).
15. **SSH/NC Connection Info Formatting:** If the `connection_info` provided for an `ssh` or `nc` challenge includes host and port, change them to `{{host}}` and `{{port}}` respectively, while preserving any other command parameters.
      * Example input: `ssh user@1.2.3.4 -p 2222` -\> Output: `ssh user@{{host}} -p {{port}}`
      * Example input: `nc challenge.ctf.site 12345 -v` -\> Output: `nc {{host}} {{port}} -v`
      * If you make this change because the host/port were not already `{{host}}/{{port}}`, issue a brief notification after generating the YAML (but before the other instructions) stating:
        ```
        Note: The host and port in the connection_info have been standardized to {{host}} and {{port}}.
        ```
16. **Attribution Social Link Instruction:** After generating the YAML and any other notifications (like connection info standardization), add the following instruction about the attribution:
    ```
    Consider adding a social link (e.g., Twitter, GitHub) to the attribution field like `Written by [author](https://link-to-social-profile)` if you'd like to be credited with a link.
    ```

**Generation Process:**

1.  Start with the base template structure.
2.  Fill in the `name`, `author`, and `description` using the provided information.
3.  Set the `attribution` following Rule 3.
4.  Set the `category` to `{{category}}`.
5.  Set the `value` to `{{difficulty}}` using the provided difficulty.
6.  Determine the `type` and `protocol` based on the input (default `standard` and remove `protocol` if not web).
7.  Handle `connection_info` based on Rules 7, 8, and 15.
8.  Process the `flags` based on Rules 4 and 6.
9.  Populate the `tags` list following Rule 2, including the provided difficulty and `{{category}}`.
10. Process the `hints` based on Rule 12.
11. Set the `state` to `hidden` (as per template).
12. Set the `version` to `"0.1"` (as per template).
13. Handle `topics` based on Rule 11.
14. Handle the `submit: drive` field for design challenges based on Rule 8.
15. Ensure the `files` section is NOT included, as per Rule 9.
16. After generating the YAML, provide the post-generation instructions and warnings (Rules 4, 7, 9, 10, 13, 15, 16) *before* any YAML output, except for warnings that must precede the YAML.

-----

Input Information
Name: <challenge name>
Author: <author>
Difficulty: <difficulty>
Category: category
Flag: 1ng3neer2k25{wat}
Connection Info: nc/ssh/"{{url}}:{{port}}"/...
Extra Tags: test, hello
Description: <text>
