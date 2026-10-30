## 前后缀分解
### 答案 = 前缀部分 + 后缀部分； 而不是暴力去重新计算整个区间
class Solution:
    def maxScore(self, s: str) -> int:
        # 一开始假设“全部在右边”，所以右边的 1 就是总数
        right1 = s.count("1")
        ans = left0 = 0
        # 不遍历最后一个字符，因为分割后右边至少要有一个字符
        for c in s[:-1]:
            if c == "0":
                left0 += 1
            else: # c == '1'
                right1 -= 1
            ans = max(ans,left0+right1)
        return ans


## 合并变量
### 把 left0 和 right1 合并成一个变量 score.如果 s[i]=0，那么左边多了个 0，把 score 增加 1。否则 s[i]=1，那么右边少了个 1，把 score 减少 1。
class Solution:
    def maxScore(self, s: str) -> int:
        score = s. count("1")
        ans = 0
        for c in s[:-1]:
            score += 1 if c == "0" else -1
            ans = max (ans, score)
        return ans


## 拆分变量，一次遍历
class Solution:
    def maxScore(self, s: str) -> int:
        cnt1 = delta = 0
        max_delta = -inf
        for c in s[:-1]:
            cnt1 += 1 if c == '1' else 0
            delta += 1 if c == '0' else -1
            max_delta = max(max_delta, delta)
        return max_delta + cnt1 + int(s[-1])