# File structure
- Add your challenge to its corresponding category
- Create a folder corresponding to the name of your challenge prefixed with difficulty, eg: `easy - [challenge Name]`
- Include if possible a `challenge.yml` file containing description of your challenge. You can find an example 
[here](https://github.com/CTFd/ctfcli/blob/master/ctfcli/spec/challenge-example.yml).
- If you are not able to add the `challenge.yml` file, add a `flag.txt` file under `challenge/`
- Put the challenge files (Dockerfile, scripts, ...) under the `challenge/` folder
- Put the files to be accessible to participants under the `challenge/files/` folder
- Add category, difficulty, author under `tags` in `challenge.yml`
- Solution should be under `solution/` folder
# Example
```bash
easy-Sample/
├── solution
├── challenge.yml
└── challenge
    ├── files
    │   ├── file2.txt
    │   └── file1.txt
    └── Dockerfile
```
