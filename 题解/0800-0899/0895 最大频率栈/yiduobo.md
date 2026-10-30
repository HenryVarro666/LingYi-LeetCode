---
title: "895. 最大频率栈"
aliases: ["yiduobo的每日leetcode 895.最大频率栈"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/design", "leetcode/hash-table", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/352718358"
zhihu_id: "352718358"
zhihu_title: "yiduobo的每日leetcode 895.最大频率栈"
question_id: "895"
question: "最大频率栈"
problem_url: "https://leetcode.cn/problems/maximum-frequency-stack/"
difficulty: "Hard"
rating: 2028
created: "2021-02-24T22:51:47+08:00"
updated: "2021-02-24T22:51:47+08:00"
upvotes: 0
comments: 0
---

# 895. 最大频率栈

> **[yiduobo的每日leetcode 895.最大频率栈](https://zhuanlan.zhihu.com/p/352718358) · 知乎 · 2021-02-24 · 赞同 0**
> 力扣：[895. 最大频率栈](https://leetcode.cn/problems/maximum-frequency-stack/) · Hard · 灵茶山艾府：[【动画】没想明白？一个动画秒懂！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

895.最大频率栈

[力扣](https://leetcode-cn.com/problems/maximum-frequency-stack/)

一开始感觉跟之前做过的某道题目很像，想着也应该可以用双向链表加dict解决，但是注意到这里有一个问题是pop时需要按进栈的顺序来，那么对于类似于

3->4->3->4

这种进栈顺序而言，其出栈的顺序是4->3->4->3，但是使用双向链表的话就不太好储存进栈的顺序，在弹出4->3之后重新构成3、4链表的顺序是不太好确定的。

换一个角度思考这个问题。对于序列中出现了k次的数x，当本次x被弹出之后，x还在序列中出现了k - 1次，那么在等到其他出现k的次的数被弹出之后，出现k - 1次的这些数将会按照进栈顺序弹出。换言之，我们可以维护一个栈，只有当某个数出现第k - 1次时将其加入到栈中，那么使用这个栈就可以处理上面所说的情况了。继续推广，若对于所有的出现次数cnt，都维护一个对应的栈，那么就可以在max_cnt这个栈弹空之后，继续使用弹出max_cnt - 1这个栈中的元素来满足题目需求。

于是现在就有了一种做法：

使用两个dict分别维护num出现的次数cnt以及每个cnt对应的栈，同时还需要维护一个变量max_cnt表示当前出现次数最多的数出现的次数。

对于push操作而言，可以通过dict获取x当前已经出现的次数cnt，将cnt + 1之后更新dict，同时将x加入到cnt + 1对应的栈当中。若此时的cnt + 1大于max_cnt，那么还需要更新max_cnt。

对于pop操作而言，将dict中max_cnt对应的栈的栈顶元素x弹出，同时还需要判断该栈在弹出x之后是否为空。若为空，那么需要将max_cnt减1，因为此时已经没有出现次数为max_cnt的数了。最后，还需要将dict中x的出现次数减去1。

最后附上python代码：

```python
class FreqStack(object):

    def __init__(self):
        self.num_cnt = {}
        self.cnt_dict = {}
        self.max_cnt = 0

    def push(self, x):
        """
        :type x: int
        :rtype: None
        """
        cnt = self.num_cnt.get(x, 0) + 1
        self.num_cnt[x] = cnt
        
        if cnt not in self.cnt_dict:
            self.cnt_dict[cnt] = []
        self.cnt_dict[cnt].append(x)

        if cnt > self.max_cnt:
            self.max_cnt = cnt

    def pop(self):
        """
        :rtype: int
        """
        x = self.cnt_dict[self.max_cnt].pop()
        if not self.cnt_dict[self.max_cnt]:
            self.max_cnt -= 1
        self.num_cnt[x] = self.num_cnt[x] - 1
        return x

# Your FreqStack object will be instantiated and called as such:
# obj = FreqStack()
# obj.push(x)
# param_2 = obj.pop()
```
