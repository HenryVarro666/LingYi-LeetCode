---
title: "2860. 让所有学生保持开心的分组方法数"
aliases: ["yiduobo的每日leetcode 2860.让所有学生保持开心的分组方法数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/661369102"
zhihu_id: "661369102"
zhihu_title: "yiduobo的每日leetcode 2860.让所有学生保持开心的分组方法数"
question_id: "2860"
question: "让所有学生保持开心的分组方法数"
problem_url: "https://leetcode.cn/problems/happy-students/"
difficulty: "Medium"
rating: 1626
created: "2023-10-15T04:53:16+08:00"
updated: "2023-10-15T04:53:16+08:00"
upvotes: 0
comments: 0
---

# 2860. 让所有学生保持开心的分组方法数

> **[yiduobo的每日leetcode 2860.让所有学生保持开心的分组方法数](https://zhuanlan.zhihu.com/p/661369102) · 知乎 · 2023-10-15 · 赞同 0**
> 力扣：[2860. 让所有学生保持开心的分组方法数](https://leetcode.cn/problems/happy-students/) · Medium · 灵茶山艾府：[遇事不决先排序（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2860.让所有学生保持开心的分组方法数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/happy-students/)

不妨设选中了k名学生，那么只有当着k名学生对应的nums都小于k，且其他剩余学生对应的nums都大于k时，这才是一种理想的分组。换言之，只有当nums中第k小的数小于k，且第k + 1小的数大于k时，选中前k小的学生才是一个好的分组。

根据这一点，就可以将数组从小到大进行排序，然后从1到n进行一趟遍历。对于当前遍历到的k，数组中对应的第k小的数为nums[k - 1]，那么当nums[k - 1] \< k，同时nums[k] > k时，就将答案加上1。

另外需要特别注意两种特殊情况。第一种是一个都不选，此时对应的k为0，但是不存在第0小的数，因此此时只需检测nums[0]是否大于0即可。第二种则是全都选了，此时对应的k为n，但是不存在第n + 1小的数，因此此时只需检测nums[n - 1]是否小于n即可。

最后附上python代码：

```python
class Solution(object):
    def countWays(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        nums.sort()
        res = 0
        if nums[0] > 0:
            res += 1
        if nums[-1] < len(nums):
            res += 1

        for k in range(1, len(nums)):
            if nums[k - 1] < k and nums[k] > k:
                res += 1
        return res
```
