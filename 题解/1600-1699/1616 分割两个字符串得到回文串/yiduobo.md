---
title: "1616. 分割两个字符串得到回文串"
aliases: ["yiduobo的每日leetcode 1616.分割两个字符串得到回文串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/two-pointers", "leetcode/tu-jie", "题单/滑动窗口与双指针", "题单/贪心算法", "题单/滑动窗口与双指针/三-单序列双指针", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/435443227"
zhihu_id: "435443227"
zhihu_title: "yiduobo的每日leetcode 1616.分割两个字符串得到回文串"
question_id: "1616"
question: "分割两个字符串得到回文串"
problem_url: "https://leetcode.cn/problems/split-two-strings-to-make-palindrome/"
difficulty: "Medium"
rating: 1868
created: "2021-11-19T23:01:19+08:00"
updated: "2021-11-19T23:01:19+08:00"
upvotes: 0
comments: 0
---

# 1616. 分割两个字符串得到回文串

> **[yiduobo的每日leetcode 1616.分割两个字符串得到回文串](https://zhuanlan.zhihu.com/p/435443227) · 知乎 · 2021-11-19 · 赞同 0**
> 力扣：[1616. 分割两个字符串得到回文串](https://leetcode.cn/problems/split-two-strings-to-make-palindrome/) · Medium · 灵茶山艾府：[没想明白？一张图秒懂！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1616.分割两个字符串得到回文串

[力扣](https://leetcode-cn.com/problems/split-two-strings-to-make-palindrome/)

题目要求找出某个位置k，满足a的前k个字符与b的后n - k个字符组合起来，或者b的前k个字符与a的后n - k个字符组合起来能形成回文串。

直接做感觉不太好做，转而分析答案是怎么构成的。简单来看一共有四种情况。

1、答案是由a的前k个字符与b的后n - k个字符组成的，且这里的k >\= n - k：

a的前n - k个字符需要与b的后n - k个字符从外到内一一对应，且a的第n - k到第k个字符需要满足是一个回文串

例如abcdc与ba，需要满足ab与ba对应，且中间的cdc本身就是一个回文串

2、答案是由a的前k个字符与b的后n - k个字符组成的，且这里的k \< n - k：

a的前k个字符需要与b的后k个字符从外到内意义对应，且b的第k到第n - k个字符需要满足是一个回文串

例如ab与cdcba，需要满足ab与ba对应，且中间的cdc本身就是一个回文串

3、答案是由b的前k个字符与a的后n - k个字符组成的，且这里的k >\= n - k:

与情况1类似，此时要求b的第n - k到第k个字符为一个回文串

4、答案是由b的前k个字符与a的后n - k个字符组成的，且这里的k \< n - k：

与情况2类似，此时要求a的第k到第n - k个字符为一个回文串

可以发现无论哪种情况，中间都存在一个原生的回文串。这个回文串可以来自a或者b，且越长越好。极限情况下这个回文串就是a或者b本身，那么此时的答案自然为true。为了找到这个最长的中心回文串，则可以使用中心扩展法分别寻找a和b最长的中心回文串。得到这个中心回文串之后，若其长度为n，说明a或者b本身就是一个回文串，直接返回true，否则还需要考察下面两种情况：

1、a的头部 + 中心回文串 + b的尾部

2、b的头部 + 中心回文串 + a的尾部

由于此时已经得到了中心回文串，那么直接从中心回文串的头尾开始继续使用中心扩展法来对a和b进行匹配，若其中某种情况可以匹配成功，那么答案为true，否则答案为false

另外需要特别注意的是，当字符串的长度为奇数时，中心回文串的长度至少为1，即a或者b正中间的字符就是一个中心回文串。而当字符串的长度为偶数时，中心回文串的长度则可能为0。

最后附上python代码：

```python
class Solution(object):
    def checkPalindromeFormation(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: bool
        """

        n = len(a)
        if n & 1:
            l = r = n / 2
        else:
            l = n / 2 - 1
            r = n / 2
        
        flag1 = flag2 = True
        while l >= 0:
            if a[l] != a[r]:
                flag1 = False
            if b[l] != b[r]:
                flag2 = False
            if not flag1 and not flag2:
                break
            l -= 1
            r += 1
        
        if l == -1:
            return True

        flag1 = flag2 = True
        while l >= 0:
            if a[l] != b[r]:
                flag1 = False
            if a[r] != b[l]:
                flag2 = False
            if not flag1 and not flag2:
                return False
            l -= 1
            r += 1

        return True
```
