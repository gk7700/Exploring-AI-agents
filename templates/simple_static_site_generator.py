import os
import markdown
import shutil

CONTENT_DIR = "content"
TEMPLATES_DIR = "templates"
OUTPUT_DIR = "site"
STATIC_DIR = "static"

def load_template(template_name):
    path = os.path.join(TEMPLATES_DIR, template_name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def build_page(content_file, template, site_name="My Site"):
    with open(content_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Front matter support (--- at top)
    meta = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            _, meta_text, body = parts
            for line in meta_text.strip().split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    meta[key.strip()] = value.strip()

    html_content = markdown.markdown(body, extensions=["fenced_code", "tables"])
    title = meta.get("title", "Untitled Page")
    template_html = load_template(meta.get("template", template))
    page = template_html.replace("${title}", title)
    page = page.replace("${content}", html_content)
    page = page.replace("${site_name}", site_name)
    return page, meta

def build_site():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # Copy static assets if they exist
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, os.path.join(OUTPUT_DIR, STATIC_DIR))

    # Process markdown files
    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith(".md"):
            content_file = os.path.join(CONTENT_DIR, filename)
            html, meta = build_page(content_file, "default.html")

            out_name = filename.replace(".md", ".html")
            out_path = os.path.join(OUTPUT_DIR, out_name)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Built {out_path}")

if __name__ == "__main__":
    build_site()
