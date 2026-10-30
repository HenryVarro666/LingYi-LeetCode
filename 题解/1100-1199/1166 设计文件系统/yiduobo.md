---
title: "1166. 设计文件系统"
aliases: ["yiduobo的每日leetcode 1166.设计文件系统"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/611364455"
zhihu_id: "611364455"
zhihu_title: "yiduobo的每日leetcode 1166.设计文件系统"
question_id: "1166"
question: "设计文件系统"
problem_url: "https://leetcode.cn/problems/design-file-system/"
created: "2023-03-04T21:47:27+08:00"
updated: "2023-03-04T21:47:27+08:00"
upvotes: 0
comments: 0
---

# 1166. 设计文件系统

> **[yiduobo的每日leetcode 1166.设计文件系统](https://zhuanlan.zhihu.com/p/611364455) · 知乎 · 2023-03-04 · 赞同 0**
> 力扣：[1166. 设计文件系统](https://leetcode.cn/problems/design-file-system/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1166.设计文件系统

[力扣](https://leetcode.cn/problems/design-file-system/)

非常标准的trie树的问题，使用trie树中的节点表示文件系统中的文件夹或者文件。为了记录文件的内容，除了常规trie树的孩子节点之外还需要额外添加一个变量记录当前节点的文件内容，接下来就是常规的trie树操作了。

最后附上python代码：

```python
class Node(object):

    def __init__(self):
        self.childs = {}
        self.v = None

class FileSystem(object):

    def __init__(self):
        self.root = Node()

    def createPath(self, path, value):
        """
        :type path: str
        :type value: int
        :rtype: bool
        """
        parts = path.split('/')
        now = self.root
        for part in parts[1:len(parts) - 1]:
            if part not in now.childs:
                return False
            now = now.childs[part]
        
        if parts[-1] in now.childs:
            return False
        
        node = Node()
        node.v = value
        now.childs[parts[-1]] = node
        return True

    def get(self, path):
        """
        :type path: str
        :rtype: int
        """
        parts = path.split('/')
        now = self.root
        for part in parts[1:]:
            if part not in now.childs:
                return -1
            now = now.childs[part]
        
        return now.v

# Your FileSystem object will be instantiated and called as such:
# obj = FileSystem()
# param_1 = obj.createPath(path,value)
# param_2 = obj.get(path)
```
