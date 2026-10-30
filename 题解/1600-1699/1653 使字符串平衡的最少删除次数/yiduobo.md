---
title: "1653. 使字符串平衡的最少删除次数"
aliases: ["yiduobo的每日leetcode 1653.使字符串平衡的最少删除次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/dynamic-programming", "leetcode/tu-jie", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/441024081"
zhihu_id: "441024081"
zhihu_title: "yiduobo的每日leetcode 1653.使字符串平衡的最少删除次数"
question_id: "1653"
question: "使字符串平衡的最少删除次数"
problem_url: "https://leetcode.cn/problems/minimum-deletions-to-make-string-balanced/"
difficulty: "Medium"
rating: 1794
created: "2021-12-04T00:02:31+08:00"
updated: "2021-12-04T00:02:31+08:00"
upvotes: 0
comments: 0
---

# 1653. 使字符串平衡的最少删除次数

> **[yiduobo的每日leetcode 1653.使字符串平衡的最少删除次数](https://zhuanlan.zhihu.com/p/441024081) · 知乎 · 2021-12-04 · 赞同 0**
> 力扣：[1653. 使字符串平衡的最少删除次数](https://leetcode.cn/problems/minimum-deletions-to-make-string-balanced/) · Medium · 灵茶山艾府：[前后缀分解，一张图秒懂！（附动态规划）Python/Java/C++/Go](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1653.使字符串平衡的最少删除次数

[力扣](https://leetcode-cn.com/problems/minimum-deletions-to-make-string-balanced/)

题目实际上就是要求找到一个位置p，满足0到p - 1之间b的个数加上p到n - 1之间a的个数最小，那么可以一趟扫描统计以当前位置结束的前缀中b的个数，记为s。接下来枚举每一个位置。对于当前位置index，0到index - 1之间b的个数就是s[index - 1]，而index到n - 1之间b的个数自然是s[n - 1] - s[index - 1]。又因为index到n - 1之间一共有index - n个数，那么说明index到n - 1之间a的个数就是index - n - (s[n - 1] - s[index - 1])，此时用s[index - 1] + index - n - (s[n - 1] - s[index - 1])更新答案即可。

上面这种方法需要执行两趟扫描，个人感觉不是太优美。我在这里采用的是动态规划的做法，虽然时间复杂度并没有区别，但是只需要一趟扫描就行了。令f[i]表示0到i这一段变为以a结尾的平衡字符串需要删去多少字符，g[i]则表示0到i这一段变为不以a结尾的平衡字符串需要删去多少字符，那么对于当前位置index：

1、首先考虑边界情况。当index \= 0时：

若s[0] \= 'a'，那么就有f[0] \= 0，g[0] \= 1

若s[0] \= 'b'，那么则是f[0] \= 1，g[0] \= 0

2、当index > 0且s[index] \= 'a'时：

对于f[index]而言，不用对这个a进行额外操作，于是就有f[index] \= f[index - 1]

对于g[index]而言，这个a是需要被删去的，因此就有g[index] \= g[index - 1] + 1

3、当index > 0且s[index] \= 'b'时：

对于f[index]而言，这个b是需要被删去的，因此就有f[index] \= f[index - 1] + 1

对于g[index]而言，不用对这个b进行额外操作，不过这里需要注意的是，这个b除了接在以b结尾的平衡字符串末尾之外，也可以接在以a结尾的平衡字符串末尾，形成aa...aaab这种形式的平衡字符串，因此这里就有

g[index] \= min(g[index - 1], f[index - 1])

动态规划完成后，min(f[-1], g[-1])即为最终答案。

另外，注意到这里f和g只与上一轮有关，因此可以使用变量替代数组滚动求解来节省空间。

最后附上python代码：

```python
class Solution(object):
    def minimumDeletions(self, s):
        """
        :type s: str
        :rtype: int
        """

        if s[0] == 'a':
            f = 0
            g = 1
        else:
            f = 1
            g = 0
        
        for char in s[1:]:
            if char == 'a':
                g += 1
            else:
                g = min(f, g)
                f += 1
        
        return min(f, g)
```
