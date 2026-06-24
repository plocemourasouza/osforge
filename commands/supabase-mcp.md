# Supabase MCP Manager

Manage Supabase MCP configuration for the current project.

## Arguments
- `enable` - Add Supabase MCP to current project
- `disable` - Remove Supabase MCP from current project
- `status` - Check if Supabase MCP is configured

## Instructions

Based on the argument provided by the user, perform the following:

### For `enable` (default if no argument):
1. Check if `.mcp.json` exists in the current working directory
2. If it exists, read it and add/update the Supabase configuration
3. If it doesn't exist, create it with Supabase configuration
4. Use the token from `~/.claude/.supabase-token`

The Supabase MCP configuration should be:
```json
{
  "mcpServers": {
    "Supabase": {
      "command": "npx",
      "args": [
        "-y",
        "@supabase/mcp-server-supabase@latest",
        "--access-token",
        "<TOKEN_FROM_FILE>"
      ]
    }
  }
}
```

### For `disable`:
1. Read `.mcp.json` if it exists
2. Remove the "Supabase" key from mcpServers
3. Save the file

### For `status`:
1. Check if `.mcp.json` exists and contains Supabase configuration
2. Report the status to the user

After any change, remind the user to restart Claude Code to apply changes.
