1. What is `@contextmanager` and why do we use it instead of a plain function here?
No need to write db.close(), the connection is always closed, so no connection leak occurs.

2. What does `check_same_thread=False` do and why is it necessary in a FastAPI application?
If two users try to access SQLite at the same time, only one user is allowed, and the other will get an error.

3. What happens to your data when the server restarts — with the old list vs. with SQLite?
Changes in a dictionary are stored in RAM, so if the server shuts down, the changes are lost. With SQLite, changes are always permanent.

