---
title: "2601. 质数减法运算"
aliases: ["yiduobo的每日leetcode 2601.质数减法运算"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/644440169"
zhihu_id: "644440169"
zhihu_title: "yiduobo的每日leetcode 2601.质数减法运算"
question_id: "2601"
question: "质数减法运算"
problem_url: "https://leetcode.cn/problems/prime-subtraction-operation/"
difficulty: "Medium"
rating: 1779
created: "2023-07-19T03:02:54+08:00"
updated: "2023-07-19T03:02:54+08:00"
upvotes: 0
comments: 0
---

# 2601. 质数减法运算

> **[yiduobo的每日leetcode 2601.质数减法运算](https://zhuanlan.zhihu.com/p/644440169) · 知乎 · 2023-07-19 · 赞同 0**
> 力扣：[2601. 质数减法运算](https://leetcode.cn/problems/prime-subtraction-operation/) · Medium · 灵茶山艾府：[【简洁写法】筛质数+二分查找（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2601.质数减法运算

[力扣](https://leetcode.cn/problems/prime-subtraction-operation/)

贪心法的题目。不妨先考虑nums[0]的处理方法。对于nums[0]而言，为了使得后续形成单调递增数组的可能性更大，就应该让nums[0]操作后得到的结果尽量的小。换言之，在这里就需要找出一个小于等于nums[0] - 1的最大质数p[0]，然后用nums[0] - p[0]得到新数组的首项final[0]

接下来对于nums[1]而言，则需要满足nums[1] - p[1] > final[0]，同时nums[1] - p[1]需要尽量小

对于nums[1] - p[1] > final[0]，可以将其变形为p[1] \<\= nums[1] - final[0] - 1，也就是说在这里需要找出一个小于等于nums[1] - final[0] - 1的最大质数p[1]，然后用nums[1] - p[1]得到final[1]

更一般的，对于nums[i]而言，同样需要满足上面的两个条件，因此可以使用相同的处理方法，即找出一个小于等于nums[i] - final[i - 1] - 1的最大质数p[i]，然后用nums[i] - p[i]得到final[i]

在这里需要注意两种特殊情况：

1、若nums[i] - final[i - 1] - 1小于0，那么说明nums[i]已经小于等于当前final的最后一项了，此时没有操作的空间，只能返回-1

2、若不存在小于nums[i] - final[i - 1] - 1的质数，那么说明此时final的最后一项就只能取nums[i]

由于题目的数据规模比较小，那么在这里可以直接暴力计算找出每一轮对应的p[i]。我在这里选择的是先通过筛法找出1到1000内的所有质数并形成一个list，然后再从2遍历到1000，通过单调性找出小于等于当前数的最大质数并记录在数组remove中，其中remove[i]表示小于等于i的最大质数。得到remove后，只需按照上面描述的处理方法计算新数组即可。

最后附上python代码：

```python
class Solution(object):
    def primeSubOperation(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        f = [None] * 1001
        prime_list = []
        x = 2
        while x <= 1000:
            if f[x] is None:
                prime_list.append(x)
                for y in range(x + x, 1001, x):
                    f[y] = x
            
            x += 1
        
        remove_num = [0, 0]
        p = 0
        for v in range(2, 1001):
            while p + 1 < len(prime_list) and prime_list[p + 1] <= v:
                p += 1
            
            remove_num.append(prime_list[p])
        
        pre = nums[0] - remove_num[nums[0] - 1]
        for v in nums[1:]:
            v -= pre + 1
            if v < 0:
                return False
            
            v -= remove_num[v]
            pre += v + 1
        
        return True
```
