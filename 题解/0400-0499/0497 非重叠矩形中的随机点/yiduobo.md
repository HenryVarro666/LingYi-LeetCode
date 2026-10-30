---
title: "497. 非重叠矩形中的随机点"
aliases: ["yiduobo的每日leetcode 497.非重叠矩形中的随机点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/257311402"
zhihu_id: "257311402"
zhihu_title: "yiduobo的每日leetcode 497.非重叠矩形中的随机点"
question_id: "497"
question: "非重叠矩形中的随机点"
problem_url: "https://leetcode.cn/problems/random-point-in-non-overlapping-rectangles/"
created: "2020-09-21T21:37:45+08:00"
updated: "2020-09-21T21:37:45+08:00"
upvotes: 0
comments: 0
---

# 497. 非重叠矩形中的随机点

> **[yiduobo的每日leetcode 497.非重叠矩形中的随机点](https://zhuanlan.zhihu.com/p/257311402) · 知乎 · 2020-09-21 · 赞同 0**
> 力扣：[497. 非重叠矩形中的随机点](https://leetcode.cn/problems/random-point-in-non-overlapping-rectangles/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

497.非重叠矩形中的随机点<https://leetcode-cn.com/problems/random-point-in-non-overlapping-rectangles/>

注意到题目是非重叠矩形，那么矩形覆盖的总面积就是各个矩形的面积之和。设面积和为sum，那么我们可以将矩形中的所有点按0到sum - 1进行编号，然后每次从0到sum - 1中随机出一个数，返回对应的点即可。

设第k个矩形的面积是areak，那么第0个矩形将使用0到area0 - 1这些编号，第1个矩形将使用area0到area0 + area1 - 1这些编号，依次类推。注意到每个矩形的编号起点都是矩形面积的前缀和，而这个前缀和必然是单调递增的，因此可以优先预处理出area的前缀和数组，然后在里面进行二分确定rand是位于哪两个area之间，即rand应该属于哪个矩形。

设我们通过二分求出rand位于第m个矩形中，那么其应该对应矩形中的第k - sum_list[m - 1]个点，此时只需要确定对矩形的编码方式即可。一种可行的方案是按照第i行第j列的编号为i \* col + j这种方式进行编码，那么此时k - sum_list[m - 1]除以col以及模col就能确定i和j了。

最后附上python代码：

```python
class Solution(object):

    def __init__(self, rects):
        """
        :type rects: List[List[int]]
        """
        self.sum_list = []
        self.col_list = []
        self.point_list = []
        for rect in rects:
            x1, y1, x2, y2 = rect
            self.col_list.append(y2 - y1 + 1)
            self.point_list.append([x1, y1])
            area = (x2 - x1 + 1) * (y2 - y1 + 1)
            if not self.sum_list:
                self.sum_list.append(area)
            else:
                self.sum_list.append(self.sum_list[-1] + area)

    def pick(self):
        """
        :rtype: List[int]
        """
        pos = random.randint(0, self.sum_list[-1] - 1)
        l = 0
        r = len(self.sum_list) - 1
        while l < r:
            mid = (l + r) / 2
            if pos >= self.sum_list[mid]:
                l = mid + 1
            else:
                r = mid
        
        if l > 0:
            pos -= self.sum_list[l - 1]
        return self.point_list[l][0] + pos / self.col_list[l], self.point_list[l][1] + pos % self.col_list[l]

# Your Solution object will be instantiated and called as such:
# obj = Solution(rects)
# param_1 = obj.pick()
```
