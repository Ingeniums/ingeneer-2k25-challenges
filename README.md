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

# Authors
| Author              | Challenges                                           |
|---------------------|------------------------------------------------------|
| tarekeee           | Problem Solving                                      |
| poysa213          | Web (1 tough)                                         |
| DahounManel        | Design                                               |
| Mountasser         | Design                                               |
| merzouka          | Web(1 easy), DevOps(1 warmup, 1 easy, 2 medium, 1 hard) |
| LanacerYasser      | Crypto(All)                                          |
| Ismail-anis-cherrak | Networking(All)                                     |
| Aymen-drid        | Reverse(All)                                         |
| Mehloul-Mohamed   | Web(1 warmup, 1 easy, 1 hard, 1 tough), DevOps(1 warmup, 1 easy) |
| sirmoncef         | Forensics(All), Web(1 easy, 2 medium)                 |
| MoncifT4F0        | Problem Solving                                      |
# Flag
`1ng3neer2k25{flag}`
