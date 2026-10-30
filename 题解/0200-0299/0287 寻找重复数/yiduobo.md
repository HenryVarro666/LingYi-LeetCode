---
title: "287. 寻找重复数"
aliases: ["yiduobo的每日leetcode 287.寻找重复数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/linked-list", "leetcode/two-pointers", "题单/链表-二叉树与回溯", "题单/图论算法", "题单/LeetCode-热题-100", "题单/链表-二叉树与回溯/一-链表", "题单/图论算法/二-拓扑排序", "题单/LeetCode-热题-100/技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/156063805"
zhihu_id: "156063805"
zhihu_title: "yiduobo的每日leetcode 287.寻找重复数"
question_id: "287"
question: "寻找重复数"
problem_url: "https://leetcode.cn/problems/find-the-duplicate-number/"
difficulty: "Medium"
created: "2020-07-04T19:15:36+08:00"
updated: "2020-07-04T19:15:36+08:00"
upvotes: 1
comments: 0
---

# 287. 寻找重复数

> **[yiduobo的每日leetcode 287.寻找重复数](https://zhuanlan.zhihu.com/p/156063805) · 知乎 · 2020-07-04 · 赞同 1**
> 力扣：[287. 寻找重复数](https://leetcode.cn/problems/find-the-duplicate-number/) · Medium · 灵茶山艾府：[用基环树理解，做法同 142. 环形链表 II（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

287.寻找重复数<https://leetcode-cn.com/problems/find-the-duplicate-number/submissions/>

之前应该碰到过类似的题目，不过这里要求不能改动原始数组且只能使用常数的额外空间，那么这里就要另想办法了。

注意到这里保证了所有数字都在1到n之间，那么意味着我们可以将0到n视为n + 1个点，然后在这些点之间，通过x到nums[x]的对应关系建立有向边，最终可以得到一张有向有环图，而题目此时就变成了找到入环的节点。

到了这里，可以发现这其实就是之前做过的142题环形链表（传送门在这里[yiduobo：yiduobo的每日leetcode 141.环形链表 && 142.环形链表II](https://zhuanlan.zhihu.com/p/142167493)）。于是可以如法炮制，将0视为链表头使用快慢指针来寻找入环节点。

最后附上python代码：

```python
class Solution(object):
    def findDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        fast = 0
        slow = 0
        while True:
            fast = nums[nums[fast]]
            slow = nums[slow]
            if fast == slow:
                break

        fast = 0
        while fast != slow:
            fast = nums[fast]
            slow = nums[slow]

        return fast
```
