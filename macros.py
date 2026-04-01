# macros.py
def define_env(env):
    show_paths = env.variables.get("show_image_paths", False)

    def img(path, alt):
        if show_paths:
            return f'![{alt}]({path} "{path}")'
        return f'![{alt}]({path})'
    
    def figure(path, alt, width=None):
        """Return a figure HTML block with image and caption."""
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
