---
title: "125. 验证回文串"
aliases: ["yiduobo的每日leetcode 125.验证回文串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/面试经典-150-题", "题单/滑动窗口与双指针/三-单序列双指针", "题单/面试经典-150-题/双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/140060290"
zhihu_id: "140060290"
zhihu_title: "yiduobo的每日leetcode 125.验证回文串"
question_id: "125"
question: "验证回文串"
problem_url: "https://leetcode.cn/problems/valid-palindrome/"
difficulty: "Easy"
created: "2020-05-12T21:59:38+08:00"
updated: "2020-05-12T21:59:38+08:00"
upvotes: 0
comments: 0
---

# 125. 验证回文串

> **[yiduobo的每日leetcode 125.验证回文串](https://zhuanlan.zhihu.com/p/140060290) · 知乎 · 2020-05-12 · 赞同 0**
> 力扣：[125. 验证回文串](https://leetcode.cn/problems/valid-palindrome/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

125.验证回文串<https://leetcode-cn.com/problems/valid-palindrome/>

比较基础的题目。

用两个指针left与right从两端往中间扫，跳过无关的字符，然后对比s[left]与s[right]。

对于大小写字符的比较，我这里是对比了二者的ascii码。A的ascii码是65，而a的ascii码是97，之间相差32。比较时，若某个字符将位于a到z之间，那么将其ascii码减去32然后再进行对比即可。

最后附上python代码：

```python
class Solution(object):
    def isPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """

        l = 0
        r = len(s) - 1

        while l < r:
            while l < r:
                if (s[l] >= 'a' and s[l] <= 'z') or (s[l] >= 'A' and s[l] <= 'Z') or (s[l] >= '0' and s[l] <= '9'):
                    break
                l += 1

            while l < r:
                if (s[r] >= 'a' and s[r] <= 'z') or (s[r] >= 'A' and s[r] <= 'Z') or (s[r] >= '0' and s[r] <= '9'):
                    break
                r -= 1

            if l == r:
                break

            ascii_l = ord(s[l])
            if ascii_l >= 97:
                ascii_l -= 32
            ascii_r = ord(s[r])
            if ascii_r >= 97:
                ascii_r -= 32
            
            if ascii_l != ascii_r:
                return False

            l += 1
            r -= 1

        return True
```
