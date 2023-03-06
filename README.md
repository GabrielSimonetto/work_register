# Work Register
I am using this project to learn django and django-rest-framework. For now it's an app where you can register a Task you want to do and your daily time goal for this task, and create WorkEntry's that define a span of time in which you worked on said Task. After you defined when you have worked, it's possible to gather analytics on how you are doing on it.

## Running

You have 2 options, in both of them, the app will be available via `localhost:8080`.

### Locally:
```
make install
make run
```

### Via docker
Make sure you have `docker` installed in you machine and run:
```
make docker_build
make docker_run
```

## Testing
```
make install
make test
```
