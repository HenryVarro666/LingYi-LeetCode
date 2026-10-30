---
title: "428. 序列化和反序列化N叉树"
aliases: ["yiduobo的每日leetcode 428.序列化和反序列化N叉树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/599558773"
zhihu_id: "599558773"
zhihu_title: "yiduobo的每日leetcode 428.序列化和反序列化N叉树"
question_id: "428"
question: "序列化和反序列化N叉树"
problem_url: "https://leetcode.cn/problems/serialize-and-deserialize-n-ary-tree/"
created: "2023-01-17T00:58:36+08:00"
updated: "2023-01-17T00:58:37+08:00"
upvotes: 0
comments: 0
---

# 428. 序列化和反序列化N叉树

> **[yiduobo的每日leetcode 428.序列化和反序列化N叉树](https://zhuanlan.zhihu.com/p/599558773) · 知乎 · 2023-01-17 · 赞同 0**
> 力扣：[428. 序列化和反序列化N叉树](https://leetcode.cn/problems/serialize-and-deserialize-n-ary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

428.序列化和反序列化N叉树

[力扣](https://leetcode.cn/problems/serialize-and-deserialize-n-ary-tree/)

我在这里采用的就是题目描述中给出的序列化方案，不过去除了最外侧的括号对。接下来描述一下序列化和反序列化的过程：

对于以root为根节点的子树，其序列化过程是首先将root.val加入到序列化的结果res中。接下来，若root有孩子节点，那么就在res中加入左括号，然后逐个枚举res的所有孩子节点，递归求解这些孩子节点并将得到的序列化结果也加入到res中，各个孩子节点的序列化结果间需要使用空格来间隔。处理完所有孩子节点后，再往res中添加收尾的右括号即可。

对于data的反序列化，使用一个变量now_root表示当前准备处理的子树的根节点。另外，由于树中节点的数值可能不止一位数，因此还需要使用一个变量now来帮助解析data中的数值。接下来，对data进行一趟遍历，对于当前遍历到的字符char，有以下几种情况：

1、char为数字：

此时应该就使用char来更新now，也就是将now乘以10，然后将char转换为整数添加到now的末尾

2、char为左括号：

左括号的左侧必然是一个数字，其描述的就是val为now的节点tmp，而括号中的内容描述的则是以tmp为根节点的子树。

此时若now_root非空，说明正在描述某棵子树，那么就需要使用某种数据结构将其储存起来，然后再处理tmp，直到tmp处理完成后再继续处理now_root。当然，在这里tmp也可能因为需要处理其某棵子树同样被储存起来，可以发现在这里处理的顺序是先进后出，因此在这里需要使用一个栈来储存尚未处理完的祖先节点。

另外，在这里可以明确tmp是now_root的孩子节点，因此在这里当now_root非空时，需要将tmp加入到now_root.children中，然后将now_root压入栈中，再将now_root更新为tmp。

反过来，当now_root为空时，说明tmp表示的就是整棵树的根节点，此时只需将now_root置为tmp就行了。

无论是哪种情况，now表示的数值已经形成了具体的节点，而now自身应该被清空掉。

3、char为空格：

空格的左侧可能紧挨着一个数字，也有可能是一个右括号。对于后者，不需要做任何处理，而对于前者，也就是now非空的情况，则需要构造出val为now的节点，并将其加入到now_root.children中，然后将now清空。

4、char为右括号：

与情况3相同，右括号的左侧可能紧挨着一个数字，也可能是一个右括号。对于前者，也就是now非空的情况，需要构造出val为now的节点，并将其加入到now_root.children中，然后将now情况。

接下来，右括号表示了now_root这棵子树已经处理完毕了，因此需要从栈中弹出now_root的父亲节点然后返回去继续处理。若此时栈为空，说明now_root描述的是整棵树的根节点，此时直接返回now_root就行了，否则需要将now_root置为栈顶节点，并将栈顶节点弹出。

另外需要注意的是还可能出现一种特殊情况，也就是遍历完data后还没有返回。这种情况下，data中必然不包含任何括号，那么data要么为空，要么就只有一整个数字，表示根节点的val。此时就应该判断data的长度是否为0，若为0，则返回空，否则此时data的值已经被转化成了now，构造一个val为now的节点并返回即可。

最后附上python代码：

```python
"""
# Definition for a Node.
class Node(object):
    def __init__(self, val=None, children=[]):
        self.val = val
        self.children = children
"""

class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string.
        
        :type root: Node
        :rtype: str
        """

        if not root:
            return ''

        first = True
        res = [str(root.val)]
        if len(root.children) > 0:
            res.append('(')
            for child in root.children:
                if first:
                    first = False
                else:
                    res.append(' ')
                res.append(self.serialize(child))
            res.append(')')

        return ''.join(res)
    
    def deserialize(self, data):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: Node
        """
        now = None
        stack = []
        now_root = None

        for char in data:
            if char >= '0' and char <= '9':
                if now is None:
                    now = 0
                now = now * 10 + int(char)
            elif char == '(':
                if now_root is not None:
                    stack.append(now_root)
                    tmp = Node(now, [])
                    now_root.children.append(tmp)
                    now_root = tmp
                else:
                    now_root = Node(now, [])

                now = None
            elif char == ' ':
                if now is not None:
                    now_root.children.append(Node(now, []))
                    now = None
            else:
                if now is not None:
                    now_root.children.append(Node(now, []))
                    now = None
                if stack:
                    now_root = stack.pop()
                else:
                    return now_root
        
        if len(data) == 0:
            return None
        else:
            return Node(now, [])

# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.deserialize(codec.serialize(root))
```
