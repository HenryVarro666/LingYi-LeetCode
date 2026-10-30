---
title: "3998. 使用子序列排序转换二进制字符串"
aliases: ["yiduobo的每日leetcode 3998.使用子序列排序转换二进制字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/四-双序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2063806531691451071"
zhihu_id: "2063806531691451071"
zhihu_title: "yiduobo的每日leetcode 3998.使用子序列排序转换二进制字符串"
question_id: "3998"
question: "使用子序列排序转换二进制字符串"
problem_url: "https://leetcode.cn/problems/transform-binary-string-using-subsequence-sort/"
difficulty: "Medium"
rating: 1862
created: "2026-07-24T02:28:57+08:00"
updated: "2026-07-24T02:28:57+08:00"
upvotes: 1
comments: 0
---

# 3998. 使用子序列排序转换二进制字符串

> **[yiduobo的每日leetcode 3998.使用子序列排序转换二进制字符串](https://zhuanlan.zhihu.com/p/2063806531691451071) · 知乎 · 2026-07-24 · 赞同 1**
> 力扣：[3998. 使用子序列排序转换二进制字符串](https://leetcode.cn/problems/transform-binary-string-using-subsequence-sort/) · Medium · 灵茶山艾府：[贪心 + 双指针（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3998.使用子序列排序转换二进制字符串

<https://leetcode.cn/problems/transform-binary-string-using-subsequence-sort/description/>

题目给出一个二进制字符串s。

另外给出一个字符串数组strs，其中每个strs[index]的长度都与s相同，且仅由字符'0'、'1'、'?'组成。每个'?'可以替换为'0'或者'1'。

现在可以执行一下操作任意次，包括0次：

- 选择s中的任意子序列sub
- 将sub中的0全部移动到1的左侧
- 将移动后的sub替换s中原来的子序列，其余字符保持不变

要求返回一个布尔数组ans，若可以将strs[index]中的所有'?'替换为'0'或者'1'，然后使用上述操作将s变为strs[index]，那么ans[index]为true，否则为false。

各个strs之间没有可以关联起来的地方，因此在这里只能逐个遍历，然后检测能否对s进行操作使其变为当前遍历到的strs。

对于当前遍历到的字符串，方便起见，将其记为t。首先可以明确的是，若某个下标index对应的s[index]与t[index]相同，那么index就没有必要加入到子序列中，因为不可能将另一种字符换位到index处，这也就意味着这个位置对其他位置的匹配没有帮助。接下来，对于每个下标index，s[index]和t[index]就只有4中不同的组合，分别是

- s[index]为1，t[index]为0
- s[index]为0，t[index]为1
- s[index]为0，t[index]为？
- s[index]为1，t[index]为？

对于以上的组合，两种带？的是比较灵活的。这两种组合既可以帮助其他两种组合补位，也可以直接作为相同字符的配对不参与操作，那么重点就在于分析s1t0以及s0t1这两种组合。

可以发现，题目中的操作只能将0放到1的左侧，因此若当前有一个靠前的下标位置满足s0t1，同时其左侧既没有落单的s1t0的位置，也没有落单的s1t？的位置，那么这个位置就不肯能变为相同，理由是左侧没有需要换位的1，那么当前s的这个0就不可能被换走。

反过来，对于s1t0的情况，则较为宽松，只需要其右侧存在落单的s0t1或者s0t?的位置就行了。

基于这一点，就可以使用三个变量one_zero、one_q以及zero_q分别对应前缀中落单的：

- s[index]为1，t[index]为0的下标数量one_zero
- s[index]为1，t[index]为？的下标数量one_q
- s[index]为0，t[index]为？的下标数量one_zero

接下来对于当前遍历到的位置：

1、若s[index]与t[index]相同，那么直接跳过

2、若s[index]为1，t[index]为0，那么将one_zero加上1

3、若s[index]为1，t[index]为？，那么将one_q加上1

4、若s[index]为0，t[index]为？，那么将zero_q加上1。这里有些变化。需要注意的是，zero_q只有两种作用，分别是作为s0t1与one_zero中的下标配对，以及作为s0t0直接不参与操作。这里的配对操作只能与其左侧的s1t0执行，例如以下两个例子

s \= 10, t \= 0？。对于这个例子，让t变为01，然后s重新排列也可以变成01

s \= 01，t \= ?0。对于这个例子，即使让t变为10，s重新排列也没法变成10

换言之，这里的zero_q应该将上限设置为当前的one_zero。若zero_q大于one_zero，那么多出的zero_q就应该全部转化为s0t0，因此在这还需要取zero_q \= min(zero_q, one_zero)

5、若s[index]为0，t[index]为1，且one_zero > 0：

此时就应该让一组s1t0与当前的s0t1配对，也就是形如1XXX...XX0与0XXX...XX1中的10与01配对，此时就可以对10进行操作变为01。在这里应该优先使用掉落单的one_zero而不是one_q，因为one_q可以自行消化。

那么对于这种情况，应该先将one_zero减去1，然后也需要注意处理可用的zero_q \= min(zero_q, one_zero)

6、若s[index]为0，t[index]为1，且one_q > 0：

此时就应该使用one_q来配对s0t1，此时直接将one_q减去1即可

7、若s[index]为0，t[index]为1，且one_zero以及one_q都为0：

这种情况就是上面说的s0t1左侧没有落单的s1t0以及s1t?，也就是说无解，这一组t对应的答案就是false

若遍历完成也没有出现情况7，那么还需要用zero_q来消化掉多出来的one_zero。若zero_q大于等于one_zero，那么答案就是true，此时多出来的zero_q以及one_q都可以自行消化；反之，答案就是false，即s1t0的右侧没有落单的s0t1或者s0t?可用。

最后附上python代码：

```python
class Solution(object):
    def transformStr(self, s, strs):
        """
        :type s: str
        :type strs: List[str]
        :rtype: List[bool]
        """
        
        res = []
        for t in strs:
            one_q = 0
            zero_q = 0
            one_zero = 0

            flag = True
            for index in range(len(s)):
                if s[index] == t[index]:
                    continue
                if s[index] == '1' and t[index] == '0':
                    one_zero += 1
                elif s[index] == '1' and t[index] == '?':
                    one_q += 1
                elif s[index] == '0' and t[index] == '?':
                    zero_q += 1
                    zero_q = min(zero_q, one_zero)
                elif one_zero > 0:
                    one_zero -= 1
                    zero_q = min(zero_q, one_zero)
                elif one_q > 0:
                    one_q -= 1
                else:
                    flag = False
                    break
            
            if flag and one_zero <= zero_q:
                res.append(True)
            else:
                res.append(False)
        
        return res
```
