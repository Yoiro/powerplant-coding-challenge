# powerplant-coding-challenge

## How to run the development server

[Python 3.7+][1] needs to be installed, as long as [Poetry][2] in order to manage dependencies.

Once both are setup, stay at the root of this repository and simply run
```
poetry install
```

in order to setup your virtual environment with all the dependencies.


Once the command finished running, you're all set in order to run the app. Some convenience scripts are provided in order to run the development server.

* For Powershell, execute `runapp.ps1`
* For CMD, execute `runapp.bat`
* For bash:
    First make the script executable by running `chmod +x runapp`
    Then execute `runapp`

Once the server is started, you can interact with it either through some HTTP client such as `curl` or even `Postman`,
but some unit tests have been provided in order to make calls to the API with the provided example payloads.

If you are using another shell, you have to make sure that:
* The FLASK_APP environment variable is set to `powerplant`
* the FLASK_ENV is set to whatever variable you want it to be (it will default to `prd`, but you can set it to `dev`)
* the arguments you give to the `flask run` command match the ones within the startup scripts (`--host 127.0.0.1  --port 8888`)

Example command (for bash): 
```
FLASK_APP=powerplant FLASK_ENV=development poetry run flask run --host 127.0.0.1 --port 8888
```

NB: all these scripts expose the API on the port 8888.

## Running unit tests

Please be careful that the unit tests will only run if you installed the development dependencies (meaning that you had to run `poetry` without the
`--no-dev` argument).

Moreover, you'll need to boot the server up in another terminal (see Running the development server above) for the unit tests to run.

If you want to run the tests, just enter the command

```
poetry run pytest test
```

The command will automatically run all the unitests contained within the `test` directory.

## Running in production
A Dockerfile has been provided in order to execute the application within a [Gunicorn][3] instance, allowing for a more robust 
way to handle requests. The image provides only the basic steps in order to deploy the application, such as adding a gunicorn user, giving it access to
the application folder, and finally running the server.

The Docker entrypoint is set to `poetry`, with default arguments allowing us to run the server (`run gunicorn [args]`) so if you want to 
override the behavior of the container when you run it, you just have to specify `run gunicorn [other args]` when entering the docker command.

The typical workflow would be (assuming you are at the root of the repository):

```
docker build --tag powerplant:latest .
docker run --name powerplant -p 8888:8888 powerplant:latest
```

or, if you don't want the container to take control of stdout:

```
docker run -dit --name powerplant -p 8888:8888 powerplant:latest
```

or, if you want to do something else with poetry (list the dependencies, for exemple)

```
docker run -dit --name powerplant -p 8888:8888 powerplant:latest show -v
```

The Gunicorn instance is configured to expose the port 8888 and no other port is exposed through the Dockerfile, so keep that in mind if you want to play with the arguments you give it.

For a list of the available options to use with Poetry, you can refer to its [documentation][5]

## Logging
Some basic logging has been set, using Flask's logger object. You'll be able to see its output wihtin the stdout, no log file have been setup 


For more information on the challenge, go see [Challenge][4]


[1]: https://www.python.org/downloads/
[2]: https://python-poetry.org/docs/#installation
[3]: https://gunicorn.org/
[4]: CHALLENGE.md
[5]: https://python-poetry.org/docs/cli/#commands
