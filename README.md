<h1 align="center">Welcome to Sudoku game 👋</h1>
<p>
  <a href="https://www.codacy.com/manual/hadialqattan/sudoku?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=hadialqattan/sudoku&amp;utm_campaign=Badge_Grade"><img alt="Python version: 3.x" src="https://app.codacy.com/project/badge/Grade/07a9c48a23bf41fdb278590209b04967">
  </a>
  <a href="https://www.python.org/"><img alt="Python version: 3.x" src="https://img.shields.io/badge/python-python%203.x-blue.svg">
  </a>
  <a href="https://github.com/hadialqattan/sudoku/blob/master/LICENSE" target="_blank">  
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://docutils.sourceforge.io/rst.html"><img alt="Docstrings: reStructuredText" src="https://img.shields.io/badge/docstrings-reStructuredText-gree.svg">
  </a>
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
  </a>
</p>

> GUI desktop [Sudoku game](https://en.wikipedia.org/wiki/Sudoku) using [pygame](https://www.pygame.org/wiki/GettingStarted). (include [Sudoku solver](https://github.com/hadialqattan/sudoku/blob/master/src/solver/solver.py) and [random Sudoku board generator](https://github.com/hadialqattan/sudoku/blob/master/src/generator/generator.py))

# Demo ([Full demo](https://github.com/hadialqattan/sudoku/tree/master/docs/DEMO.md)) 🧮

automatic solver

![start button](https://github.com/hadialqattan/sudoku/blob/master/docs/gif/start.gif?raw=true)

win 

![Won](https://github.com/hadialqattan/sudoku/blob/master/docs/gif/won.gif?raw=true)

lose

![Lost](https://github.com/hadialqattan/sudoku/blob/master/docs/gif/lost.gif?raw=true)

# Usage 🗝
### There's two way to use this project: 
* Without any prerequisites: 
  + download whole [executable directory](https://github.com/hadialqattan/sudoku/tree/master/executable)
  + run [executable/exe/sudoku.exe](https://github.com/hadialqattan/sudoku/tree/master/executable/exe/sudoku.exe)

* With prerequisites: 
  + clone this repo : 
    ```shell 
    $ git clone https://github.com/hadialqattan/sudoku.git
    ```
  + [install prerequisites](#Prerequisites%20🔩)
  + Run run.sh : 
    ```shell
    $ ./run.sh
    ```

# Prerequisites 🔩

* [Python 3.x](https://www.python.org/downloads/)
* Python libraries from [requirements.txt](https://github.com/hadialqattan/sudoku/blob/master/requirements.txt)
  ```shell 
  $ sudo pip3 install -r requirements.txt
  ```

# Tests 🧪

### Unit tests @ [tests directory](https://github.com/hadialqattan/sudoku/tree/master/tests) include tests only for :
* [src.solver.sovler.Solver](https://github.com/hadialqattan/sudoku/blob/master/src/solver/solver.py) class (not include auto_solver function) @ [tests/test_01_solver.py](https://github.com/hadialqattan/sudoku/blob/master/tests/test_01_solver.py) using [tests/IO.py](https://github.com/hadialqattan/sudoku/blob/master/tests/IO.py) data.
* [src.generator.generator.Generator](https://github.com/hadialqattan/sudoku/blob/master/src/generator/generator.py) class @ [tests/test_02_generator.py](https://github.com/hadialqattan/sudoku/blob/master/tests/test_02_generator.py).

### Run instructions:

* All tests :
  ``` shell
  $ pytest -v tests/
  ```

* Specific tests :
  + only solver tests :
    ``` shell
    $ pytest -v tests/test_01_solver.py
    ```

  + only generator tests :
    ```shell
    $ pytest -v tests/test_02_generator.py
    ```

# Copyright ©

👤 **Hadi Zaki Alqattan**

* Github: [@hadialqattan](https://github.com/hadialqattan)
* Email: [alqattanhadizaki@gmail.com]()

📝 **License**

Copyright © 2020 [Hadi Zaki Alqattan](https://github.com/hadialqattan).<br />
This project is [MIT](https://github.com/hadialqattan/sudoku/blob/master/LICENSE) licensed.

***
Give a ⭐️ if this project helped you!
