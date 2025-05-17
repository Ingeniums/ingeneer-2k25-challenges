
Given the following template, based on the format used by ctfcli by CTFd:
```yaml
name: "name"
author: "author"
# DO NOT CHANGE
category: {{category}}
description: |
  This is a sample description, 
  with multiple lines
attribution: Written by [author](https://ctfd.io)
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
# difficulty, author, category ARE MANDATORY may be other things you see fit
tags:
  # warmup/easy/medium/hard/tough
    - difficulty
  # this is to know which challenge was made by which author
    - author
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
```
Fill in the following information, taking into consideration the following:
1. if i give you any type of category don't add it to the output, the yaml is supposed to have a {{category}} be 
the category for all challenges, i will use the file path to fill it in.
2. if i give you any tags first fill in the required tags in the template (author, difficulty, {{category}}), 
then add the tags i input
3. Double check that the inputted flag matches the format `1ng3neer2k25{flag}` and tell me 
when it doesn't, also BE EXTRA CAUTIOUS not to change the flag part in `1ng3neer2k25{flag}`
4. The difficulty i input in should be in the tags (as indicated in the template) and in the 
value property of the output yaml under the format {{diff}} where diff is the difficulty i input in
5. If i specify that the flag is case_insensitive you use the format of the flag
```yaml
flags:
    - {
        type: "static",
        content: "1ng3neer2k25{wat}",
        data: "case_insensitive",
    }
```
else you use
```yaml
flags:
    -  1ng3neer2k25{flag}
```
6. If my author name contains `{}` put it between quotes (make it a string) both in the tags section and 
the author attribute, and tell me that the script will consider it a yaml section if it is not quoted
7. If anywhere in my input i specify that the challenge is web and i don't provide any 
connection_info, you fill it in as `{{url}}` make sure it is a string, if i specify a connection_info 
give some sort of noticeable warning that challenges meant to be accessible through the web should be set 
to `{{url}}` display this warning first and highlight it.
8. If anywhere in my input i specify that the challenge is a design challenge, 
you ignore any connection_info I input, and make sure not to add in in the output yaml
9. remove any files section I give you as input, and instruct me to put files to be access directly under `files` on the same 
directory as `challenge.yml` all files need to be on the first level of `files` so `src/file.txt` needs to go in `files/file.txt`, 
display the following folder structure:
    ```bash
    .
    ├── challenge
    │   ├── compose.yaml
    │   └── Dockerfile
    ├── challenge.yml
    ├── files
    │   └── file1.txt
    └── solution
    ```
10. instruct me to not have spaces in the challenge folder name, and to use 
`-` or `_`, and to also not include the difficulty in the name
11. Accept topics if they are inputted and add them in
12. For hints make sure they are either in the format
    ```yaml
    {
        content: "This hint costs points",
        cost: 10
    }
    ```
    or 
    ```yaml
    This hint is free
    ```
    for the first format if any fields are missing or not written properly fix them and put them in.
13. Mention that the category is deliberately set to {{category}} and it will later be filled.
14. If I ask about connection info tell me that it is used to tell the player 
how to connect to you challenge.
15. Any topics i put in should be in the topics section of the yaml file
16. For ssh and nc connection info whatever is provided, change the host and port to `{{host}}` and `{{port}}`, so for example: 
`ssh {{host}} {{port}}`, and tell me that you changed it if i didn't set it correctly, make sure to keep 
any other parameters i specify for the command

Input Information
Name: <challenge name>
Author: <author>
Difficulty: <difficulty>
Category: category
Flag: 1ng3neer2k25{wat}
Connection Info: nc/ssh/"{{url}}:{{port}}"/...
Extra Tags: test, hello
Description: <text>
