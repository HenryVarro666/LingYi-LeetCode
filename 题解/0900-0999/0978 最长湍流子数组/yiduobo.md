---
title: "978. 最长湍流子数组"
aliases: ["yiduobo的每日leetcode 978.最长湍流子数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/363053607"
zhihu_id: "363053607"
zhihu_title: "yiduobo的每日leetcode 978.最长湍流子数组"
question_id: "978"
question: "最长湍流子数组"
problem_url: "https://leetcode.cn/problems/longest-turbulent-subarray/"
created: "2021-04-07T22:03:30+08:00"
updated: "2021-04-07T22:03:30+08:00"
upvotes: 0
comments: 0
---

# 978. 最长湍流子数组

> **[yiduobo的每日leetcode 978.最长湍流子数组](https://zhuanlan.zhihu.com/p/363053607) · 知乎 · 2021-04-07 · 赞同 0**
> 力扣：[978. 最长湍流子数组](https://leetcode.cn/problems/longest-turbulent-subarray/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

978.最长湍流子数组

[力扣](https://leetcode-cn.com/problems/longest-turbulent-subarray/)

首先，数组中的任意元素单独拉出来都是长度为1的湍流子数组，因此可以先初始化答案为1。

接下来，根据题目的定义，湍流子数组中不会出现两个数相等的情况，同时要求满足符号在不断变化。那么可以从头到尾进行一趟扫描，使用两个变量start_pos和flag分别记录当前湍流子数组的起始位置以及当前的符号情况，那么对于arr[index]：

1、若arr[index]等于arr[index + 1]，那么从start_pos开始的湍流子数组将在index结束，使用index - start_pos + 1更新答案。同时arr[index]与arr[index + 1]也无法作为新的湍流子数组的开端，于是置start_pos与flag为空。

2、若arr[index] \< arr[index + 1]，那么需要判断当前flag是否表示arr[index - 1] > arr[index]。在这里可以先约定flag等于1有arr[index - 1] > arr[index]，flag为0则表示arr[index - 1] \< arr[index]，那么若此时flag为1，说明湍流子数组仍在向后延伸，因此只需将flag改为0；若flag不为1，那么从start_pos开始的湍流子数组将在index结束，使用index - start_pos + 1更新答案，同时新的湍流子数组将以arr[index]与arr[index + 1]作为开端，因此需要置start_pos为inedx，同时置flag为0。

3、若arr[index] > arr[index + 1]，与情况2相反，若flag为0，则置flag为1，否则更新答案并置start_pos为index，同时置flag为1。

遍历完成后，需要记得使用由arr末尾形成的湍流子数组的长度更新答案。

最后附上python代码：

```python
class Solution(object):
    def maxTurbulenceSize(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        n = len(arr)
        start_pos = None
        flag = None
        res = 1
        for index in range(n - 1):
            if arr[index] == arr[index + 1]:
                if start_pos is not None:
                    res = max(res, index - start_pos + 1)
                start_pos = None
                flag = None
            
            elif arr[index] < arr[index + 1]:
                if flag == 1:
                    flag = 1 - flag
                else:
                    if start_pos is not None:
                        res = max(res, index - start_pos + 1) 
                    start_pos = index
                    flag = 0

            else:
                if flag == 0:
                    flag = 1 - flag
                else:
                    if start_pos is not None:
                        res = max(res, index - start_pos + 1) 
                    start_pos = index
                    flag = 1

        if start_pos is not None:
            res = max(res, n - start_pos)

        return res
```
