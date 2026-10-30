---
title: "901. 股票价格跨度"
aliases: ["yiduobo的每日leetcode 901.股票价格跨度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/data-stream", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/353380640"
zhihu_id: "353380640"
zhihu_title: "yiduobo的每日leetcode 901.股票价格跨度"
question_id: "901"
question: "股票价格跨度"
problem_url: "https://leetcode.cn/problems/online-stock-span/"
difficulty: "Medium"
rating: 1709
created: "2021-02-27T18:12:17+08:00"
updated: "2021-02-27T18:12:17+08:00"
upvotes: 0
comments: 0
---

# 901. 股票价格跨度

> **[yiduobo的每日leetcode 901.股票价格跨度](https://zhuanlan.zhihu.com/p/353380640) · 知乎 · 2021-02-27 · 赞同 0**
> 力扣：[901. 股票价格跨度](https://leetcode.cn/problems/online-stock-span/) · Medium · 灵茶山艾府：[【视频】一个视频讲透单调栈！附题单（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

901.股票价格跨度

[力扣](https://leetcode-cn.com/problems/online-stock-span/)

经典的单调栈问题。题目实际上要求对于输入的price[p]，找到p之前最近的q，满足price[q] > price[p]，那么此时p - q就是答案。

对于输入序列中的某个数price[p]，设其前面有两个数price[i]以及price[j]，其中满足i \< j且price[i] \<\= price[j]。对于price[p]而言，其对应的q显然不可能是i，可以使用反证法证明。

若p对应的q就是i，那么此时需要满足：

price[i] > price[p]

price[i + 1] \<\= price[p]

price[i + 2] \<\= price[p]

...

price[j - 1] \<\= price[p]

price[j] \<\= price[p]

...

price[p - 1] \<\= price[p]

但是注意到这里的price[j] >\= price[i]，那么必然有price[j] > price[p]，与上面的price[j] \<\= price[p]产生了矛盾。

这就说明，对于输入的任意price[i]，若其后续出现了一个price[j]满足price[j] >\= price[i]，那么price[i]就没有再存在的价值了，因此很自然想到使用一个单调栈来维护当前可能成为答案的那些下标。

对于当前输入的price：

1、若栈不为空，且栈顶元素小于等于price，那么将栈顶元素弹出。重复该过程直到栈为空或者栈顶元素大于price。

2、若栈为空，那么答案就是1，否则答案就是当前输入的下标减去栈顶元素对应的下标。

3、最后，还需要将price压入栈中。

由于这里的price都小于100000，那么可以初始化栈为100001，设其对应的下标为-1，这样就不用再判断栈是否为空了。

最后附上python代码：

```python
class StockSpanner(object):

    def __init__(self):
        self.stack = [[100001, -1]]
        self.cnt = 0

    def next(self, price):
        """
        :type price: int
        :rtype: int
        """
        while price >= self.stack[-1][0]:
            self.stack.pop()
        
        res = self.cnt - self.stack[-1][1]
        self.stack.append([price, self.cnt])
        self.cnt += 1
        return res
        

# Your StockSpanner object will be instantiated and called as such:
# obj = StockSpanner()
# param_1 = obj.next(price)
```
