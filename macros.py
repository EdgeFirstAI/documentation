# macros.py
import os

from mkdocs.utils import get_relative_url

def define_env(env):
    show_paths = env.variables.get("show_image_paths", False)
    studio_urls = {
        "studio": "https://test.edgefirst.studio/",
        "signup": "https://test.edgefirst.studio/signup",
        "login": "https://test.edgefirst.studio/login",
        "price": "https://test.edgefirst.studio/price",
        "project": "https://test.edgefirst.studio/public/projects",
    }

    def resolve_path(path, page):        
        full_path = path
        if path.startswith("/"):    
            page_dir = os.path.dirname(page.file.src_path)
            docs_relative = path.lstrip("/")
            full_path = os.path.relpath(docs_relative, page_dir)
            full_path = full_path.replace(os.sep, "/")
        return full_path
    
    def doc_path_of(path, page):
        """Resolve an asset reference to its docs-root-relative path.

        Accepts an absolute (``/foo/bar.mp4``) or page-relative
        (``../foo/bar.mp4``) reference and returns the normalized path
        relative to the docs root (e.g. ``foo/bar.mp4``).
        """
        if path.startswith("/"):
            return path.lstrip("/")
        page_dir = os.path.dirname(page.file.src_path)
        resolved = os.path.normpath(os.path.join(page_dir, path))
        return resolved.replace(os.sep, "/")

    def img(path, alt):
        page = env.page
        path = resolve_path(path, page)
        
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

    def video(path, alt, width=None):
        """Return an autoplaying, looping, muted inline video that behaves
        like a GIF.

        The source is resolved relative to the rendered page URL (via
        MkDocs' get_relative_url) so it works under use_directory_urls and
        the versioned (mike) deployment. Unlike <img> tags, MkDocs does not
        rewrite raw <source> URLs, so resolve_path (which is relative to the
        source file directory) cannot be reused here.
        """
        page = env.page
        src = get_relative_url(doc_path_of(path, page), page.url)

        style = f' style="width:{width}"' if width is not None else ""
        return (
            f'<figure markdown="span">\n'
            f'<video autoplay loop muted playsinline{style}>\n'
            f'<source src="{src}" type="video/mp4">\n'
            f'{alt}\n'
            f'</video>\n'
            f'<figcaption>{alt}</figcaption>\n'
            f'</figure>'
        )

    def studio_url(name="studio"):
        """Return a shared EdgeFirst Studio URL by key."""
        if name not in studio_urls.keys():
            raise ValueError(f"Unknown studio URL key: {name}")
        return studio_urls[name]

    def studio_link(text, name="studio"):
        """Return an HTML anchor for a shared EdgeFirst Studio URL."""
        return f'<a href="{studio_url(name)}">{text}</a>'

    env.macros.figure = figure
    env.macros.video = video
    env.macros.img = img
    env.macros.studio_url = studio_url
    env.macros.studio_link = studio_link
