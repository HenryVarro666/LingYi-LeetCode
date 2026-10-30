---
title: "3458. 选择K个互不重叠的特殊子字符串"
aliases: ["yiduobo的每日leetcode 3458.选择K个互不重叠的特殊子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/depth-first-search", "leetcode/graph", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1894477525658367045"
zhihu_id: "1894477525658367045"
zhihu_title: "yiduobo的每日leetcode 3458.选择K个互不重叠的特殊子字符串"
question_id: "3458"
question: "选择 K 个互不重叠的特殊子字符串"
problem_url: "https://leetcode.cn/problems/select-k-disjoint-special-substrings/"
difficulty: "Medium"
rating: 1520
created: "2025-04-12T20:16:10+08:00"
updated: "2025-04-12T20:16:10+08:00"
upvotes: 0
comments: 0
---

# 3458. 选择K个互不重叠的特殊子字符串

> **[yiduobo的每日leetcode 3458.选择K个互不重叠的特殊子字符串](https://zhuanlan.zhihu.com/p/1894477525658367045) · 知乎 · 2025-04-12 · 赞同 0**
> 力扣：[3458. 选择 K 个互不重叠的特殊子字符串](https://leetcode.cn/problems/select-k-disjoint-special-substrings/) · Medium · 灵茶山艾府：[有向图建模+合并区间+无重叠区间（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3458.选择K个互不重叠的特殊子字符串

[3458. 选择 K 个互不重叠的特殊子字符串 - 力扣（LeetCode）](https://leetcode.cn/problems/select-k-disjoint-special-substrings/description/)

题目给出一个长度为n的字符串s以及一个整数k，现在要求判断能否从s中选出k个互不重叠的特殊子串。特殊子串指的是：

1、子串中的任何字符都不应该出现在子串之外

2、子串不是整个字符串s

问能否选出k个这样的互不重叠的特殊子串。

对于选出的某个子串sub，若其包含了字母c，那么其就必须包含所有的c，也就是说其至少需要包含pos[c][0]到pos[c][-1]之间的所有字符，在这里pos[c]记录的是c在s中出现的所有位置，按从小到大的顺序排列。

另一方面，在pos[c][0]到pos[c][-1]之间可能包含了其他的字符，这样的话有需要该字符进行扩展，而扩展后的字符区间可能需要继续迭代扩展，实现起来会比较麻烦，不妨换一种角度来思考。

对于两种不同的字符串first和second，若second出现在pos[first][0]以及pos[first][-1]之间，那么如果子串中包含了字符first，那么就必须包含所有的second，可以发现这是一种有向关系。这里之所以说是有向关系，理由是仅靠上面的包含关系只能推导出想要包含字符first就必须包含字符second，反过来却不一定成立，例如字符串"abba"，想要包含a就必须包含b，反之选择两个b不选择a也是可行的方案。

更进一步的，如果将每种字符都视为有向图中的点，包含关系视为图中的有向边，那么就可以建立起一张有向图。对于包含关系则可以通过二分查找来进行确认，即对于first和second，先找出second所有下标中最小的，且大于pos[first][0]的下标，若这个下标小于pos[first][-1]，那么就说明second被first包含了。

接下来对于图中的某个节点，若想选择该节点，就必须选择所有可以直接或者间接到达该节点的节点，而问题就变成了可以选择的节点组数是否大于等于k。

可以发现，为了使得选择的组数尽可能多，就应该优先选择入度为0的点，理由是对于入度非0的点，想选取这些点就需要牵扯到其他的点，而一个入度非0的点可能牵扯到多个入度为0的点，这样是不优的。

选择完所有入度为0的点之后，从这些点出发可以到的点就不可以再选取了，但是除了这些点之外，还有一种可能就是图中形成了没有其他点可以到达的环。例如字符串abcabc，三个字符两两之间都互为包含与被包含的关系，其中没有入度为0的点，但是可以将这三个点作为一组一次性选取。为了处理这种情况，就应该先计算有向图中的强连通分量，将这些连通分量中的所有节点收缩成一个单独的节点，这样一来就得到了一张有向无环图，此时再选取其中入度为0的点即可。

最后附上python代码：

```python
class Solution(object):
    def maxSubstringLength(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: bool
        """
        
        pos = {}
        for index, char in enumerate(s):
            if char not in pos:
                pos[char] = []
            pos[char].append(index)
        
        g = {char : set() for char in pos}
        for first in pos:
            for second in pos:
                if first == second or pos[first][0] > pos[second][-1]:
                    continue
                
                left = 0
                right = len(pos[second]) - 1
                while left < right:
                    mid = (left + right) // 2
                    if pos[second][mid] < pos[first][0]:
                        left = mid + 1
                    else:
                        right = mid
                
                if pos[second][left] < pos[first][-1]:
                    g[second].add(first)
        
        low = {}
        dfn = {}
        stack = []
        stack_set = set()
        belong = {}

        global timestamp, tot
        timestamp = 0
        tot = 0

        def dfs(now):
            global timestamp, tot
            timestamp += 1
            low[now] = timestamp
            dfn[now] = timestamp
            stack.append(now)
            stack_set.add(now)

            for nxt in g[now]:
                if nxt not in dfn:
                    dfs(nxt)
                    low[now] = min(low[now], low[nxt])
                elif nxt in stack_set:
                    low[now] = min(low[now], dfn[nxt])
            
            if low[now] == dfn[now]:
                v = -1
                while v != now:
                    v = stack.pop()
                    stack_set.remove(v)
                    belong[v] = tot
                tot += 1
        
        for char in g:
            if char not in dfn:
                dfs(char)
        
        if tot == 1:
            return k == 0

        new_g = [set() for _ in range(tot)]
        ind = [0] * tot
        for x in g:
            for y in g[x]:
                if belong[x] != belong[y] and belong[y] not in new_g[belong[x]]:
                    new_g[belong[x]].add(belong[y])
                    ind[belong[y]] += 1
        
        cnt = 0
        for index in range(tot):
            if ind[index] == 0:
                cnt += 1
        
        return cnt >= k
```
