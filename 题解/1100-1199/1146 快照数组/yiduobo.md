---
title: "1146. 快照数组"
aliases: ["yiduobo的每日leetcode 1146.快照数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/design", "leetcode/hash-table", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/一-二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/377756018"
zhihu_id: "377756018"
zhihu_title: "yiduobo的每日leetcode 1146.快照数组"
question_id: "1146"
question: "快照数组"
problem_url: "https://leetcode.cn/problems/snapshot-array/"
difficulty: "Medium"
rating: 1771
created: "2021-06-03T23:55:15+08:00"
updated: "2021-06-03T23:55:15+08:00"
upvotes: 0
comments: 0
---

# 1146. 快照数组

> **[yiduobo的每日leetcode 1146.快照数组](https://zhuanlan.zhihu.com/p/377756018) · 知乎 · 2021-06-03 · 赞同 0**
> 力扣：[1146. 快照数组](https://leetcode.cn/problems/snapshot-array/) · Medium · 灵茶山艾府：[记录修改历史：哈希表+二分查找（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1146.快照数组

[力扣](https://leetcode-cn.com/problems/snapshot-array/)

由于这里的数组长度和操作轮次都比较大，因此不可能每次执行snap就将当前数组储存起来。一个自然的想法就是我们只储存本轮snap之前产生变化的位置和数值，那么我们需要维护两个二维数组s和v，其中s[index]表示下标为index的数产生改变的snap_id组成的list，而v[index]则表示与s[index]中对应snap_id时刻在index上的数值。那么对于题目中的几种操作而言：

1、set(index, val)

此时我们需要先判断s[index][-1]表示的snap_id是否与当前全局的snap_id一致。若一致，说明修改的就是本轮的数值，那么直接将v[index][-1]置为val即可。若不一致，说明s和v中并没有本轮snap_id对应的数值信息，因此需要将snap_id添加到s[index]的末尾，同时将val添加到v[index]的末尾

2、snap()

此时直接将全局的snap_id加上1即可

3、get(index, snap_id)

对于s[index][p]和s[index][p + 1]而言，其中s[index][p]到s[index][p + 1] - 1这些时间点对应的数值都是v[index][p]，因此在这里我们可以在s[index]中二分查找snap_id，找到对应的s[index][p] \<\= snap_id \< s[index][p + 1]，那么此时对应的结果就是v[index][p]

最后附上python代码：

```python
class SnapshotArray(object):

    def __init__(self, length):
        """
        :type length: int
        """
        self.s = [[0] for _ in range(length)]
        self.v = [[0] for _ in range(length)]
        self.snap_id = 0

    def set(self, index, val):
        """
        :type index: int
        :type val: int
        :rtype: None
        """
        if self.snap_id == self.s[index][-1]:
            self.v[index][-1] = val
        else:
            self.s[index].append(self.snap_id)
            self.v[index].append(val)

    def snap(self):
        """
        :rtype: int
        """
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index, snap_id):
        """
        :type index: int
        :type snap_id: int
        :rtype: int
        """
        tmp = self.s[index]
        if tmp[-1] <= snap_id:
            return self.v[index][-1]
        else:
            l = 0
            r = len(tmp) - 1
            while l < r:
                mid = (l + r + 1) >> 1
                if tmp[mid] <= snap_id:
                    l = mid
                else:
                    r = mid - 1
            return self.v[index][r]

# Your SnapshotArray object will be instantiated and called as such:
# obj = SnapshotArray(length)
# obj.set(index,val)
# param_2 = obj.snap()
# param_3 = obj.get(index,snap_id)
```
