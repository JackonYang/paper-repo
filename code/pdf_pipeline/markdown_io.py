import codecs

from jinja2 import Environment, FileSystemLoader


def render_md(template_dir, template_name, data, out_filename):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)

    content = template.render(data)

    with codecs.open(out_filename, 'w', 'utf8') as f:
        f.write(content)
