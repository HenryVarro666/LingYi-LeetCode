---
title: "2081. k镜像数字的和"
aliases: ["yiduobo的每日leetcode 2081.k镜像数字的和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/enumeration", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/518032069"
zhihu_id: "518032069"
zhihu_title: "yiduobo的每日leetcode 2081.k镜像数字的和"
question_id: "2081"
question: "k 镜像数字的和"
problem_url: "https://leetcode.cn/problems/sum-of-k-mirror-numbers/"
difficulty: "Hard"
rating: 2210
created: "2022-05-21T23:54:58+08:00"
updated: "2022-05-21T23:54:58+08:00"
upvotes: 0
comments: 0
---

# 2081. k镜像数字的和

> **[yiduobo的每日leetcode 2081.k镜像数字的和](https://zhuanlan.zhihu.com/p/518032069) · 知乎 · 2022-05-21 · 赞同 0**
> 力扣：[2081. k 镜像数字的和](https://leetcode.cn/problems/sum-of-k-mirror-numbers/) · Hard · 灵茶山艾府：[【模板】枚举回文数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2081.k镜像数字的和

[力扣](https://leetcode.cn/problems/sum-of-k-mirror-numbers/)

完全没有思路的题目，不过数据范围比较小，可以通过打表来做。

在打表过程中，发现直接枚举十进制数字老半天都不出结果，还需要优化打表的代码。。

题目要求十进制数和k进制数都是回文数，那么可以枚举回文数的半边，然后翻转过去得到完整的回文数。枚举十进制数需要枚举的位数较短，但是每位上可选的数字较多；相对的，枚举k进制数需要枚举的位数较长，但是每位上可选的数字较少。具体选择枚举哪种还是见仁见智吧，我在这里枚举的是十进制数的一半。

由于题目要求是最小的n个数，因此需要先枚举这个一半的长度l。

对于这个l开始执行dfs，得到长度为l的数字，即上面说的回文数的半边。接下来对于这个数字，翻转过去后可以形成长度为l + l - 1以及l + l这两种回文数，区别在于是否需要复制最后一个数字。同样的，由于题目有顺序要求，因此在这里需要先检测所有对称得到长度为l + l - 1的数字，再重新dfs然后检测长度为l + l的数字。

具体的检测就是将这个一半的数字翻转过去得到完整数字后，转化成k进制然后检测是否为回文数，都是比较基础的操作，这里就不展开了。

打表完成之后，发现最后枚举的长度其实很短，那么这个打表代码提交上去完全可以通过。。

最后附上python代码：

```python
class Solution(object):
    def kMirror(self, k, n):
        """
        :type k: int
        :type n: int
        :rtype: int
        """

        def check(now, l, target_l):
            num = 0
            for index in range(target_l):
                if index < l:
                    num = num * 10 + now[index]
                else:
                    num = num * 10 + now[target_l - index - 1]
            
            base_k = []
            tmp = num
            while True:
                base_k.append(tmp % k)
                tmp /= k
                if tmp == 0:
                    break
            
            flag = True
            for index in range(len(base_k) / 2):
                if base_k[index] != base_k[len(base_k) - 1 - index]:
                    flag = False
                    break
            
            if flag:
                return num
            
            return 0

        def dfs(level, now, l, target_l):
            if level == l:
                check_res = check(now, l, target_l)
                if check_res > 0:
                    self.res += check_res
                    self.cnt += 1
                return
            
            for index in range(10):
                if index > 0 or level > 0:
                    now.append(index)
                    dfs(level + 1, now, l, target_l)
                    if self.cnt == n:
                        return
                    now.pop()

        l = 0
        self.cnt = 0
        self.res = 0
        while True:
            l += 1
            dfs(0, [], l, l + l - 1)
            if self.cnt == n:
                break
            dfs(0, [], l, l + l)
            if self.cnt == n:
                break

        return self.res
```
