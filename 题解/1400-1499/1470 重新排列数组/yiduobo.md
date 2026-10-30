---
title: "1470. 重新排列数组"
aliases: ["yiduobo的每日leetcode 1470.重新排列数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/413983226"
zhihu_id: "413983226"
zhihu_title: "yiduobo的每日leetcode 1470.重新排列数组"
question_id: "1470"
question: "重新排列数组"
problem_url: "https://leetcode.cn/problems/shuffle-the-array/"
difficulty: "Easy"
created: "2021-09-25T23:42:14+08:00"
updated: "2021-09-25T23:42:14+08:00"
upvotes: 0
comments: 0
---

# 1470. 重新排列数组

> **[yiduobo的每日leetcode 1470.重新排列数组](https://zhuanlan.zhihu.com/p/413983226) · 知乎 · 2021-09-25 · 赞同 0**
> 力扣：[1470. 重新排列数组](https://leetcode.cn/problems/shuffle-the-array/) · Easy · 灵茶山艾府：[两种方法：创建新数组 / 原地交换（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1470.重新排列数组

[力扣](https://leetcode-cn.com/problems/shuffle-the-array/)

比较基础的题目。从0到n - 1进行遍历，对于当前位置index，将nums[index]以及nums[index + n]加入到答案的末尾即可。

最后附上python代码：

```python
class Solution(object):
    def shuffle(self, nums, n):
        """
        :type nums: List[int]
        :type n: int
        :rtype: List[int]
        """

        res = []
        for index in range(n):
            res.append(nums[index])
            res.append(nums[index + n])
        
        return res
```
