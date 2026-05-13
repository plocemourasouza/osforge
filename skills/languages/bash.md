# Bash/Linux

**Trigger:** Bash, shell script, Linux commands, terminal, CLI

---

## Essential Commands

### Navigation
```bash
pwd                     # Print working directory
cd /path/to/dir         # Change directory
cd -                    # Go to previous directory
cd ~                    # Go to home

ls -la                  # List all files with details
ls -lah                 # Human-readable sizes
tree -L 2               # Tree view, 2 levels deep
```

### File Operations
```bash
cp source dest          # Copy file
cp -r source dest       # Copy directory recursively
mv source dest          # Move/rename
rm file                 # Remove file
rm -rf dir              # Remove directory (DANGEROUS)
mkdir -p path/to/dir    # Create nested directories
touch file              # Create empty file / update timestamp
```

### File Content
```bash
cat file                # Print entire file
head -n 20 file         # First 20 lines
tail -n 20 file         # Last 20 lines
tail -f file            # Follow file (live updates)
less file               # Paginated view
wc -l file              # Count lines
```

### Search
```bash
find . -name "*.ts"                    # Find by name
find . -type f -mtime -7               # Files modified in last 7 days
find . -size +10M                      # Files larger than 10MB

grep "pattern" file                    # Search in file
grep -r "pattern" dir/                 # Recursive search
grep -rn "pattern" dir/                # With line numbers
grep -ri "pattern" dir/                # Case insensitive
```

---

## Piping & Redirection

```bash
# Pipe output to another command
cat file | grep "pattern" | wc -l

# Redirect stdout
command > file          # Overwrite
command >> file         # Append

# Redirect stderr
command 2> errors.log

# Redirect both
command > output.log 2>&1
command &> output.log   # Bash shorthand

# Discard output
command > /dev/null 2>&1
```

---

## Variables & Strings

```bash
# Variables
NAME="John"
echo "Hello, $NAME"
echo "Hello, ${NAME}!"  # Braces for clarity

# Command substitution
DATE=$(date +%Y-%m-%d)
FILES=$(ls -1 | wc -l)

# Arithmetic
COUNT=$((COUNT + 1))
RESULT=$((10 * 5))

# String operations
${VAR:-default}         # Use default if VAR is unset
${VAR:=default}         # Set default if VAR is unset
${VAR:+replacement}     # Use replacement if VAR is set
${#VAR}                 # Length of VAR
${VAR^^}                # Uppercase
${VAR,,}                # Lowercase
```

---

## Control Flow

### Conditionals
```bash
if [ "$VAR" = "value" ]; then
    echo "Match"
elif [ "$VAR" = "other" ]; then
    echo "Other"
else
    echo "No match"
fi

# File tests
[ -f file ]     # File exists
[ -d dir ]      # Directory exists
[ -r file ]     # File is readable
[ -w file ]     # File is writable
[ -x file ]     # File is executable
[ -s file ]     # File is not empty

# String tests
[ -z "$VAR" ]   # String is empty
[ -n "$VAR" ]   # String is not empty
[ "$A" = "$B" ] # Strings are equal

# Numeric tests
[ "$A" -eq "$B" ]   # Equal
[ "$A" -ne "$B" ]   # Not equal
[ "$A" -lt "$B" ]   # Less than
[ "$A" -gt "$B" ]   # Greater than
```

### Loops
```bash
# For loop
for file in *.txt; do
    echo "Processing $file"
done

for i in {1..10}; do
    echo "Number: $i"
done

# While loop
while read -r line; do
    echo "$line"
done < input.txt

# Until loop
until [ "$STATUS" = "ready" ]; do
    sleep 1
    STATUS=$(check_status)
done
```

---

## Script Template

```bash
#!/usr/bin/env bash
set -euo pipefail  # Exit on error, undefined var, pipe fail

# Constants
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="/tmp/script.log"

# Functions
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

die() {
    log "ERROR: $*"
    exit 1
}

usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] <argument>

Options:
    -h, --help      Show this help
    -v, --verbose   Verbose output
    -f, --force     Force operation

Arguments:
    argument        Description of argument
EOF
}

# Parse arguments
VERBOSE=false
FORCE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -*)
            die "Unknown option: $1"
            ;;
        *)
            ARGUMENT="$1"
            shift
            ;;
    esac
done

# Validate
[ -z "${ARGUMENT:-}" ] && die "Argument required. See --help"

# Main
main() {
    log "Starting script with argument: $ARGUMENT"

    if [ "$VERBOSE" = true ]; then
        log "Verbose mode enabled"
    fi

    # Your code here

    log "Done"
}

main "$@"
```

---

## Process Management

```bash
# Background processes
command &               # Run in background
jobs                    # List background jobs
fg %1                   # Bring job 1 to foreground
bg %1                   # Resume job 1 in background

# Process info
ps aux                  # All processes
ps aux | grep name      # Find process
pgrep -f pattern        # Find process ID
top                     # Interactive process viewer
htop                    # Better process viewer

# Kill processes
kill PID                # Send SIGTERM
kill -9 PID             # Send SIGKILL (force)
pkill -f pattern        # Kill by name/pattern
killall name            # Kill all by name
```

---

## Networking

```bash
curl -X GET https://api.example.com          # GET request
curl -X POST -d '{"key":"value"}' -H "Content-Type: application/json" URL
curl -I URL                                   # Headers only
wget URL                                      # Download file

ping host                # Test connectivity
nc -zv host port         # Test port
lsof -i :3000            # What's using port 3000
netstat -tlnp            # Listening ports
```

---

## Best Practices

1. **Always quote variables**: `"$VAR"` not `$VAR`
2. **Use `set -euo pipefail`** at script start
3. **Use `[[ ]]` over `[ ]`** for tests (more features, safer)
4. **Check command existence**: `command -v cmd >/dev/null 2>&1`
5. **Use `readonly` for constants**
6. **Use `local` in functions**
7. **Quote file paths**: Handle spaces in filenames
