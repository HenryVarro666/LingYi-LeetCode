---
title: "519. 随机翻转矩阵"
aliases: ["yiduobo的每日leetcode 519.随机翻转矩阵"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/260813840"
zhihu_id: "260813840"
zhihu_title: "yiduobo的每日leetcode 519.随机翻转矩阵"
question_id: "519"
question: "随机翻转矩阵"
problem_url: "https://leetcode.cn/problems/random-flip-matrix/"
created: "2020-09-30T20:58:12+08:00"
updated: "2020-09-30T20:58:12+08:00"
upvotes: 0
comments: 0
---

# 519. 随机翻转矩阵

> **[yiduobo的每日leetcode 519.随机翻转矩阵](https://zhuanlan.zhihu.com/p/260813840) · 知乎 · 2020-09-30 · 赞同 0**
> 力扣：[519. 随机翻转矩阵](https://leetcode.cn/problems/random-flip-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

519.随机翻转矩阵<https://leetcode-cn.com/problems/random-flip-matrix/>

题目要求从矩阵中没有使用过的点随机选一个，相当于一共有n个数，第一轮从这n个数中随机选一个，第二轮从剩下的n - 1个数中随机选一个，依次类推。

现在问题的难点主要在于如果每次都从1到n中随机选，然后判断是否被选过，那么随着剩下的数逐渐减少，需要尝试的次数就越多。

一个自然的想法是每次就从剩下的数中随机选一个，即用某种数据结构维护剩下的数，然后每次从中间随机选一个之后再将其从数据结构中剔除。遗憾的是，这里数的规模可能达到10000的平方也就是一亿，全部储存起来对空间的要求就比较高了。

另一个想法就是从堆这种数据结构找灵感。首先第一轮，应该是从1到n中随机选一个数，不妨设其为p。在得到p之后，我们将这个数映射到第n个数上，即我们接下来第二轮的随机选取中，我们只从1到n - 1中随机如果随机到了p，那么我们就认为这是n，接下来将第二轮的数映射到n - 1，然后第三轮就从1到n - 2中进行随机。

需要注意的是，当前这一轮随机的右边界x有可能已经在之前的随机中被使用过了，那么这一轮的p的映射需要多跳一次，即p应该映射到x的映射上。

这样一来，每一轮就只需要进行一次随机操作了，而对于复位操作，则重置随机的右边界，同时清空映射表即可。

最后附上python代码：

```python
class Solution(object):

    def __init__(self, n_rows, n_cols):
        """
        :type n_rows: int
        :type n_cols: int
        """
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.tot = n_rows * n_cols
        self.pos_dict = {}

    def flip(self):
        """
        :rtype: List[int]
        """
        self.tot -= 1
        pos = random.randint(0, self.tot)
        if pos in self.pos_dict:
            real_pos = self.pos_dict[pos]
        else:
            real_pos = pos
        
        if self.tot in self.pos_dict:
            self.pos_dict[pos] = self.pos_dict[self.tot]
        else:
            self.pos_dict[pos] = self.tot

        self.pos_dict[self.tot] = real_pos

        return real_pos / self.n_cols, real_pos % self.n_cols

    def reset(self):
        """
        :rtype: None
        """
        self.pos_dict = {}
        self.tot = self.n_rows * self.n_cols

# Your Solution object will be instantiated and called as such:
# obj = Solution(n_rows, n_cols)
# param_1 = obj.flip()
# obj.reset()
```
