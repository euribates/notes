---
title: Notes on gulp
---

### How to install gulp

First, check the version for node, npm and npx

```shell
node --version
npm --version
npx --version
```

At 19th, May 2021, this is the current versions

| Name     | Version   |
|----------|-----------|
| ``node`` | v16.13.0  |
| ``npm``  | 6.14.9    |
| ``npx``  | 10.2.2    |

Now install `gulp-cli`:

```shell
$ gulp --version
CLI version: 2.2.0
Local version: 4.0.0
```

#### Gulpfile explained

A **gulpfile** is a file in your project directory titled `gulpfile.js` (or
capitalized as `Gulpfile.js`, like `Makefile`), that automatically loads when
you run the gulp command. Within this file, you'll often see gulp APIs, like
`src()`, `dest()`, `series()`, or `parallel()` but any vanilla JavaScript or Node
modules can be used. **Any exported functions** will be registered into gulp's task
system.

You can write a gulpfile using a language that requires **transpilation**, like
**TypeScript** or **Babel**, by changing the extension on your `gulpfile.js` to
indicate the language and install the matching transpiler module.

For TypeScript, rename to `gulpfile.ts` and install the
[`ts-node`](https://www.npmjs.com/package/ts-node) module.  For Babel, rename
to `gulpfile.babel.js` and install the
[`@babel/register`](https://www.npmjs.com/package/@babel/register) module. 

Most new versions of node support most features that TypeScript or Babel
provide, except the import/export syntax. When only that syntax is desired,
rename to `gulpfile.esm.js` and install the
[`esm`](https://www.npmjs.com/package/esm) module.








Sources:

- [Gulp Quick Start](https://gulpjs.com/docs/en/getting-started/quick-start/)
