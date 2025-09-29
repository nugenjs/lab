# JS, TS, and NodeJS
Sandbox for Javascript, Typescript, and NodeJS related.





## Build tools
### Vite (2020) (Rust)
Bundling tool and server that uses esBuild for development and Rollup for production builds.

Pros:
- Very fast dev startup (🏎️:smoke: Blazingly fast might might say)
- Hot Module Replacement (HMR)
- Out-of-the-box support for TypeScript and JSX
- Built-in scaffolding (React, Vue, Svelte, etc.)
- Large ecosystem momentum

Cons:
- Limited plugin ecosystem compared to Webpack
- Less mature
### Webpack (2014) (Javascript)
Bundling tool with huge consumer base, high configurability and stability.

Pros:
- Powerful plugin/loaders system
- Strong community support
- Battle hardened from years in production environments

Cons:
- Steep learning curve
- Configuration complexity
- Slow build times
### esBuild (2020) (Go)
JavaScript bundler and minifier. Primary use is compiler/transpiler. Unlike others, its focus in only 

Pros:
- Extremely fast (Uses parallelism)
- Simple configuration
- Can bundle, transpile, and minify in one step.

Cons:
- Limited features as focus was mainly for building
- Tree shaking is not as aggressive as Rollup
### Rollup (2015)
Bundler created for production builds

Pros:
- Very small bundles (libraries and npm packages)

Cons:
- Limited support for non-ES module formats
- More complex configuration for certain use cases