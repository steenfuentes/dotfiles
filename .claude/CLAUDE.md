# Generation Guidelines for Claude
- When making additions to code, prefer direct, clean changes over backward compatibility layers.

## Style Guidelines
Adhere to these coding guidelines when generating code.

### General Style Guidelines

#### Do not include redudunant inline comments
Avoid comments that restate what the code does. If there is ambiguity in the code,
comments should provide additional context or explain why something is done,
not what is being done. 

Example of what not do do (redundant inline comments):
```python
  def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns
    -------
    FastAPI
        Configured FastAPI application
    """
    settings = get_settings()

    # Create FastAPI app
    app = FastAPI(
        title="propagate Platform API",
        version="1.0.0",
        description="Modular AI platform with MCP support",
        lifespan=lifespan,
    )

    # Setup middleware
    setup_cors_middleware(app, settings.cors_origins)
    setup_custom_middleware(app)

    # Include API routers
    app.include_router(v1_router, prefix=settings.api_v1_prefix)

    return app
  ```

This can be cleaned up to just:

```python
def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns
    -------
    FastAPI
        Configured FastAPI application
    """
    settings = get_settings()

    app = FastAPI(
        title="propagate Platform API",
        version="1.0.0",
        description="Modular AI platform with MCP support",
        lifespan=lifespan,
    )

    setup_cors_middleware(app, settings.cors_origins)
    setup_custom_middleware(app)

    app.include_router(v1_router, prefix=settings.api_v1_prefix)

    return app
```

### Python Specific Guidelines
When generating Python code, follow these additional guidelines.

#### Comments and Docstrings
- Follow PEP 8 and PEP 257 conventions for comments and docstrings, and use Numpy-style docstrings
for all documentation (from modules to functions and classes)
- Always prefer absolute imports over relative imports
- When installing dependencies, don't specify versions unless absolutely necessary
