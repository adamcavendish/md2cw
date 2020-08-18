import argparse
import sys

import mistune


class ConfluenceWikiRender(mistune.HTMLRenderer):
    # Doc: https://confluence.atlassian.com/doc/confluence-wiki-markup-251003035.html
    NAME = 'confluence-wiki'
    IS_TREE = False

    def __init__(self, escape=False, allow_harmful_protocols=None):
        super(ConfluenceWikiRender, self).__init__()
        self._escape = escape
        self._allow_harmful_protocols = allow_harmful_protocols

    def autolink(self, link, is_email=False):
        if is_email:
            return '[mailto:{inner}]'.format(inner=link)
        return '[{inner}]\n'.format(inner=link)

    def block_code(self, code, lang=None):
        # inner = mistune.escape(code)
        return '\n{{code:theme=FadeToGrey|linenumbers=true}}\n{inner}{{code}}\n'.format(inner=code)

    def block_html(self, html):
        raise NotImplementedError('Does not support raw html yet. See confluence macro html')

    def block_quote(self, text):
        return 'bq. {inner}'.format(inner=text)

    def codespan(self, text):
        # inline code text
        # inner = mistune.escape(text)
        return '{{{{{inner}}}}}'.format(inner=text)

    def strong(self, text):
        # strong/bold text
        return '*{inner}*'.format(inner=text)

    def emphasis(self, text):
        return '{{_}}{inner}{{_}}'.format(inner=text)

    def footnote_item(self, key, text):
        return ''

    def footnote_ref(self, key, index):
        return ''

    def footnotes(self, text):
        return ''

    def heading(self, text, level, raw=None):
        assert level >= 1, "heading level >= 1 condition is not met up"
        level = 6 if level > 6 else level
        return '\nh{level}. {inner}\n'.format(level=level, inner=text)

    def hrule(self):
        return '----'

    def image(self, src, title, text):
        return '\n!{inner}|align=center|title={title}|alt={alt}!'.format(inner=src, title=title, alt=text)

    def inline_html(self, html):
        raise NotImplementedError('Does not support raw html yet. See confluence macro html')

    def linebreak(self):
        return '\n\\\\'

    def link(self, link, title, text):
        return '[{title}|{inner}]'.format(title=title, inner=link)

    def list(self, body, ordered, level, start=None):
        bodies = body.strip('\n').split('\n')
        if ordered:
            prefix = '#'
        else:
            prefix = '*'
        bodies = ['{prefix}{inner}'.format(prefix=prefix, inner=inner) for inner in bodies if inner]
        body = '\n'.join(bodies)
        return '\n' + body + '\n'

    def list_item(self, text, level):
        return ' {text}\n'.format(text=text)

    def newline(self):
        return '\n'

    def paragraph(self, text):
        return '\n' + text + '\n'

    def strikethrough(self, text):
        return '-{inner}-'.format(inner=text)

    def table(self, header, body):
        raise NotImplementedError('Does not support raw html yet. See confluence macro html')

    def table_cell(self, content, **flags):
        raise NotImplementedError('Does not support raw html yet. See confluence macro html')

    def table_row(self, content):
        raise NotImplementedError('Does not support raw html yet. See confluence macro html')

    def text(self, text):
        return text

if __name__ == '__main__':
    markdown = mistune.Markdown(
        renderer=ConfluenceWikiRender(),
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('markdown_file', help='a markdown file path or use "-" to use stdin')
    args = parser.parse_args()

    if args.markdown_file == '-':
        source = sys.stdin.read()
    else:
        with open(args.markdown_file, 'r') as f:
            source = f.read()
    output = markdown(source).strip('\n')
    print(output, file=sys.stderr)

