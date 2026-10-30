---
title: "588. 设计内存文件系统"
aliases: ["yiduobo的每日leetcode 588.设计内存文件系统"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/601806380"
zhihu_id: "601806380"
zhihu_title: "yiduobo的每日leetcode 588.设计内存文件系统"
question_id: "588"
question: "设计内存文件系统"
problem_url: "https://leetcode.cn/problems/design-in-memory-file-system/"
created: "2023-01-30T01:01:44+08:00"
updated: "2023-01-30T01:01:44+08:00"
upvotes: 1
comments: 0
---

# 588. 设计内存文件系统

> **[yiduobo的每日leetcode 588.设计内存文件系统](https://zhuanlan.zhihu.com/p/601806380) · 知乎 · 2023-01-30 · 赞同 1**
> 力扣：[588. 设计内存文件系统](https://leetcode.cn/problems/design-in-memory-file-system/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

588.设计内存文件系统

[力扣](https://leetcode.cn/problems/design-in-memory-file-system/)

从linux类系统的角度出发来看，文件系统应该是某种树结构，其中所有的东西都可以认为是文件，因此可以使用树节点来表示单个的文件或者文件夹。当然，在这里也需要一个标记表示当前是文件还是文件夹，因此这个树节点需要四种属性：

1、文件名称

2、是否为文件

3、文件内容，若当前为文件夹时文件内容应该为空

4、子目录内容，若当前为文件时子目录应该为空

而对于题目中的几种操作：

1、初始化：

只需初始化一个根节点root。root应该是文件夹

2、ls：

若path不只是'/'，那么就应该用'/'来分割path，然后从下标1开始遍历分割出来的部分，同时使用一个变量now从root开始逐级向下迭代。来到目标位置后，若now是一个文件，那么答案就是由now的文件名构成的list。若now是一个文件夹，那么就将其子目录中的内容排序后返回

3、mkdir：

与上面类似，使用'/'来分割path，然后从下标1开始遍历分割出来的部分，同样是使用一个now从root开始逐级向下迭代。迭代过程中，若now的childs中不存在当前遍历到部分对应名称的文件夹，那么就在now的childs下新建对应名称的文件夹。

4、addContentToFile：

同样是从root向下迭代，需要注意的是，在迭代的最后一步的目标文件不存在，那么需要新建一个内容为content的文件，若存在，那么就在这个文件末尾加上content

5、readContentFromFile：

还是从root向下迭代，迭代完成后输出文件内容即可

最后附上python代码：

```python
class TreeNode(object):

    def __init__(self, file_name, file_flag, file_content = ""):
        self.file_name = file_name
        self.file_flag = file_flag
        self.file_content = file_content
        self.childs = {}

class FileSystem(object):

    def __init__(self):
        self.root = TreeNode('', False)

    def ls(self, path):
        """
        :type path: str
        :rtype: List[str]
        """

        now = self.root
        if len(path) > 1:
            parts = path.split('/')
            for name in parts[1:]:
                now = now.childs[name]
            
        if now.file_flag:
            return [now.file_name]
        else:
            return sorted(now.childs.keys())

    def mkdir(self, path):
        """
        :type path: str
        :rtype: None
        """

        now = self.root
        parts = path.split('/')
        for name in parts[1:]:
            if name not in now.childs:
                tmp = TreeNode(name, False)
                now.childs[name] = tmp
            
            now = now.childs[name]

    def addContentToFile(self, filePath, content):
        """
        :type filePath: str
        :type content: str
        :rtype: None
        """

        now = self.root
        parts = filePath.split('/')
        for name in parts[1: len(parts) - 1]:
            now = now.childs[name]
        
        if parts[-1] not in now.childs:
            now.childs[parts[-1]] = TreeNode(parts[-1], True, content)
        else:
            now.childs[parts[-1]].file_content += content

    def readContentFromFile(self, filePath):
        """
        :type filePath: str
        :rtype: str
        """

        now = self.root
        parts = filePath.split('/')
        for name in parts[1:]:
            now = now.childs[name]
        
        return now.file_content

# Your FileSystem object will be instantiated and called as such:
# obj = FileSystem()
# param_1 = obj.ls(path)
# obj.mkdir(path)
# obj.addContentToFile(filePath,content)
# param_4 = obj.readContentFromFile(filePath)
```
