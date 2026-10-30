from collections import deque
from typing import List

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))

class Solution994:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        fresh_count = 0
        rotten = deque()
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                if cell == 1:
                    fresh_count += 1
                elif cell == 2:
                    rotten.append((r, c))

        minutes = 0
        while rotten and fresh_count:
            minutes += 1
            for _ in range(len(rotten)):          # 只处理当前这一层
                r, c = rotten.popleft()
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh_count -= 1
                        rotten.append((nr, nc))
        return -1 if fresh_count else minutes

class Solution739:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        days_to_wait = [0] * len(temperatures)
        pending = []  # 单调栈：还没等到更高温度的日子（存下标）
        for day, temp in enumerate(temperatures):
            while pending and temp > temperatures[pending[-1]]:
                prev_day = pending.pop()
                days_to_wait[prev_day] = day - prev_day
            pending.append(day)
        return days_to_wait

class Solution3:
    def lengthOfLongestSubstring(self, s: str) -> int:
        max_len = left = 0
        char_count = {}
        for right, ch in enumerate(s):
            char_count[ch] = char_count.get(ch, 0) + 1
            while char_count[ch] > 1:          # 窗口里有重复字符，收缩左端
                char_count[s[left]] -= 1
                left += 1
            max_len = max(max_len, right - left + 1)
        return max_len

# --- original versions for cross-check
from collections import defaultdict
def ling3(s):
    ans = left = 0
    cnt = defaultdict(int)
    for right, c in enumerate(s):
        cnt[c] += 1
        while cnt[c] > 1:
            cnt[s[left]] -= 1
            left += 1
        ans = max(ans, right - left + 1)
    return ans
def yidu739(T):
    stack = [0]
    res = [0] * len(T)
    for index in range(1, len(T)):
        while stack and T[index] > T[stack[-1]]:
            res[stack[-1]] = index - stack[-1]
            stack.pop()
        stack.append(index)
    return res
def ling994(grid):
    m, n = len(grid), len(grid[0])
    fresh = 0
    q = []
    for i, row in enumerate(grid):
        for j, x in enumerate(row):
            if x == 1:
                fresh += 1
            elif x == 2:
                q.append((i, j))
    ans = 0
    while q and fresh:
        ans += 1
        tmp = q
        q = []
        for x, y in tmp:
            for i, j in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
                if 0 <= i < m and 0 <= j < n and grid[i][j] == 1:
                    fresh -= 1
                    grid[i][j] = 2
                    q.append((i, j))
    return -1 if fresh else ans

import random, copy
random.seed(0)
for _ in range(3000):
    R, C = random.randint(1, 6), random.randint(1, 6)
    g = [[random.choice([0, 1, 1, 2]) for _ in range(C)] for _ in range(R)]
    assert Solution994().orangesRotting(copy.deepcopy(g)) == ling994(copy.deepcopy(g)), g
    T = [random.randint(30, 40) for _ in range(random.randint(1, 12))]
    assert Solution739().dailyTemperatures(T) == yidu739(T)
    s = ''.join(random.choice('abcd ') for _ in range(random.randint(0, 15)))
    assert Solution3().lengthOfLongestSubstring(s) == ling3(s)
print('examples', Solution994().orangesRotting([[2,1,1],[1,1,0],[0,1,1]]), Solution994().orangesRotting([[2,1,1],[0,1,1],[1,0,1]]),
      Solution739().dailyTemperatures([73,74,75,71,69,72,76,73]), Solution3().lengthOfLongestSubstring('abcabcbb'))
print('all random tests passed')
