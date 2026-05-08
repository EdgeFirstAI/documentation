# macros.py
import os

def define_env(env):
    show_paths = env.variables.get("show_image_paths", False)

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

    env.macros.figure = figure
    env.macros.img = img
