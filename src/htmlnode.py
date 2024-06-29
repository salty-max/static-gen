class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("to_html not implemented for HTMLNode")

    def props_to_html(self):
        props_html = ""
        if self.props == None:
            return ""
        for k, v in self.props.items():
            props_html += f' {k}="{v}"'
        return props_html

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        str = f"ParentNode({self.tag}, ["
        for i in range(len(self.children)):
            str += f"{self.children[i]}"
            if i != len(self.children) - 1:
                str += ", "
        str += f"], {self.props})"
        return str

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Invalid HTML: no children")
        html = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children:
            html += node.to_html()
        html += f"</{self.tag}>"
        return html
