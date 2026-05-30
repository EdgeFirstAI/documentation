# EdgeFirst Documentation

The EdgeFirst Documentation provides tutorials and information related to EdgeFirst Studio, Middleware, and Platforms.

# Deployment

## MkDocs
Follow these steps for deploying the documentation locally on your machine.

`pip install -r requirements.txt`

`mkdocs serve`

You should now be able to see the documentation on your browser by visiting this link `http://localhost:8000/`.

## Mike

**Alternatively**, use `mike` which is typically used for extra verification that the links are not broken.

`mike deploy -r <git branch> <version> <alias>` [Example: `mike deploy -r DE-1941-doc-fixes v1.0 testing-v1.0`]

`mike set-default <version>` [Example: `mike set-default v1.0`]

Once deployed, run `mike serve` and access the documentation in this link `http://localhost:8000/v1.0/`.

This will create a local branch for the documentation that will show like the following below.

![Local Deployed Documentation](docs/assets/mike-deploy-local.jpg)

To delete the local branches that's created, run `mike delete <identifier>` [Example: `mike delete DE-1941-doc-fixes`]

More information for using `mike` can be found [here](https://github.com/jimporter/mike?tab=readme-ov-file#building-your-docs).

## Spell Check

Run a spell checker on the documentation using `mkdocs build -s`.

## Discrete Documentations

Discrete documentations allow a single doc file to appear in multiple locations.  The doc file needs to be maintained once and the changes will be propagated in all pages that contains the doc file. All discrete documentations are placed under the directory `/discrete`.  The syntax for adding the contents of the discrete doc in another doc is provided below.

Example: `{% include-markdown "discrete/workflows/web.md" %}`

# Conventions

Follow these conventions when working on the documentation.

1. Filenames should be lower case. Avoid a name like "Projects" for files and directories for example.
2. Keep images in an `assets` folder for better organization.
3. Use well descriptive names for the images. Avoid a name like "image-1" for example.
4. Either keep assets as a sub-folder to where the documentation using these assets lives, or a sub-folder of the root assets with the same hierarchy (former is currently being followed).
5. Do NOT use screenshots from private customer data in the documentation. We should be using our own custom datasets. Exception would be documentation for a specific dataset such as COCO.
6. Avoid any unused images in the assets folder. Any unused images should be removed.
7. Typically images are rendered by using the macro `figure()` with a caption and center alignment as shown. This will also expose the image path to show via mouse hover as explained in point 8.

    ```
    {{ figure("/studio/assets/user/signup-page.jpg", "Create a New Account") }}
    ```

    Otherwise, standalone images with no captions or center alignment can either use the `img()` macro or the `![Alt Text](/path/to/image.jpg)` syntax.

    ```
    {{ img("/studio/assets/user/signup-page.jpg", "Create a New Account") }}
    ```

8. For production set `show_image_paths: false` under mkdocs.yml `extra: `. This will prevent the image path from being shown upon mouse hover in the docs which is used mostly for development process to ease the replacement of images.
9. The site [remove.bg](https://www.remove.bg/) was used to remove the background from the platform screenshots.
10. [Greenshot software](https://getgreenshot.org/) was used to take screenshots and image annotations in this documentation.
11. For deployment across different stages (test/stage/saas) ensure the following links are updated under [macros.py](macros.py).

    ```python
    studio_urls = {
        "studio": "https://edgefirst.studio/",
        "signup": "https://edgefirst.studio/signup",
        "login": "https://edgefirst.studio/login",
        "price": "https://edgefirst.studio/price",
    }
    ```

    The syntax for using these links in the documentation is as follows `{{ studio_link("text", "key") }}`

    ```
    {{ studio_link("EdgeFirst Studio") }}
    {{ studio_link("sign up", "signup") }}
    {{ studio_link("login", "login") }}
    {{ studio_link("price", "price") }}
    {{ studio_link("Public Project", "project") }}
    ```

# Reusable Components

Reusable UI components are defined in [docs/stylesheets/components.css](docs/stylesheets/components.css) and registered under `extra_css` in [mkdocs.yml](mkdocs.yml). They can be used anywhere in the documentation, including page content, headings, and navigation titles in `.nav.yml`.

## Badge

The `ef-badge` is a small pill label with a periodic shine sweep, useful for flagging new, beta, or preview features. Drop a `<span>` with the `ef-badge` class anywhere inline:

```html
<span class="ef-badge">New</span>
```

Color variants are available by adding a modifier class (the default is gold):

```html
<span class="ef-badge ef-badge--teal">Beta</span>
<span class="ef-badge ef-badge--navy">Preview</span>
```

Notes:

- The badge is sized in `em`, so it scales with the surrounding text and can follow a word or heading.
- For navigation titles in `.nav.yml`, wrap the entry in single quotes so the embedded HTML parses correctly, for example `'Profiler <span class="ef-badge">New</span>': profiler`.
- The shine animation is automatically disabled for users who have enabled the `prefers-reduced-motion` accessibility setting.