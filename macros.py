# macros.py
def define_env(env):
    def img(path, alt):
        if env.variables.get("show_image_paths"):
            return f'![{alt}]({path} "{path}")'
        return f'![{alt}]({path})'
    env.macros.img = img