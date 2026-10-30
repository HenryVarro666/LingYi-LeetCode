def _info(S):
    if 'index' not in S or 'r' not in S or S['_line'] < 10:
        return '换个角度：对每个房间 `index`，数有多少个起点能在这里得分'
    i = S['index']
    if 'h' not in S or S['_line'] < 13:
        return f'房间 `{i}`：`requirement = {S["r"]}`'
    if 'left' in S and S['_line'] >= 17 and S['left'] is not None:
        return f"房间 `{i}`，余量 `h = {S['h']}`：二分 `p`，区间 `[{S['left']}, {S['right']}]`（要 `s[{i}] − s[p] ≤ {S['h']}` 的最小 `p`）"
    return f"房间 `{i}`：`h = hp − requirement = {S['h']}`，起点到这里最多能扣 `{S['h']}` 血"


CONFIG = dict(
    num=3771, title='探索地牢的得分', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='换个方向数 · 前缀和 + 二分',
    tags=['贪心与思维', '难度分 1981'],
    code='''
class Solution(object):
    def totalScore(self, hp, damage, requirement):
        
        s = [damage[0]]
        for d in damage[1:]:
            s.append(s[-1] + d)
        
        res = 0
        for index, r in enumerate(requirement):
            if r > hp:
                continue
            
            h = hp - r
            if s[index] <= h:
                res += index + 1
            else:
                left = 0
                right = index
                while left < right:
                    mid = (left + right) // 2
                    if s[index] - s[mid] > h:
                        left = mid + 1
                    else:
                        right = mid

                res += index - left
        
        return res
''',
    call='Solution().totalScore(10, [3,2,4,1], [2,5,3,4])',
    expect=7,
    views=[
        dict(type='text', fn=_info, size=25, h=60),
        dict(type='array', var='damage', label='damage', pointers={'index': 'blue'}, cell=84, h=150),
        dict(type='array', var='requirement', label='requirement', cell=84, h=135,
             color=lambda S, i, v: 'blue' if 'index' in S and i == S['index'] else None),
        dict(type='array', var='s', label='s（前缀和）', cell=84, h=170,
             pointers={'left': 'cyan', 'right': 'pink', 'mid': 'yellow'},
             ),
    ],
    watch=['hp', ('index', 'index', 'blue'), ('h', 'h', 'yellow'), ('left', 'left', 'cyan'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        's = [damage[0]]': '`s[i]` = `damage[0..i]` 的和；`damage` 为正，所以 `s` ==单调递增==，可以二分',
        's.append': '`s` 追加 `{s[-1]}`（前一项 + `{d}`）',
        'res = 0': '`res` 累计「每个房间有多少起点能得分」',
        'for index, r': lambda S, B, rr: (f'看房间 `{S.index}`：`requirement = {S.r}`' if 'index' not in B or B.index != S.index else '所有房间都看完了'),
        'if r > hp': lambda S, B, rr: (f'`requirement = {S.r} > hp = {S.hp}`：连满血都达不到 → 这个房间谁也拿不到分，跳过' if S.r > S.hp else f'`requirement = {S.r} ≤ hp = {S.hp}`：有可能拿到分'),
        'continue': '跳过这个房间',
        'h = hp - r': '`h = hp − r = {h}`：从起点到 `index` 这段最多只能扣 `{h}` 点血',
        'if s[index] <= h': lambda S, B, rr: (f'`s[{S.index}] = {S.s[S.index]} ≤ h = {S.h}`：从房间 0 出发都扣得起 → ==前面所有 {S.index + 1} 个起点都能得分==' if S.s[S.index] <= S.h else f'`s[{S.index}] = {S.s[S.index]} > h = {S.h}`：从房间 0 出发扣血太多，要二分找最早能得分的起点'),
        'res += index + 1': '`res += {index} + 1` → `{res}`',
        'left = 0': '二分的下界 `left = 0`',
        'right = index': '上界 `right = {right}`：`p = index` 一定满足（`s[index] − s[index] = 0 ≤ h`）',
        'while left < right': lambda S, B, rr: (f'`left = {S.left} < right = {S.right}`：区间没缩完，继续' if S.left < S.right else f'`left = {S.left} = right`：找到最小的 `p = {S.left}`'),
        'mid = ': '`mid = ({left} + {right}) // 2 = {mid}`',
        'if s[index] - s[mid] > h': lambda S, B, rr: (f'`s[{S.index}] − s[{S.mid}] = {S.s[S.index] - S.s[S.mid]} > h = {S.h}`：从 `mid` 之后出发还是扣太多 → 起点要再往后，`left = mid + 1`' if S.s[S.index] - S.s[S.mid] > S.h else f'`s[{S.index}] − s[{S.mid}] = {S.s[S.index] - S.s[S.mid]} ≤ h = {S.h}`：扣得起 → `mid` 可能就是答案，往左找，`right = mid`'),
        'left = mid + 1': '`left` → {left}',
        'right = mid': '`right` → {right}',
        'res += index - left': '最小的 `p = {left}`，起点 `{left + 1}..{index}` 共 `{index} − {left}` 个得分 → `res` = =={res}==',
        'return res': '所有房间的得分起点数相加：`{res}`',
    },
    skip=['s.append', 'left = 0'],
    max_steps=90,
    cards=dict(
        one_liner='不算每个起点的得分，改数每个房间有几个起点拿分',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`hp` 点生命，进入房间 `i` 扣 `damage[i]`',
                 '扣完后剩余生命 `≥ requirement[i]` 就得 1 分',
                 '`score(j)` = 从房间 `j` 一路走到底的得分；求所有 `score` 之和',
                 '本视频：`hp=10, damage=[3,2,4,1], requirement=[2,5,3,4]` → `7`'],
        quote='对于score[index]，由于damage是正整数数组，因此随着向后移动，hp必然是逐渐减少的。但是这里的requirement并不是单调的，因此直接计算每个score[index]是比较麻烦的，不妨换一个思路。',
        quote_src='—— yiduobo 题解原文',
        idea=['换成对每个房间 `index`，数有多少起点能在这里得分，`requirement` 的影响就消掉了',
              '起点 `p+1..index`：要求 `s[index] − s[p] ≤ h = hp − requirement[index]`',
              '`requirement > hp` 直接跳过；`s[index] ≤ h` 时全部 `index + 1` 个起点都行',
              '否则在 `[0, index]` 二分最小的 `p`，贡献 `index − p`'],
        result='运行结束，返回 `7`：每个房间的得分起点数之和 `1+2+2+2`',
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：`requirement[index] > hp` 要先跳过，否则 `h` 为负',
                 '二分区间是 `[0, index]`，`right = index` 时 `s[index] − s[index] = 0` 必满足',
                 '这里的 `s[i]` 含 `damage[i]`（从 0 开始的前缀和），所以和灵神的 `s[i+1]` 差一位',
                 '原文为 Python 2 风格，仅沿用原代码，没有需要改动的地方'],
    ),
)
