# Create Vue Project

You can use the following commands to create a new vue project.

```bash
$ npm create vue@latest
```

**Notice**: You may encounter some issues about the npm network error.
The following solutions ([link1](https://stackoverflow.com/a/18428563), [link2](https://stackoverflow.com/a/56938323)) may help:

```bash
# Only use the following commands when you encounter network error
$ npm config set registry http://registry.npmjs.org/
$ npm config delete proxy
$ npm config delete https-proxy
```
