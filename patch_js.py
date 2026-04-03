with open("src/js/main.js", "r") as f:
    js_content = f.read()

preloader_logic = """
// Preloader logic
window.addEventListener('load', () => {
    const preloader = document.getElementById('preloader');
    if (preloader) {
        preloader.style.opacity = '0';
        preloader.style.visibility = 'hidden';
        document.body.classList.remove('preloader-active');
        setTimeout(() => {
            preloader.remove();
        }, 600);
    }
});
"""

if "// Preloader logic" not in js_content:
    with open("src/js/main.js", "w") as f:
        f.write(js_content + "\n" + preloader_logic)
        print("Updated main.js with preloader logic")
