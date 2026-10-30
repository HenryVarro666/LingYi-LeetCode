---
title: "3646. 下一个特殊回文数"
aliases: ["yiduobo的每日leetcode 3646.下一个特殊回文数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/bit-manipulation", "leetcode/dynamic-programming", "leetcode/backtracking", "leetcode/enumeration", "题单/链表-二叉树与回溯", "题单/数学算法", "题单/贪心算法", "题单/链表-二叉树与回溯/四-回溯", "题单/数学算法/七-杂项", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1948167615768934059"
zhihu_id: "1948167615768934059"
zhihu_title: "yiduobo的每日leetcode 3646.下一个特殊回文数"
question_id: "3646"
question: "下一个特殊回文数"
problem_url: "https://leetcode.cn/problems/next-special-palindrome-number/"
difficulty: "Hard"
rating: 2445
created: "2025-09-08T21:51:49+08:00"
updated: "2025-09-08T21:51:50+08:00"
upvotes: 1
comments: 0
---

# 3646. 下一个特殊回文数

> **[yiduobo的每日leetcode 3646.下一个特殊回文数](https://zhuanlan.zhihu.com/p/1948167615768934059) · 知乎 · 2025-09-08 · 赞同 1**
> 力扣：[3646. 下一个特殊回文数](https://leetcode.cn/problems/next-special-palindrome-number/) · Hard · 灵茶山艾府：[两种方法：枚举全排列 / 倒序贪心 + 0-1 背包（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3646.下一个特殊回文数

<https://leetcode.cn/problems/next-special-palindrome-number/>

题目给出一个整数n，n不超过10^15。若一个数是回文数，且其中每个数字k出现的次数恰好为k次，那么这个数就是特殊数。现在要求找出严格大于n的最小的特殊数。

对于一个整数n，若其长度为m，那么大于n的最小特殊数，其长度要么为m，要么为m + 1，理由是特殊数中每种数字k出现的次数恰好为k次，而n最多只有16位，通过1到9这些数之和可以凑出1到17之间的任意数，因此对于n，只需检测所有m位以及m + 1位的特殊数即可。

由于用到的元素只有1到9，那么使用元素集合一共只有2^9种，因此在一开始，可以先使用状态压缩动态规划，计算出每种state对应的数字集最终形成的数字长度是多少，方便后续使用。

接下来遍历所有的state，若state对应的数字集合形成的数字长度等于m或者m + 1，那么就可以通过回溯法找出当前数字集合形成的所有特殊数，并取其中大于n的最小值作为最终答案。需要特别注意的是，并不是所有长度合法的state都可用，因为题目要求形成回文数，因此一个state中最多包含一个奇数，而这个奇数必须放置在回文中心。

另外，在计算每种数字集合可以形成的回文数时，可以利用回文的特性，对每种元素只取一半，然后对这些元素计算全排列。对于得到的每种排列，以当前排列的顺序作为回文数的前半部分，然后复制出后半部分即可得到一个完整的特殊数。当然，有奇数时不要忘了回文中心。

```python
class Solution(object):
    def specialPalindrome(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        f = [0]
        for state in range(1, 512):
            for d in range(1, 10):
                if state & (1 << (d - 1)) == (1 << (d - 1)):
                    f.append(f[state ^ (1 << (d - 1))] + d)
                    break

        global res
        res = None

        def search(now, vis, half_list, mid):
            if len(now) == len(half_list):
                left = ''.join(now)
                right = ''.join(now[::-1])
                final = left + mid + right
                final = int(final)
                if final > n:
                    global res
                    if res is None or res > final:
                        res = final
                return

            for index in range(len(half_list)):
                if index in vis:
                    continue
                if index == 0 or index - 1 not in vis or half_list[index] != half_list[index - 1]:
                    vis.add(index)
                    now.append(half_list[index])
                    search(now, vis, half_list, mid)
                    now.pop()
                    vis.remove(index)

        def generate(num_list):
            mid = ''
            half_list = []
            for d in num_list:
                if d % 2 == 1:
                    mid = str(d)
                half_list.extend([str(d)] * (d // 2))
            
            vis = set()
            now = []
            search(now, vis, half_list, mid)

        length = len(str(n))
        for state in range(1, 512):
            if f[state] == length or f[state] == length + 1:
                num_list = []
                odd = 0
                for d in range(1, 10):
                    if state & (1 << (d - 1)) == (1 << (d - 1)):
                        if d % 2 == 1:
                            odd += 1
                        num_list.append(d)
                
                if odd <= 1:
                    generate(num_list)
        
        return res
```
