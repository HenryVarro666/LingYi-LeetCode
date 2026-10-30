---
title: "440. 字典序最小的第K个数字"
aliases: ["yiduobo的每日leetcode 440.字典序最小的第K个数字"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/trie", "leetcode/math", "题单/常用数据结构", "题单/常用数据结构/六-字典树-trie"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/203934547"
zhihu_id: "203934547"
zhihu_title: "yiduobo的每日leetcode 440.字典序最小的第K个数字"
question_id: "440"
question: "字典序的第K小数字"
problem_url: "https://leetcode.cn/problems/k-th-smallest-in-lexicographical-order/"
difficulty: "Hard"
created: "2020-08-29T01:09:55+08:00"
updated: "2020-08-29T01:09:55+08:00"
upvotes: 0
comments: 0
---

# 440. 字典序最小的第K个数字

> **[yiduobo的每日leetcode 440.字典序最小的第K个数字](https://zhuanlan.zhihu.com/p/203934547) · 知乎 · 2020-08-29 · 赞同 0**
> 力扣：[440. 字典序的第K小数字](https://leetcode.cn/problems/k-th-smallest-in-lexicographical-order/) · Hard · 灵茶山艾府：[在十叉树上找第 k 小，O(log n) 数学优化（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

440.字典序最小的第K个数字<https://leetcode-cn.com/problems/k-th-smallest-in-lexicographical-order/>

很有意思的题目。根据之前做过的字典排序树的思路，依然可以将问题看成十叉树按先序遍历找到的第k个节点是什么。但是在这里，如果模拟先序遍历的过程，时间复杂度为O(k)，效率捉急，需要想办法优化。

一个自然的想法就是如果能提前得知以当前节点为根的子树中有多少个节点，那么就可以高效地判断第k个节点是否位于当前子树中了。

注意到如果能遍历到第k层的节点，树中第1到第k - 1层一定是满的，因此可以采用逐层填充判断的方式。不妨设当前节点为tmp，如果存在下一层的节点，tmp的子节点应该是tmp \* 10到tmp \* 10 + 9。因此若tmp \* 10依然小于等于N，说明整棵树可以扩展到tmp \* 10这一层。同样的，若tmp \* 10小于等于N，那么就可以继续扩展到下一层，而这一层就有10个节点，下一层的最左侧节点则是tmp \* 100。

到了这里可以发现，以1为根的子树如果共k层，那么其一共就有1 + 10 + ... + 10^(k - 1) + min(n - 10^k，10^k)，设为cnt。若这个cnt小于等于k，说明第k个节点不在以1位根的子树中，那么按同样的方式开始计算以2为根的子树，此时应该寻找的就是第k - cnt个节点，这里k - cnt的含义是排除了以1为根节点的树中的所有节点。若这个cnt大于k，说明要找的节点就在以1为根节点的子树中，那么可以按同样的方式开始计算以10为根的子树，此时则是应该寻找第k - 1个节点，这里k - 1表示的是排除了节点1。

不断按上面的方法迭代，直到k等于0，那么此时迭代到的根节点就是答案。

最后附上python代码：

```python
class Solution(object):
    def findKthNumber(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """

        res = 1
        k -= 1
        while k > 0:
            cnt = 0
            tmp = res
            next = res + 1
            while tmp <= n:
                cnt += min(next, n + 1) - tmp
                tmp *= 10
                next *= 10
            print tmp, next, cnt
            if k >= cnt:
                k -= cnt
                res += 1
            else:
                k -= 1
                res *= 10

        return res
```
