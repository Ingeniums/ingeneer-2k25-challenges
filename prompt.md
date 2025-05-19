**Instructions for LLM to Generate `challenge.yml`**

Your task is to generate a `challenge.yml` file based on the following CTFd ctfcli template and the user-provided information. **Crucially, remove all comments from the final YAML output.** Adhere strictly to the rules below.

**Template (Note: Comments are shown here for context, but REMOVE them in the final output):**

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
# difficulty level, category ARE MANDATORY may be other things you see fit
tags:
    # warmup/easy/medium/hard/tough
    - difficulty_level # THIS SHOULD BE THE ACTUAL LEVEL FROM INPUT
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

1.  **Remove Comments:** After generating the YAML structure based on the rules, **remove all lines starting with `#`** from the output.
2.  **Category:** Ignore any specific category provided in the input. The `category` field in the output YAML **must** be `{{category}}`. This is intentional and will be filled later based on the file path. Add `{{category}}` to the `tags` list as shown in the template.
3.  **Tags:** The `tags` list **must** include the **actual difficulty level** provided in the input (e.g., "easy", "hard") and `{{category}}` first. Then, add any additional tags provided in the input. **Do not** add the literal string "difficulty" or the author's name to the tags list.
4.  **Attribution:** Set the `attribution` field to `Written by [author_name]`, where `author_name` is the author provided in the input.
5.  **Flag Format:** When a flag is provided, check if it matches the format `1ng3neer2k25{flag}`.
      * If it does NOT match this format, issue a warning *before* generating the YAML stating that the provided flag does not match the expected `1ng3neer2k25{flag}` format.
      * **CRITICAL:** Do not modify the `1ng3neer2k25{}` part of the flag. Only replace the content inside the curly braces with the user's flag content.
      * Handle case sensitivity as described in Rule 7.
6.  **Difficulty:** Set the `value` field to `{{diff}}`, where `diff` is the actual difficulty level provided in the input (e.g., `{{easy}}`, `{{hard}}`). Also, add this actual difficulty level to the `tags` list according to Rule 3.
7.  **Flag Case Sensitivity:**
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
8.  **Protocol Field:** Include the `protocol` field **only if** the input specifies the challenge `type` as `web`. Set its value to `http`. Omit the `protocol` field otherwise.
9.  **Connection Info Field:**
      * Include the `connection_info` field **only if** it is explicitly provided in the input OR if the challenge `type` is `web` and no `connection_info` was provided (in which case, set it to `"{{url}}"` as per Rule 10).
      * If `connection_info` is provided for a non-web challenge (that is not a `design` challenge as per Rule 11), format it according to Rule 15.
      * Omit the `connection_info` field if it is not provided AND the challenge is not a `web` challenge requiring the default `{{url}}` (i.e., standard pwn/rev/crypto challenges without explicit connection info).
10. **Web Challenge Connection Info (Default):** If the input specifies the challenge `type` as `web` AND no `connection_info` is provided, set the `connection_info` field to the string `"{{url}}"`.
11. **Design Challenge:** If the input specifies the challenge `type` as `design`:
      * Ignore any `connection_info` provided in the input and ensure the `connection_info` field is **not** included in the output YAML (This is covered by Rule 9's omission rule).
      * The `protocol` field should also be omitted (covered by Rule 8 as it's not `web`).
      * Add the field `submit: drive` to the root level of the YAML.
12. **Web Challenge Connection Info (Warning):** If the input specifies the challenge `type` as `web` AND `connection_info` *is* provided, issue a prominent warning *before* generating the YAML stating:
    ```
    ████ WARNING: WEB CHALLENGES SHOULD TYPICALLY USE '{{url}}' FOR CONNECTION_INFO ████
    Continuing with the provided connection_info...
    ```
    Then, process the provided `connection_info` according to Rule 15.
13. **Files Section:** Ignore any `files` section provided in the input. Do **not** include a `files` section in the output YAML. After generating the YAML, provide the following instruction to the user:
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
14. **Challenge Folder Name:** After generating the YAML, provide the following instruction to the user regarding the challenge folder name:
    ```
    Remember not to use spaces in your challenge folder name. Use hyphens (-) or underscores (_) instead. Do not include the difficulty in the folder name.
    ```
15. **SSH/NC Connection Info Formatting:** If `connection_info` is provided and seems to be for `ssh` or `nc` (e.g., starts with `ssh` or `nc`), change any host and port specified to `{{host}}` and `{{port}}` respectively, while preserving any other command parameters.
      * Example input: `ssh user@1.2.3.4 -p 2222` -\> Output `connection_info`: `ssh user@{{host}} -p {{port}}`
      * Example input: `nc challenge.ctf.site 12345 -v` -\> Output `connection_info`: `nc {{host}} {{port}} -v`
      * If you make this change because the host/port were not already `{{host}}/{{port}}`, issue a brief notification after generating the YAML (but before the other instructions) stating:
        ```
        Note: The host and port in the connection_info have been standardized to {{host}} and {{port}}.
        ```
16. **Topics:** If `topics` are provided in the input, include a `topics` list in the output YAML and add each provided topic as a list item. **If no topics are provided in the input, the `topics` field should be entirely omitted from the output.**
17. **Hints:** Process the `hints` provided in the input. Ensure each hint is in one of the two accepted formats:
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
      * If no hints are provided, the `hints` field should not be included.
18. **Category Explanation:** After generating the YAML, remind the user about the category field:
    ```
    Note that the 'category' field is deliberately set to '{{category}}'. This is a placeholder that ctfcli will automatically fill in based on the directory structure when the challenge is deployed.
    ```
19. **Connection Info Explanation (if asked):** If the user specifically asks about `connection_info`, explain:
    ```
    The `connection_info` field is used to tell players how to connect to your challenge service (e.g., `nc <host> <port>` or `ssh <host> <port>`). For web challenges, it is typically set to `{{url}}`.
    ```
    (Only provide this explanation if directly asked).
20. **Attribution Social Link Instruction:** After generating the YAML and any other notifications (like connection info standardization), add the following instruction about the attribution:
    ```
    Consider adding a social link (e.g., Twitter, GitHub) to the attribution field like `Written by [author](https://link-to-social-profile)` if you'd like to be credited with a link.
    ```

**Generation Process:**

1.  Start building the YAML structure based on the user's input and the rules.
2.  Include fields like `name`, `author`, `description`, `attribution`, `category`, `value`, `type`, `flags`, `tags`, `state`, and `version` based on the input and corresponding rules (2, 3, 4, 5, 6, 7). Remember Rule 3 for adding the *actual* difficulty level to tags and Rule 6 for the `value` field format.
3.  Conditionally include `protocol` based on Rule 8.
4.  Conditionally include and format `connection_info` based on Rules 9, 10, 11 (omission for design), 12 (web warning), and 15 (formatting).
5.  Conditionally include `hints` based on Rule 17.
6.  Conditionally include `topics` based *strictly* on Rule 16 (only if provided in input).
7.  Conditionally include `submit: drive` based on Rule 11.
8.  Ensure the `files` section is NOT included, as per Rule 13.
9.  After constructing the full YAML structure, apply Rule 1 to remove all comments (`#`).
10. Finally, provide the post-generation instructions and warnings (Rules 5, 12, 13, 14, 15, 18, 20) *before* the YAML output, except for warnings that must precede the YAML.

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
