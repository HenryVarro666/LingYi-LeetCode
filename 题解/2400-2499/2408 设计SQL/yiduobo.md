---
title: "2408. 设计SQL"
aliases: ["yiduobo的每日leetcode 2408.设计SQL"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/631062257"
zhihu_id: "631062257"
zhihu_title: "yiduobo的每日leetcode 2408.设计SQL"
question_id: "2408"
question: "设计SQL"
problem_url: "https://leetcode.cn/problems/design-sql/"
created: "2023-05-21T22:25:49+08:00"
updated: "2023-05-21T22:25:49+08:00"
upvotes: 0
comments: 0
---

# 2408. 设计SQL

> **[yiduobo的每日leetcode 2408.设计SQL](https://zhuanlan.zhihu.com/p/631062257) · 知乎 · 2023-05-21 · 赞同 0**
> 力扣：[2408. 设计SQL](https://leetcode.cn/problems/design-sql/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2408.设计SQL

[力扣](https://leetcode.cn/problems/design-sql/)

题目主要需要实现几个操作：

1、通过表名找到对应的表：

直接使用哈希表建立表名到表的映射即可

2、向指定表的末尾插入一行：

既然是在末尾插入，那么使用list记录表中的行是比较适合的

3、删去指定表中的某一行：

题目中的删除操作执行后，后续行的行数并不会向前移动，因此在这里可以不执行真正的删除，而是记录下哪些行被删去就行了。那么在这里可以使用一个set记录被删去的行

4、查询指定表中某一行的某一列：

首先通过操作1中的哈希表找到对应的表，然后判断查询的行是否存在，再判断查询的列是否存在即可

综合起来，就是对于单张表，需要使用一个list记录其中的行，使用一个set记录该表中被删去的行。而对于所有的表，则都需要使用哈希表建立表名到表的联系。

最后附上python代码：

```python
class Table(object):

    def __init__(self):
        self.rows = []
        self.removed = set()

class SQL(object):

    def __init__(self, names, columns):
        """
        :type names: List[str]
        :type columns: List[int]
        """
        self.tables = {}
        for name in names:
            self.tables[name] = Table()

    def insertRow(self, name, row):
        """
        :type name: str
        :type row: List[str]
        :rtype: None
        """
        t = self.tables[name]
        t.rows.append(row)

    def deleteRow(self, name, rowId):
        """
        :type name: str
        :type rowId: int
        :rtype: None
        """
        t = self.tables[name]
        t.removed.add(rowId)

    def selectCell(self, name, rowId, columnId):
        """
        :type name: str
        :type rowId: int
        :type columnId: int
        :rtype: str
        """
        if name not in self.tables:
            return ""
            
        t = self.tables[name]
        if rowId in t.removed or rowId > len(t.rows):
            return ""

        if columnId > len(t.rows[rowId - 1]):
            return ""
        
        return t.rows[rowId - 1][columnId - 1]

# Your SQL object will be instantiated and called as such:
# obj = SQL(names, columns)
# obj.insertRow(name,row)
# obj.deleteRow(name,rowId)
# param_3 = obj.selectCell(name,rowId,columnId)
```
