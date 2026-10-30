CONFIG = dict(
    num=1705, title='吃苹果的最大数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='最小堆 + 腐烂日期贪心',
    tags=['贪心与思维', '难度分 1930'],
    code='''
class Solution:
    def eatenApples(self, apples: List[int], days: List[int]) -> int:
        ans = 0
        h = []
        for i, (num, day) in enumerate(zip(apples, days)):
            while h and h[0][0] == i:  # 已腐烂
                heappop(h)
            if num:
                heappush(h, [i + day, num])
            if h:
                ans += 1
                h[0][1] -= 1  # 吃一个最早腐烂的苹果
                if h[0][1] == 0:
                    heappop(h)

        i = len(apples)
        while True:
            while h and h[0][0] <= i:  # 已腐烂
                heappop(h)
            if not h:
                return ans
            rotten_day, num = heappop(h)
            k = min(num, rotten_day - i)
            ans += k
            i += k
''',
    call='Solution().eatenApples([1,2,3,5,2], [3,2,1,4,2])',
    expect=7,
    views=[
        dict(type='array', var='apples', pointers={'i': 'blue'}, label='apples（第 i 天新长出的苹果数）', h=170),
        dict(type='heap', var='h', fmt=lambda x: f'第{x[0]}天烂×{x[1]}', h=200),
        dict(type='text', fn=lambda S: f"今天是第 `{S['i']}` 天，已吃 ==`{S['ans']}`== 个" if 'i' in S and 'ans' in S else '', h=70),
    ],
    watch=[('i', 'i', 'blue'), ('ans', 'ans', 'green'), ('堆大小', 'len(h)', 'yellow')],
    captions={
        'while h and h[0][0] == i': lambda S, B, r: (f'堆顶 `{S.h[0]}` 的腐烂日 == 今天 `{S.i}` → 已烂，弹出' if S.h and S.h[0][0] == S.i
                                                      else f'堆顶没烂（或堆空）→ 不用再弹'),
        'if num': '今天长出 `{num}` 个苹果（有苹果才入堆）',
        'heappush(h, [i + day': '入堆 `[腐烂日={i + day}, 个数={num}]`：==按腐烂日排序==，最早烂的在堆顶',
        'ans += 1': '堆不空 → 今天吃一个，`ans` → =={ans}==',
        'h[0][1] -= 1': '吃==最早腐烂==的那堆：剩 `{h[0][1]}` 个。先吃它，否则明天可能就烂了',
        'if h[0][1] == 0': lambda S, B, r: ('这堆吃完了 → 弹出' if S.h[0][1] == 0 else '这堆还有剩，留在堆里'),
        'i = len(apples)': '前 n 天结束。==第 n 天之后仍可继续吃==，从 `i = {i}` 起直接按堆里的苹果批量吃',
        'while True': '循环到堆为空为止',
        'while h and h[0][0] <= i': lambda S, B, r: (f'堆顶腐烂日 `{S.h[0][0]}` ≤ `{S.i}` → 已烂，弹出' if S.h and S.h[0][0] <= S.i
                                                      else '堆顶还没烂（或堆空）'),
        'if not h': lambda S, B, r: f'堆空了 → 没苹果可吃，返回 `{S.ans}`' if not S.h else '堆里还有苹果，继续',
        'rotten_day, num = heappop': '取出最早腐烂的一堆：`{num}` 个，第 `{rotten_day}` 天烂',
        'k = min(num, rotten_day - i)': '腐烂前能吃 `min({num}, {rotten_day} − {i})` = =={k}== 个（吃完，或吃到烂的前一天）',
        'ans += k': '`ans` += {k} → =={ans}==',
        'i += k': '一次跳过 `{k}` 天：`i` → {i}',
        'return ans': '堆空，一共吃了 `{ret}` 个',
    },
    cards=dict(
        one_liner='先吃最早腐烂的苹果，堆里存「腐烂日, 个数」',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['第 `i` 天树上长出 `apples[i]` 个苹果，`days[i]` 天后烂掉；每天最多吃一个',
                 '求最多能吃多少个（第 n 天之后还可以继续吃）',
                 '示例：`apples=[1,2,3,5,2]`，`days=[3,2,1,4,2]` → `7`'],
        quote='对于两个苹果 A 和 B，设 A 更早腐烂，那么应该先吃 A。如果先吃 B，可能下一天 A 就烂了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最小堆按==腐烂日期==排序，堆里一项 = 一批同日腐烂的苹果',
              '前 `n` 天：每天先弹掉烂的，再入堆新苹果，吃堆顶一个',
              '第 `n` 天后不再有新苹果：一批一批吃，`k = min(个数, 腐烂日 − i)`，==直接跳 k 天=='],
        summary=['时间 `O(n log n)`：每批苹果最多入堆出堆一次',
                 '易错点：==第 n 天之后还能吃==，要一直模拟到堆空',
                 '腐烂日是 `i + day`，第 `i + day` 天那天已经不能吃，所以用 `==` / `<=` 弹出',
                 '优化前写法：第 n 天后仍逐天吃，慢在 `O(U)` 次循环；优化后一次吃一批'],
    ),
)
