# PowerShell Windows

**Trigger:** PowerShell, Windows scripting, Windows administration

---

## Core Differences from Bash

| Concept | Bash | PowerShell |
|---------|------|------------|
| Variable | `$VAR` | `$VAR` |
| Assignment | `VAR=value` | `$VAR = value` (spaces!) |
| Equality | `-eq` (numeric), `=` (string) | `-eq` (both) |
| Pipe | Text | Objects |
| And | `&&` | `-and` or `;` |
| Or | `\|\|` | `-or` |

---

## Essential Commands

### Navigation
```powershell
Get-Location              # pwd
Set-Location C:\path      # cd
Get-ChildItem             # ls
Get-ChildItem -Recurse    # ls -R
```

### File Operations
```powershell
Copy-Item src dest
Copy-Item src dest -Recurse    # Copy directory
Move-Item src dest
Remove-Item file
Remove-Item dir -Recurse -Force   # rm -rf equivalent
New-Item -ItemType Directory -Path path   # mkdir
New-Item -ItemType File -Path file        # touch
```

### File Content
```powershell
Get-Content file              # cat
Get-Content file -Head 20     # head
Get-Content file -Tail 20     # tail
Get-Content file -Wait        # tail -f
Get-Content file | Measure-Object -Line   # wc -l
```

### Search
```powershell
Get-ChildItem -Recurse -Filter "*.ts"
Get-ChildItem -Recurse | Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) }

Select-String "pattern" file.txt
Select-String "pattern" -Path *.ts -Recurse
```

---

## Variables & Operators

```powershell
# Variables
$name = "John"
$count = 42
$items = @(1, 2, 3)           # Array
$hash = @{ key = "value" }    # Hashtable

# String interpolation
"Hello, $name"                # Interpolated
'Hello, $name'                # Literal (no interpolation)

# Arithmetic
$result = 10 * 5
$count++
$count += 10

# Comparison
-eq      # Equal
-ne      # Not equal
-lt      # Less than
-gt      # Greater than
-le      # Less than or equal
-ge      # Greater than or equal
-like    # Wildcard match
-match   # Regex match
-contains # Array contains
```

---

## Control Flow

### Conditionals
```powershell
if ($condition) {
    # code
} elseif ($other) {
    # code
} else {
    # code
}

# Test file/path
Test-Path $path
Test-Path $path -PathType Container   # Directory
Test-Path $path -PathType Leaf        # File

# Switch
switch ($value) {
    "one" { "First" }
    "two" { "Second" }
    default { "Other" }
}
```

### Loops
```powershell
# ForEach
foreach ($item in $items) {
    Write-Output $item
}

# ForEach-Object (pipeline)
Get-ChildItem | ForEach-Object { $_.Name }

# For
for ($i = 0; $i -lt 10; $i++) {
    Write-Output $i
}

# While
while ($condition) {
    # code
}

# Do-While
do {
    # code
} while ($condition)
```

---

## Functions

```powershell
function Get-Greeting {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Name,

        [Parameter()]
        [string]$Greeting = "Hello"
    )

    return "$Greeting, $Name!"
}

# Call
Get-Greeting -Name "John"
Get-Greeting -Name "John" -Greeting "Hi"

# Advanced function
function Process-Items {
    [CmdletBinding()]
    param(
        [Parameter(ValueFromPipeline=$true)]
        [string[]]$Items
    )

    begin {
        Write-Verbose "Starting"
    }

    process {
        foreach ($item in $Items) {
            Write-Output "Processing: $item"
        }
    }

    end {
        Write-Verbose "Done"
    }
}

# Use in pipeline
@("a", "b", "c") | Process-Items
```

---

## Error Handling

```powershell
# Try-Catch
try {
    # Risky operation
    $result = Get-Content "nonexistent.txt" -ErrorAction Stop
} catch {
    Write-Error "Failed: $_"
} finally {
    # Cleanup
}

# Error action preference
$ErrorActionPreference = "Stop"   # Treat all errors as terminating

# Per-command
Get-Content file.txt -ErrorAction SilentlyContinue
Get-Content file.txt -ErrorAction Stop

# Check last command
if ($?) {
    Write-Output "Success"
} else {
    Write-Output "Failed"
}

# Throw error
throw "Something went wrong"
```

---

## Script Template

```powershell
#Requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$InputPath,

    [Parameter()]
    [switch]$Force,

    [Parameter()]
    [ValidateSet("Option1", "Option2")]
    [string]$Mode = "Option1"
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Output "[$timestamp] $Message"
}

function Main {
    Write-Log "Starting with input: $InputPath"

    if (-not (Test-Path $InputPath)) {
        throw "Input path not found: $InputPath"
    }

    if ($Force) {
        Write-Log "Force mode enabled"
    }

    # Main logic here

    Write-Log "Done"
}

try {
    Main
} catch {
    Write-Error "Script failed: $_"
    exit 1
}
```

---

## Common Tasks

### Working with JSON
```powershell
# Read JSON
$data = Get-Content "data.json" | ConvertFrom-Json

# Access properties
$data.name
$data.items[0]

# Write JSON
$object | ConvertTo-Json -Depth 10 | Set-Content "output.json"
```

### HTTP Requests
```powershell
# GET
$response = Invoke-RestMethod -Uri "https://api.example.com/data"

# POST
$body = @{ key = "value" } | ConvertTo-Json
$response = Invoke-RestMethod -Uri "https://api.example.com" -Method Post -Body $body -ContentType "application/json"

# With headers
$headers = @{ Authorization = "Bearer $token" }
$response = Invoke-RestMethod -Uri $url -Headers $headers
```

### Process Management
```powershell
Get-Process                  # List all
Get-Process -Name "code"     # By name
Stop-Process -Name "code"    # Kill by name
Stop-Process -Id 1234        # Kill by PID

Start-Process "notepad.exe"
Start-Process "script.ps1" -Wait
```

---

## Gotchas

1. **Spaces around `=`**: `$x = 1` not `$x=1`
2. **Use `-eq` for comparison**: `if ($x -eq 1)` not `if ($x = 1)`
3. **Return values**: Functions return all output, not just `return` statements
4. **Single vs Double quotes**: Use `"..."` for interpolation, `'...'` for literal
5. **Pipeline objects**: PowerShell pipes objects, not text
