def _txt(S):
    if 'mid' not in S:
        return '二分答案：每座城市至少要有 `mid` 座电站，新增不超过 `k`'
    if 'now' not in S:
        return f"二分区间 `[{S['left']}, {S['right']}]`，试探 `mid = {S['mid']}`"
    i = S.get('i')
    if i is None:
        return f"试探 `mid = {S['mid']}`，已新增 `used = {S['used']}`"
    return f"城市 `{i}`：原始 + 新增有效电站 `now + used = {S['now']} + {S['used']}`，目标 `mid = {S['mid']}`"


CONFIG = dict(
    num=2528, title='最大化城市的最小电量', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分答案 · 滑动窗口 · 差分 · 贪心',
    tags=['二分算法', '常用数据结构', '难度分 2236'],
    code='''
class Solution(object):
    def maxPower(self, stations, r, k):

        left = min(stations)
        right = sum(stations) + k
        n = len(stations)
        while left < right:
            mid = (left + right + 1) >> 1
            f = [0] * n
            used = 0
            now = 0
            j = 0
            flag = True

            for i in range(n):
                if j < i:
                    j = i
                while j < n and j - i <= r:
                    now += stations[j]
                    j += 1
                
                now -= f[i]

                if now + used < mid:
                    delta = mid - now - used
                    if delta + used <= k:
                        used += delta
                        if i + r + r + 1 < n:
                            f[i + r + r + 1] += delta
                    else:
                        flag = False
                        break
            
                if i - r >= 0:
                    now -= stations[i - r]

            if flag:
                left = mid
            else:
                right = mid - 1
        
        return left
''',
    call='Solution().maxPower([1,2,0,3], 1, 2)',
    expect=4,
    max_steps=70,
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='array', var='stations', label='stations', h=150,
             pointers={'i': 'blue', 'j': 'pink'},
             dim=lambda S, i, v: 'now' in S and 'j' in S and 'i' in S and not (S['i'] - S['r'] <= i < S['j'])),
        dict(type='array', var='f', label='f（在这座城市失效的新增电站数）', h=150, pointers={'i': 'blue'},
             color=lambda S, i, v: 'yellow' if v else None),
    ],
    watch=['mid', 'i', 'j', 'now', 'used', 'k', 'left', 'right', ('flag', 'flag', 'green')],
    captions={
        'left = min(stations)': '下界 `left = {left}`：每座城市至少有这么多',
        'right = sum': '上界 `right = sum + k = {right}`',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，继续二分' if S.left < S.right else f'`left = right = {S.left}`，答案确定'),
        'mid = (left': '想让最少电站 ≥ `mid = {mid}`：因为取上中位数，所以 `left = mid` 不会死循环',
        'f = [0] * n': '重置 `f`：记录新增电站在哪座城市失效',
        'used = 0': '`used` = 当前仍有效的新增电站数',
        'now = 0': '`now` = 当前城市的原始有效电站数（滑动窗口）',
        'j = 0': '`j` = 窗口右边界（下一个要加入的电站）',
        'flag = True': '假设 `mid` 可行',
        'if j < i': lambda S, B, r: ('窗口右端落后于 `i`，拉到 `i`' if S.j < S.i else '`j` 不落后，不用动'),
        'while j < n and j - i <= r': lambda S, B, r_: (f'电站 `{S.j}` 在 `[i-r, i+r]` 内，加入窗口' if S.j < len(S.stations) and S.j - S.i <= S.r else f'`j = {S.j}`：窗口已覆盖到 `i+r` 或数组末尾，停止'),
        'now += stations[j]': '电站 `{B.j}` 进窗口：`now = {now}`',
        'now -= f[i]': '新增电站失效 `{f[i]}` 座 → `now = {now}`',
        'if now + used < mid': lambda S, B, r: (f'`{S.now} + {S.used} < {S.mid}` → 电量不够，需要补' if S.now + S.used < S.mid else f'`{S.now} + {S.used} ≥ {S.mid}` → 够了'),
        'delta = mid': '还缺 `delta = {mid} - {now} - {used} = {delta}` 座',
        'if delta + used <= k': lambda S, B, r: (f'`{S.delta} + {S.used} ≤ {S.k}`：预算够，建在 `i+r`（尽量靠后）' if S.delta + S.used <= S.k else f'`{S.delta} + {S.used} > {S.k}`：预算不够 → ==mid 不可行=='),
        'used += delta': '新增 `{delta}` 座：`used = {used}`',
        'f[i + r + r + 1] += delta': '这些电站覆盖到 `i+2r`，在 `{i + 2*r + 1}` 失效：`f[{i + 2*r + 1}] += {delta}`',
        'flag = False': '预算超了，`flag = False`，跳出循环',
        'now -= stations[i - r]': '`i` 右移前，移出窗口的原始电站 `stations[{i - r}]`：`now = {now}`',
        'left = mid': '`mid = {mid}` 可行 → `left = {left}`',
        'right = mid - 1': '`mid = {mid}` 不可行 → `right = {right}`',
        'return left': '答案 `{left}`',
    },
    cards=dict(
        one_liner='缝合怪：二分答案 + 滑动窗口 + 贪心 + 差分',
        complexity='时间 `O(n log(sum + k))`，空间 `O(n)`',
        problem=['`stations[i]` 是城市 i 的电站数，电站向两侧供电 `r` 格',
                 '再建 `k` 座，使==电量最小的城市==电量最大',
                 '本视频：`[1,2,0,3], r=1, k=2`'],
        quote='超级缝合怪的一题，综合了leetcode中最经常出现的滑动窗口、二分、贪心以及差分数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['电站越多越好 → 二分最后的答案 `mid`',
              '滑动窗口算 `now`；缺了就把新电站放在 `i + r`',
              '新电站到 `i + 2r + 1` 失效，记在 `f` 里，到时扣掉'],
        summary=['时间 `O(n log(sum + k))`，空间 `O(n)`',
                 '原文已是 Python 3 可运行写法，无需修改',
                 '二分取上中位数 `(l + r + 1) >> 1`，配合 `left = mid`',
                 '新电站放 `i + r` 才能最大覆盖后面的城市',
                 '对比灵神：灵神先用前缀和算 power、差分直接累加；yiduobo 用双指针窗口和 `f` 边扫边扣'],
    ),
)
