# questions-three-poc

To run this PoC the first thing you need to do is: 
1st have python3 installed and install the requierements:

```sh
pip install -r requirements.txt
```

After it you will need to get the Access Token for Go Rest Web login via gmail account / fb account /github account in the next URL:
`https://gorest.co.in/access-token`

And once you have it, replace the value of 'token' `$YOUR_TOKEN_HERE` in /env file with your own token, and rename the file to a dotenv one.
```sh
mv ./env ./.env
```


After it you're ready to run the project:
```sh
python3 src/Users_Tests.py
```

Good Luck!
