---
title: "715. range模块"
aliases: ["yiduobo的每日leetcode 715.range模块"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/330875328"
zhihu_id: "330875328"
zhihu_title: "yiduobo的每日leetcode 715.range模块"
question_id: "715"
question: "range模块"
problem_url: "https://leetcode.cn/problems/range-module/"
created: "2020-12-04T23:17:05+08:00"
updated: "2020-12-04T23:17:05+08:00"
upvotes: 0
comments: 0
---

# 715. range模块

> **[yiduobo的每日leetcode 715.range模块](https://zhuanlan.zhihu.com/p/330875328) · 知乎 · 2020-12-04 · 赞同 0**
> 力扣：[715. range模块](https://leetcode.cn/problems/range-module/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

715.range模块

[力扣](https://leetcode-cn.com/problems/range-module/)

动态区间的修改与查找的问题，注意到这里必须使用在线算法，因此离散化加线段树的做法就行不通了。当然，由于查询数量有限，直接通过树节点的方式建立线段树也是可以勉强通过的，不过最好的做法还是平衡二叉树。

我在这里用了比较偷懒的做法，没有使用任何高级数据结构，直接用数组来维护当前所有的区间，然后线性查找当前加入或删去的区间的左右边界位于现有的哪两个区间当中，然后执行区间合并或拆分的操作。

最后附上python代码：

```python
class RangeModule(object):

    def __init__(self):
        self.f = []

    def addRange(self, left, right):
        """
        :type left: int
        :type right: int
        :rtype: None
        """
        #print 'add %d %d' % (left, right)
        if not self.f:
            self.f = [[left, right]]
            #print self.f
        else:
            l = 0
            while l < len(self.f) and self.f[l][1] < left:
                l += 1
            
            if l == len(self.f):
                self.f.append([left, right])
                #print self.f
                return
            
            r = l
            while r < len(self.f) and self.f[r][0] <= right:
                r += 1
            
            if r == 0:
                self.f = [[left, right]] + self.f
            else:
                r -= 1
                left = min(left, self.f[l][0])
                right = max(right, self.f[r][1])
                self.f = self.f[:l] + [[left, right]] + self.f[r + 1:]
            #print self.f

    def queryRange(self, left, right):
        """
        :type left: int
        :type right: int
        :rtype: bool
        """
        for index in range(len(self.f)):
            if self.f[index][0] <= left and self.f[index][1] >= right:
                return True

        return False

    def removeRange(self, left, right):
        """
        :type left: int
        :type right: int
        :rtype: None
        """
        #print 'remove %d %d' % (left, right)
        if not self.f:
            return

        l = 0
        while l < len(self.f) and self.f[l][1] <= left:
            l += 1
        
        if (l == 0 and right <= self.f[l][0]) or (l == len(self.f)):
            #print self.f
            return
        
        r = l
        while r < len(self.f) and self.f[r][0] < right:
            r += 1
        
        r -= 1
        tmp = []
        if left > self.f[l][0]:
            tmp.append([self.f[l][0], left])
        if right < self.f[r][1]:
            tmp.append([right, self.f[r][1]])
        
        self.f = self.f[:l] + tmp + self.f[r + 1:]
        #print self.f

# Your RangeModule object will be instantiated and called as such:
# obj = RangeModule()
# obj.addRange(left,right)
# param_2 = obj.queryRange(left,right)
# obj.removeRange(left,right)
```
