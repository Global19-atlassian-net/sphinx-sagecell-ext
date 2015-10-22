# -*- coding: utf-8 -*-

from docutils.nodes import Element, General
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive

class sagecell(General, Element):
    pass

class SageCell(Directive):

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        "linked": directives.unchanged
    }

    def run(self):

        if "linked" in self.options:
            linked = self.options.get("linked")
        else:
            linked = None # TODO: sagecell_default_linked var from conf.py
        content = "\n".join(self.content)
        node = sagecell()
        node['content'] = content
        node['linked'] = linked
        return [node]

def visit_sagecell_node(self, node):

    if node['linked'] == "true":
        self.body.append("<div class='sage_linked'>")
    elif node['linked'] == "false":
        self.body.append("<div class='sage_unlinked'>")
    else:
        pass # TODO sagecell_default_linked var from conf.py
    self.body.append("<script type='text/x-sage'>")
    self.body.append(node['content'])
    self.body.append("</script>")
    self.body.append("</div>")


def depart_sagecell_node(self, node):
    pass

def setup(app):

    # Register a configuration value
    app.add_config_value('sagecell_default_linked', True, 'html')
    # Register a Docutils node class
    app.add_node(sagecell,
                 html=(visit_sagecell_node, depart_sagecell_node))
    # Register a Docutils directive
    app.add_directive("sagecell", SageCell)
