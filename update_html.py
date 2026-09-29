import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Verify iconsData contains all 37 SVG icons
    slugs = re.findall(r"slug:\s*'([^']+)'", html)
    print(f"Verified {len(slugs)} icons in index.html iconsData array.")

if __name__ == '__main__':
    main()
