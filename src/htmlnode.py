class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if (self.children == None):
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.children_to_html()}</{self.tag}>"
    def children_to_html(self):
        result_html = ""
        for child in self.children:
            if(child.tag == "code"):
                result_html += child.to_html()
            else:
                
                result_html += child.to_html()
        return result_html

    def props_to_html(self):
        if self.props is None:
            return ""
        keys = self.props.keys()
        result = ""
        for key in keys:
            result += " " + key + "=" + '"' + self.props[key] + '"'
        return result

    def __repr__(self):
        return f"tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}\n"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag == "" or self.tag == None:
            if self.props == None:
                return self.value
            else:
                raise ValueError("Cannot have props with no tag")
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None or self.tag.strip() == "":
            raise ValueError("Missing tag")
        if self.children == None or len(self.children) == 0:
            raise ValueError("Missing children")
        htmlChildren = ""
        for child in self.children:
            htmlChildren += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{htmlChildren}</{self.tag}>"