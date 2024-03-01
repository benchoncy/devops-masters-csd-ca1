# DevOps Masters - Continous Software Delivery - CA1

This repository holds a proof of concept blood pressure web application and associated continuous integration and deployment pipeline as part of a continuous assessment.

## Development

Build the development container with docker. This container will have all nessary packages installed.
```
docker build . -t test --target development
```

Run the container with development files mounted.
```
docker run -it -p 5000:5000 --mount src="$(pwd)",target=/app,type=bind test
```

> Note: This repo is part of a university assignment, assume all decisions made for experimentation and learning and not for long-term maintainability.
