

-  **Poetry** (`poetry==^1.8`): Follow the [installation guide](https://python-poetry.org/docs/main/#installing-with-the-official-installer).

-  **Python Environment Manager**: Use [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html), [pyenv](https://github.com/pyenv/pyenv), or [venv](https://docs.python.org/3/library/venv.html) to manage your Python environment (`python==^3.10`).

-  **IDE**: Recommended IDEs are [PyCharm](https://www.jetbrains.com/pycharm/download/) or [VSCode](https://code.visualstudio.com/download).

-  **Development Environment Setup**: See [CONTRIBUTING.md](CONTRIBUTING.md#setting-up-the-dev-environment) for detailed instructions.



### Running the Application



Once the prerequisites are set up, you can run the application locally with:



```bash

python -m  app.main

```



Or, if you're using Poetry:



```bash

poetry run  python  -m  app.main

```



The application will be available at [http://localhost:8001](http://localhost:8001), with API documentation accessible at [http://localhost:8001/api/docs](http://localhost:8001/api/docs).



## Contribution Guidelines



To contribute to this project, please read through [CONTRIBUTING.md](CONTRIBUTING.md) and adhere to the standards outlined in [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).



## Changelog



For a history of changes, refer to [CHANGELOG.md](CHANGELOG.md).



## Additional Hints




### Poetry Installation

For LINUX, MACOS
```
curl -sSL https://install.python-poetry.org | python3 -
```

By default, Poetry is installed into a platform and user-specific directory:
```
~/Library/Application Support/pypoetry on MacOS.
~/.local/share/pypoetry on Linux/Unix.
%APPDATA%\pypoetry on Windows.

curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
 ```


For Windows users, install Poetry using PowerShell:



```powershell

(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

```

Please refer to this detailed documentation on installing poetry :




Windows installation is bit tricky please refer to documentation for detailed steps.

Official Document : https://python-poetry.org/docs/#installing-with-the-official-installer

You Tube : https://www.youtube.com/watch?v=5lioBm8f324



**Note:**

Ensure that Poetry's bin directory (`C:\Users\<user>\AppData\Roaming\Python\Scripts`) is included in your `PATH` environment variable.



---




### Poetry Commands



Below are common Poetry commands. Refer to the [Poetry CLI documentation](https://python-poetry.org/docs/cli/) for more details:



```bash

# Install Poetry
Follow the instruction outlined in the section above,  Poetry Installation


# Create virtual env using poetry
poetry config  virtualenvs.in-project  true


# Install dependencies from pyproject.toml
poetry install


# switch to your virtual env
poetry shell


# Update all dependencies
poetry update


# Add a new dependency
poetry add <your-package>


# Remove an existing dependency
poetry remove <your-package>

  ```

