# Go Links with Real-Time File Updates

This is a Flask-based go/ links service that automatically reloads mappings from a JSON file when changes are detected.

## Features

- **Real-time updates**: Mappings are automatically reloaded when `mappings.json` is modified
- **File-based configuration**: All go/ links are stored in a JSON file
- **Background monitoring**: File changes are detected every minute
- **Error handling**: Graceful fallback if the mappings file is corrupted or missing
- **Web interface**: View all available mappings at the root URL

## Files

- `main.py` - Main Flask application with file watching
- `mappings.json` - Configuration file containing go/ link mappings
- `update_mappings.py` - Interactive script to manage mappings
- `README.md` - This documentation

## Usage

### 1. Start the server

```bash
python main.py
```

The server will start on `http://127.0.0.1:9191` and automatically load mappings from `mappings.json`.

### 2. Access go/ links

- Visit `http://127.0.0.1:9191/go/docs` to redirect to Python docs
- Visit `http://127.0.0.1:9191/go/github` to redirect to GitHub
- Visit `http://127.0.0.1:9191/` to see all available mappings

### 3. Update mappings in real-time

#### Option A: Edit mappings.json directly

Simply edit the `mappings.json` file with any text editor. The server will automatically detect changes and reload the mappings.

Example:
```json
{
    "docs": "https://docs.python.org/3/",
    "github": "https://github.com/",
    "newlink": "https://example.com"
}
```

#### Option B: Use the interactive script

```bash
python update_mappings.py
```

This provides a menu-driven interface to add, remove, and view mappings.

### 4. How real-time updates work

1. **Background monitoring**: A daemon thread checks the file modification time every minute
2. **Smart reloading**: Mappings are only reloaded when the file has actually changed
3. **Request-time updates**: Each request also triggers a reload check for immediate updates
4. **Error resilience**: If the file is corrupted or missing, existing mappings are preserved

## Example Workflow

1. Start the server: `python main.py`
2. In another terminal, run: `python update_mappings.py`
3. Add a new mapping: `go/test → https://example.com`
4. The server automatically detects the change and loads the new mapping
5. Visit `http://127.0.0.1:9191/go/test` to test the new link

## File Format

The `mappings.json` file should contain a valid JSON object where:
- Keys are the go/ link names (without the "go/" prefix)
- Values are the destination URLs

```json
{
    "linkname": "https://destination-url.com",
    "another": "https://another-site.org"
}
```

## Error Handling

- **File not found**: Server continues with empty mappings
- **Invalid JSON**: Server keeps existing mappings and logs the error
- **Permission errors**: Server logs the error and continues operation

## Performance

- File checking happens every minute in the background
- Each request also checks for updates (minimal overhead)
- Only reloads when file modification time changes
- Uses efficient file system calls for modification time checking

