---
title: "1737. 满足三条件之一需改变的最少字符数"
aliases: ["yiduobo的每日leetcode 1737.满足三条件之一需改变的最少字符数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/453359888"
zhihu_id: "453359888"
zhihu_title: "yiduobo的每日leetcode 1737.满足三条件之一需改变的最少字符数"
question_id: "1737"
question: "满足三条件之一需改变的最少字符数"
problem_url: "https://leetcode.cn/problems/change-minimum-characters-to-satisfy-one-of-three-conditions/"
created: "2022-01-04T23:42:52+08:00"
updated: "2022-01-04T23:42:52+08:00"
upvotes: 0
comments: 0
---

# 1737. 满足三条件之一需改变的最少字符数

> **[yiduobo的每日leetcode 1737.满足三条件之一需改变的最少字符数](https://zhuanlan.zhihu.com/p/453359888) · 知乎 · 2022-01-04 · 赞同 0**
> 力扣：[1737. 满足三条件之一需改变的最少字符数](https://leetcode.cn/problems/change-minimum-characters-to-satisfy-one-of-three-conditions/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1737.满足三条件之一需改变的最少字符数

[力扣](https://leetcode-cn.com/problems/change-minimum-characters-to-satisfy-one-of-three-conditions/)

由于a和b由小写字母组成，那么就可以枚举所有的小写字符char，然后基于char就有三种可能的变化：

1、将a和b全部变成char

2、将a中的字符变成小于char的字符，将b中的字符变成大于等于char的字符

3、将a中的字符变成大于等于char的字符，将b中的字符变成小于char的字符

为了方便计算，需要先使用哈希表统计出a和b中各个字符出现的次数，分别记为cnt_a和cnt_b。那么对于上面三种变化：

1、将a和b全部变成char：

a中原有的的字符char一共有cnt_a[char]个，那么需要对剩下的len(a) - cnt_a[char]个字符做出改变，b也是类似，需要改变len(b) - cnt_b[char]个字符，因此这里改变的代价就是len(a) - cnt_a[char] + len(b) - cnt_b[char]

2、将a中的字符变成小于char的字符，将b中的字符变成大于等于char的字符：

a中原有的字符中，小于char的字符一共有cnt_a['a'] + cnt_a['b'] + ... + cnt_a[prev(char)]个，其中prev(char)表示char的上一个字符。注意到这是一个前缀和的式子，那么可以将其写成sum_a[prev(char)]，表示a中小于等于prev(char)的字符的数目。相对的，大于等于char的字符数目就是len(a) - sum_a[prev(char)]个，因此将a中字符变成小于char的字符一共需要len(a) - sum_a[prev(char)]次操作。

b中原有的字符中，小于char的字符也是cnt_b['a'] + cnt_b['b'] + ... + cnt_b[prev(char)]个，同样可以使用前缀和sum_b[prev(char)]来表示。需要将这些字符变为大于等于char的字符，因此需要sum_b[prev(char)]次操作。

综合起来，一共需要len(a) - sum_a[prev(char)] + sum_b[prev(char)]次操作。

3、将a中的字符变成大于等于char的字符，将b中的字符变成小于char的字符：

这种情况与情况2是对称的，那么需要的操作数就是len(b) - sum_b[prev(char)] + sum_a[prev(char)]次操作

对于枚举到的char，计算三种变化所需的操作数，然后使用其中的最小值更新答案即可。

在这里除了已经统计好的cnt_a以及cnt_b之外，就只需要额外计算sum_a以及sum_b了。由于这两个是前缀和，那么按照从小到大的顺序枚举char的话，就可以边计算答案边计算sum_a和sum_b，而不需要额外预处理了。

具体实现上，由于'a'的ascii码是97，所以我选择将'a'到'z'映射到0到25上方便数组下标的操作。

最后附上python代码：

```python
class Solution(object):
    def minCharacters(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: int
        """

        cnt_a = [0] * 26
        cnt_b = [0] * 26

        for char in a:
            cnt_a[ord(char) - 97] += 1
        for char in b:
            cnt_b[ord(char) - 97] += 1

        len_a = len(a)
        len_b = len(b)

        res = len_a + len_b
        sum_a = sum_b = 0
        for index in range(26):
            res = min(res, len_a - cnt_a[index] + len_b - cnt_b[index])
            if index > 0:
                res = min(res, min(len_a - sum_a + sum_b, len_b - sum_b + sum_a))

            sum_a += cnt_a[index]
            sum_b += cnt_b[index]
        
        return res
```
