---
title: "1754. 构造字典序最大的合并字符串"
aliases: ["yiduobo的每日leetcode 1754.构造字典序最大的合并字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/suffix-array", "题单/贪心算法", "题单/字符串", "题单/贪心算法/三-字符串贪心", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/458716642"
zhihu_id: "458716642"
zhihu_title: "yiduobo的每日leetcode 1754.构造字典序最大的合并字符串"
question_id: "1754"
question: "构造字典序最大的合并字符串"
problem_url: "https://leetcode.cn/problems/largest-merge-of-two-strings/"
difficulty: "Medium"
rating: 1829
created: "2022-01-17T23:45:20+08:00"
updated: "2022-01-17T23:45:20+08:00"
upvotes: 0
comments: 0
---

# 1754. 构造字典序最大的合并字符串

> **[yiduobo的每日leetcode 1754.构造字典序最大的合并字符串](https://zhuanlan.zhihu.com/p/458716642) · 知乎 · 2022-01-17 · 赞同 0**
> 力扣：[1754. 构造字典序最大的合并字符串](https://leetcode.cn/problems/largest-merge-of-two-strings/) · Medium · 灵茶山艾府：[后缀数组线性做法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1754.构造字典序最大的合并字符串

[力扣](https://leetcode-cn.com/problems/largest-merge-of-two-strings/)

经典的字符串合并问题，也是使用两个指针进行归并，不过由于相同字符的存在以及字典序的定义与数值大小有所区别，因此在执行合并时不能按照数值的二路归并来做。一种经典的写法是若当前的word1[p1:] + word2[p2:] > word2[p2:] + word1[p1:]，那么此时就应该合并word1[p1]，否则合并word2[p2]。

这个写法也很好理解，就是从word1的p1开始与word2的p2开始逐个字符进行比较。而加上另一个字符串的理由是若两边的字符一直相同，那么可能出现p1走到word1末尾或者p2走到word2末尾的情况。在p1走到word1末尾时需要被迫用到word2中的字符，同样的，在p2走到word2末尾时需要用上word1中的字符，因此可以用上面这种写法。

另外，本题应该是可以使用后缀数组来做的，不过由于数据规模很小，我在这里偷懒就用了上面这种写法。

最后附上python代码：

```python
class Solution(object):
    def largestMerge(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: str
        """

        n1 = len(word1)
        n2 = len(word2)
        p1 = p2 = 0
        res = []
        while p1 < n1 and p2 < n2:
            if word1[p1:] + word2[p2:] > word2[p2:] + word1[p1:]:
                res.append(word1[p1])
                p1 += 1
            else:
                res.append(word2[p2])
                p2 += 1
        
        if p1 == n1:
            return ''.join(res) + word2[p2:]
        else:
            return ''.join(res) + word1[p1:]
```
