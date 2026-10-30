---
title: "1585. 检查字符串是否可以通过排序子字符串得到另一个字符串"
aliases: ["yiduobo的每日leetcode 1585.检查字符串是否可以通过排序子字符串得到另一个字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/430995591"
zhihu_id: "430995591"
zhihu_title: "yiduobo的每日leetcode 1585.检查字符串是否可以通过排序子字符串得到另一个字符串"
question_id: "1585"
question: "检查字符串是否可以通过排序子字符串得到另一个字符串"
problem_url: "https://leetcode.cn/problems/check-if-string-is-transformable-with-substring-sort-operations/"
created: "2021-11-08T23:45:59+08:00"
updated: "2021-11-08T23:45:59+08:00"
upvotes: 0
comments: 0
---

# 1585. 检查字符串是否可以通过排序子字符串得到另一个字符串

> **[yiduobo的每日leetcode 1585.检查字符串是否可以通过排序子字符串得到另一个字符串](https://zhuanlan.zhihu.com/p/430995591) · 知乎 · 2021-11-08 · 赞同 0**
> 力扣：[1585. 检查字符串是否可以通过排序子字符串得到另一个字符串](https://leetcode.cn/problems/check-if-string-is-transformable-with-substring-sort-operations/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1585.检查字符串是否可以通过排序子字符串得到另一个字符串

[力扣](https://leetcode-cn.com/problems/check-if-string-is-transformable-with-substring-sort-operations/)

这题目名字也是够长的。。

回到题目本身。对于排序操作，不确定性还是比较多的，不过这里有一点可以确定的是，对于原字符串中的两个字符s[i]和s[j]而言，若i \< j且s[i] \< s[j]，那么无论怎么排s[j]都是不可能被排到s[i]前面去的。更进一步的，如果现在要将某个位置上的字符s[k]通过排序放置到s[0]上去，那么就必须满足s[0]到s[k - 1]之间的字符都大于等于s[k]。

根据上面的结论，就可以从头开始向后逐个检测t中当前位置的字符能否被转移过来。简单来说就是对于t[i]这个字符而言，设其在s中还未被使用的最靠前的位置为p，那么此时只需要检测0到t[i] - 1这些字符在s中还未被使用的最靠前的位置是否小于p，若小于p，说明s[p]这个字符是无法越过这个位置小于p的字符的，因此答案为false。

上面这种做法还有一个前提是每次交换并不会影响未使用字符在s中的相对位置，这一点可以通过在交换时两两进行交换来达成。例如需要将s[p]交换到s[i]时，可以先将s[p]与s[p - 1]做排序从而将s[p]与s[p - 1]对调，然后将此时的s[p - 1]与s[p - 2]排序进行交换，直到原先的s[p]被交换到i这个位置上为止。这个过程与冒泡排序法的交换过程是完全一致的。

根据上面的算法，就可以先对s进行一趟扫描，将每个字符的位置按从前向后的顺序记录下来，然后逐个遍历t中的字符，检测当前字符是否满足上面的条件。

最后附上python代码：

```python
class Solution(object):
    def isTransformable(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """

        pos_list = [[] for _ in range(10)]
        for index, char in enumerate(s):
            now = int(char)
            pos_list[now].append(index)
        
        now_pos = [0] * 10
        for char in t:
            now = int(char)
            if now_pos[now] == len(pos_list[now]):
                return False
            for num in range(now):
                if now_pos[num] < len(pos_list[num]) and pos_list[num][now_pos[num]] < pos_list[now][now_pos[now]]:
                    return False
            
            now_pos[now] += 1
        
        return True
```
