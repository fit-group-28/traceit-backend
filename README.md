# Toolchain

1. Install pipenv
2. brew install postgresql
3. pipenv install

# Run

To run the server, run
`pipenv run python src/app.py`
from the terminal. The server should be exposed at `localhost:3000`.

# Conventions

1. Place endpoints handler functions within their own file in the src/endpoints directory.
2. Place db queries in the src/dbops directory. Import these to the handlers, then call them there with the dbconnectors.
3. Define dataclasses corresponding to database models.
4. When performing SQL queries, deserialise from the returned tuple immediately, then operate programmatically on the instantiated dataclass objects. Minimise the lifespan of stray tuples that can't be typechecked.
5. DB operations should create and use only one connection if possible.
6. Use type annotations where possible, and use MyPy to typecheck
7. Document every function! (Easy with copilot)
8. Minimise the lifespan of instantiated objects in general, and avoid shared mutable state. Instantiate the object, use it for what you need, then discard it.
