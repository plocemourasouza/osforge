#!/usr/bin/env python3
"""
Extract metadata from all SKILL.md files and generate index files.
"""
import os
import json
import re
from pathlib import Path

BASE = Path(os.path.expanduser("~/Development/osforge"))

SOURCE_LABELS = {
    "01-anthropic": {"label": "Anthropic (Oficial)", "emoji": "🟣", "url": "https://github.com/anthropics/skills"},
    "02-superpowers": {"label": "Superpowers (obra)", "emoji": "🔵", "url": "https://github.com/obra/superpowers"},
    "03-claude-mem": {"label": "Claude-Mem", "emoji": "🧠", "url": "https://github.com/thedotmack/claude-mem"},
    "04-vercel": {"label": "Vercel Labs", "emoji": "🟢", "url": "https://github.com/vercel-labs/agent-skills"},
    "05-context-engineering": {"label": "Context Engineering", "emoji": "📐", "url": "https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering"},
    "06-antigravity": {"label": "Antigravity (634+)", "emoji": "🌌", "url": "https://github.com/sickn33/antigravity-awesome-skills"},
    "07-trailofbits": {"label": "Trail of Bits", "emoji": "🔒", "url": "https://github.com/trailofbits/skills"},
    "08-supabase": {"label": "Supabase", "emoji": "🟩", "url": "https://github.com/supabase/agent-skills"},
    "09-expo": {"label": "Expo", "emoji": "📱", "url": "https://github.com/expo/skills"},
    "10-cloudflare": {"label": "Cloudflare", "emoji": "☁️", "url": "https://github.com/cloudflare/skills"},
    "11-sentry": {"label": "Sentry", "emoji": "🔴", "url": "https://github.com/getsentry/skills"},
    "12-curadoria": {"label": "Curadoria", "emoji": "📋", "url": ""},
    "13-claude-red": {"label": "Claude-Red (Offensive Security)", "emoji": "🛡️", "url": "https://github.com/SnailSploit/Claude-Red"},
}

def extract_frontmatter(content):
    name, desc = "", ""
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return name, desc
    
    fm = fm_match.group(1)
    
    # Name
    m = re.search(r'^name:\s*["\']?([^"\'#\n]+)["\']?\s*$', fm, re.MULTILINE)
    if m:
        name = m.group(1).strip()
    
    # Description - try single line first
    m = re.search(r'^description:\s*["\'](.+?)["\']', fm, re.MULTILINE)
    if m:
        desc = m.group(1).strip()
    else:
        m = re.search(r'^description:\s*(.+?)$', fm, re.MULTILINE)
        if m:
            val = m.group(1).strip()
            if val in ('|', '>', '|+', '>-'):
                # Multi-line: grab next lines until next key or end
                idx = fm.find(m.group(0))
                rest = fm[idx + len(m.group(0)):]
                lines = []
                for line in rest.split('\n'):
                    if line and not line[0].isspace() and ':' in line:
                        break
                    lines.append(line.strip())
                desc = ' '.join(l for l in lines if l)
            else:
                desc = val
    
    desc = re.sub(r'\s+', ' ', desc).strip()
    # Remove trailing quotes
    desc = desc.strip('"').strip("'")
    return name, desc

def extract_first_paragraph(content):
    # Remove frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n?', '', content, flags=re.DOTALL)
    lines = content.strip().split('\n')
    para = []
    for line in lines:
        line = line.strip()
        if not line:
            if para:
                break
            continue
        if line.startswith('#'):
            if para:
                break
            continue
        if line.startswith('<!--') or line.startswith('```') or line.startswith('|'):
            if para:
                break
            continue
        para.append(line)
    
    text = ' '.join(para)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'[*_`]', '', text)
    return text[:300].strip()

def categorize_skill(name, desc, path_str):
    """Auto-categorize based on keywords."""
    text = f"{name} {desc} {path_str}".lower()
    
    categories = {
        "🔒 Security": ["security", "vuln", "audit", "pentest", "owasp", "scanner", "apk", "firewall", "waf", "xss", "sqli", "injection", "exploit", "malware", "yara", "burp", "semgrep", "codeql", "fuzzing", "fuzz", "sanitizer", "constant-time", "secure-contract", "insecure"],
        "🧪 Testing": ["test", "tdd", "coverage", "playwright", "e2e", "property-based", "spec-to-code"],
        "⚛️ React / Frontend": ["react", "next.js", "nextjs", "frontend", "tailwind", "css", "ui-ux", "web-design", "composition", "component", "shadcn", "html", "dom", "animation"],
        "📱 Mobile": ["expo", "react-native", "ios", "android", "mobile", "flutter", "swift"],
        "🗄️ Database / Backend": ["postgres", "sql", "database", "prisma", "supabase", "django", "rails", "api-design", "graphql", "rest-api"],
        "☁️ Infrastructure / DevOps": ["docker", "kubernetes", "aws", "cloud", "terraform", "ci/cd", "deploy", "vercel", "cloudflare", "worker", "serverless", "wrangler", "nginx", "infra"],
        "🤖 AI / ML / Agents": ["agent", "llm", "ai-", "ml-", "rag", "prompt", "context", "memory", "model", "embedding", "vector", "langchain", "langgraph", "hugging", "inference", "evaluation", "bdi"],
        "🏗️ Architecture": ["architect", "system-design", "c4", "adr", "pattern", "microservice", "monorepo", "event-driven", "domain-driven"],
        "📝 Documentation / Writing": ["doc", "writing", "readme", "changelog", "internal-comms", "brand", "copywriting", "content"],
        "🔄 Workflow / Process": ["brainstorm", "plan", "execute", "review", "git", "commit", "pr", "workflow", "agile", "scrum", "kanban"],
        "💼 Business / Marketing": ["seo", "marketing", "pricing", "growth", "analytics", "ads", "crm", "sales"],
        "🎨 Design / Creative": ["art", "design", "canvas", "gif", "theme", "image", "video", "3d", "svg"],
        "🐍 Languages / Frameworks": ["python", "typescript", "rust", "golang", "java", "ruby", "angular", "vue", "svelte", "php", "csharp"],
    }
    
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw in text:
                return cat
    
    return "📦 General"

def main():
    skills = []
    skill_files = sorted(BASE.rglob("SKILL.md"))
    
    for sf in skill_files:
        rel = sf.relative_to(BASE)
        parts = list(rel.parts)
        
        if len(parts) < 2:
            continue
            
        source_folder = parts[0]
        if source_folder.startswith("_"):
            continue
        
        skill_dir = sf.parent.name
        skill_path = str(rel.parent)
        
        try:
            content = sf.read_text(encoding='utf-8', errors='replace')
        except:
            continue
        
        name, desc = extract_frontmatter(content)
        
        if not desc:
            desc = extract_first_paragraph(content)
        
        if not name:
            name = skill_dir
        
        # Truncate
        desc = desc[:300]
        
        source_info = SOURCE_LABELS.get(source_folder, {"label": source_folder, "emoji": "📦", "url": ""})
        category = categorize_skill(name, desc, skill_path)
        
        skills.append({
            "name": name,
            "description": desc,
            "category": category,
            "source": source_info["label"],
            "source_emoji": source_info["emoji"],
            "source_url": source_info["url"],
            "local_path": skill_path,
            "skill_dir": skill_dir,
        })
    
    # Write JSON index
    json_path = BASE / "INDICE-SKILLS.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(skills, f, ensure_ascii=False, indent=2)
    
    print(f"Total: {len(skills)} skills indexed")
    print(f"JSON: {json_path}")
    
    # Category stats
    cats = {}
    for s in skills:
        c = s["category"]
        cats[c] = cats.get(c, 0) + 1
    
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")

if __name__ == "__main__":
    main()
