---
title: "1472. 设计浏览器历史记录"
aliases: ["yiduobo的每日leetcode 1472.设计浏览器历史记录"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/design", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/414338374"
zhihu_id: "414338374"
zhihu_title: "yiduobo的每日leetcode 1472.设计浏览器历史记录"
question_id: "1472"
question: "设计浏览器历史记录"
problem_url: "https://leetcode.cn/problems/design-browser-history/"
difficulty: "Medium"
rating: 1454
created: "2021-09-26T23:37:12+08:00"
updated: "2021-09-26T23:37:12+08:00"
upvotes: 1
comments: 0
---

# 1472. 设计浏览器历史记录

> **[yiduobo的每日leetcode 1472.设计浏览器历史记录](https://zhuanlan.zhihu.com/p/414338374) · 知乎 · 2021-09-26 · 赞同 1**
> 力扣：[1472. 设计浏览器历史记录](https://leetcode.cn/problems/design-browser-history/) · Medium · 灵茶山艾府：[栈模拟（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1472.设计浏览器历史记录

[力扣](https://leetcode-cn.com/problems/design-browser-history/)

注意到回退操作是非常符合栈的操作的，因此可以使用一个栈来维护当前的访问记录，并将被回退掉的部分使用另一个栈来储存，用来执行前进操作。当出现回退或前进操作时，就将网页在这两个栈中来回倒腾，若出现跳转操作，那么将其加入到回退栈中，并将前进栈清空即可。

我在这里采用的另一种做法。使用一个队列q维护当前浏览过的所有地址，并使用一个变量now表示目前正在访问队列中哪个位置表示的网页，以及另一个变量cnt表示当前队列中有效网页的数目。这里维护有效网页数目的理由是因为当出现回退操作接跳转操作的话，回退的那些网页就会被清理掉，也就是队列中的无效网页了。对于每种操作而言：

1、visit操作：

若now位于0到当前队列长度减一之间，说明此前已经遇到过回退操作，那么此时就应该将url直接插入到队列now的下一个位置，也就是q[now + 1]这里，并将now加上1。

否则的话，说明此时是正常的新增浏览，因此需要将url添加到q的末尾，并将now加上1。

无论是哪种情况，visit操作的出现意味着需要更新有效网页的数目，由于now是从下标0开始的，因此此时的有效网页数目cnt就等于now加1。

2、back操作：

直接将now减去steps。当然这里now的下限是队列中最前面那个网页，也就是0，因此若now小于0，那么将now置为0，接下来返回q[now]即可。

3、forward操作：

直接将now加上steps，当是这里前进的上限是队列中最后一个有效网页，也就是cnt - 1，因此若now大于cnt - 1，那么将now置为cnt - 1，接下来返回q[now]即可。

需要注意，对于back和forward操作而言，浏览历史是不会变化的，因此有效网页的数目cnt此时也不应该产生变化。

最后附上python代码：

```python
class BrowserHistory(object):

    def __init__(self, homepage):
        """
        :type homepage: str
        """
        self.q = [homepage]
        self.cnt = 1
        self.now = 0

    def visit(self, url):
        """
        :type url: str
        :rtype: None
        """

        if len(self.q) - 1 > self.now:
            self.now += 1
            self.q[self.now] = url
        else:
            self.now += 1
            self.q.append(url)
        
        self.cnt = self.now + 1

    def back(self, steps):
        """
        :type steps: int
        :rtype: str
        """
        self.now -= steps
        if self.now < 0:
            self.now = 0
        
        return self.q[self.now]

    def forward(self, steps):
        """
        :type steps: int
        :rtype: str
        """
        self.now += steps
        if self.now > self.cnt - 1:
            self.now = self.cnt - 1
        
        return self.q[self.now]

# Your BrowserHistory object will be instantiated and called as such:
# obj = BrowserHistory(homepage)
# obj.visit(url)
# param_2 = obj.back(steps)
# param_3 = obj.forward(steps)
```
