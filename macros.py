# macros.py
import os

def define_env(env):
    show_paths = env.variables.get("show_image_paths", False)
    studio_urls = {
        "studio": "https://stage.edgefirst.studio/",
        "signup": "https://stage.edgefirst.studio/signup",
        "login": "https://stage.edgefirst.studio/login",
        "price": "https://stage.edgefirst.studio/price",
        "project": "https://stage.edgefirst.studio/public/projects",
    }

    def resolve_path(path, page):        
        full_path = path
        if path.startswith("/"):    
            page_dir = os.path.dirname(page.file.src_path)
            docs_relative = path.lstrip("/")
            full_path = os.path.relpath(docs_relative, page_dir)
            full_path = full_path.replace(os.sep, "/")
        return full_path

    def img(path, alt):
        if show_paths:
            return f'![{alt}]({path} "{path}")'
        return f'![{alt}]({path})'
    
    def figure(path, alt, width=None):
        """Return a figure HTML block with image and caption."""
        page = env.page
        path = resolve_path(path, page)

        tooltip = f' "{path}"' if show_paths else ""
        if width is None:
            return \
            f'''<figure markdown="span">
            ![{alt}]({path}{tooltip}){{ align=center }}
            <figcaption>{alt}</figcaption>
            </figure>'''
        else:
            return \
            f'''<figure markdown="span">
            ![{alt}]({path}{tooltip}){{ align=center width={width} }}
            <figcaption>{alt}</figcaption>
            </figure>'''
        
    def studio_url(name="studio"):
        """Return a shared EdgeFirst Studio URL by key."""
        if name not in studio_urls.keys():
            raise ValueError(f"Unknown studio URL key: {name}")
        return studio_urls[name]

    def studio_link(text, name="studio"):
        """Return an HTML anchor for a shared EdgeFirst Studio URL."""
        return f'<a href="{studio_url(name)}">{text}</a>'

    env.macros.figure = figure
    env.macros.img = img
    env.macros.studio_url = studio_url
    env.macros.studio_link = studio_link
