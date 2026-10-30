def _win(S):
    """current window of start points counted in cnt: [index-maxJump, index-minJump] (shifted by 1 after the slide)"""
    if 'index' not in S:
        return None
    sh = 1 if S.get('_line', 0) >= 18 else 0
    return S['index'] + sh - S['maxJump'], S['index'] + sh - S['minJump']


def _fc(S, i, v):
    w = _win(S)
    if w is None:
        return None
    if i == S['index'] and S.get('_line', 0) < 18:
        return 'pink'
    return 'blue' if w[0] <= i <= w[1] else None


def _show(S):
    if 'index' not in S:
        return '`f[i]`：能否跳到 `i`；`cnt`：滑窗内 True 的个数'
    lo, hi = _win(S)
    return f'滑窗 `f[{max(lo, 0)}..{hi}]` 里有 =={S["cnt"]}== 个 True（`cnt`）'


CONFIG = dict(
    num=1871, title='跳跃游戏 VII', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='DP + 定长滑动窗口计数',
    tags=['滑动窗口与双指针', '常用数据结构', '难度分 1896'],
    code='''
class Solution(object):
    def canReach(self, s, minJump, maxJump):

        cnt = 1
        f = [True]
        for index in range(1, minJump):
            f.append(False)
        
        n = len(s)
        for index in range(minJump, n):
            if s[index] == '1' or cnt == 0:
                f.append(False)
            else:
                f.append(True)

            if index - maxJump >= 0:
                if f[index - maxJump]:
                    cnt -= 1
            
            if f[index - minJump + 1]:
                cnt += 1

        return f[-1]
''',
    call="Solution().canReach('0110100', 2, 3)",
    expect=True,
    views=[
        dict(type='text', fn=_show, size=26, h=70),
        dict(type='string', var='s', label='s', h=170, pointers={'index': 'pink'},
             color=lambda S, i, v: 'pink' if i == S.get('index') else None),
        dict(type='array', var='f', label='f[i]：能否跳到 i（蓝色 = 滑窗）', h=190, color=_fc),
    ],
    watch=[('index', 'index', 'pink'), ('cnt', 'cnt', 'green'), ('minJump', 'minJump', 'blue'), ('maxJump', 'maxJump', 'blue')],
    captions={
        'cnt = 1': '`cnt` = 滑窗里 True 的个数；`f[0]` 是 True，所以初始 `cnt = 1`',
        'f = [True]': '起点一定能到：`f[0] = True`',
        'for index in range(1, minJump)': '`f[1]` 到 `f[minJump-1]`：一步最少跳 `minJump`，必然跳不到',
        'f.append(False)': lambda S, B, ret: (f'`f[{len(S.f) - 1}] = False`' if S.get('_line') == 7 else '这台跳不到：`f` 末尾加 False'),
        'for index in range(minJump, n)': '从 `index = {index}` 开始求 `f[index]`',
        "if s[index] == '1'": lambda S, B, ret: (f"`s[{S.index}] = '1'`：落脚点不能是 1 → 跳不到" if S.s[S.index] == '1' else (f'`cnt = 0`：窗口 `[{S.index - S.maxJump}, {S.index - S.minJump}]` 里没有能到的点 → 跳不到' if S.cnt == 0 else f"`s[{S.index}] = '0'` 且 `cnt = {S.cnt} > 0`：窗口里有起跳点 → ==能跳到==")),
        'f.append(True)': '`f[{index}] = True`',
        'if index - maxJump >= 0': lambda S, B, ret: (f'窗口右移：左端 `index - maxJump = {S.index - S.maxJump}` 要滑出去' if S.index - S.maxJump >= 0 else f'`index - maxJump = {S.index - S.maxJump}` < 0：窗口左端还没到数组里，没有东西滑出'),
        'if f[index - maxJump]': lambda S, B, ret: (f'`f[{S.index - S.maxJump}]` 是 True → 滑出去了，`cnt` 减 1' if S.f[S.index - S.maxJump] else f'`f[{S.index - S.maxJump}]` 是 False → 对计数没影响'),
        'cnt -= 1': '`cnt` → {cnt}',
        'if f[index - minJump + 1]': lambda S, B, ret: (f'新进窗口的右端 `f[{S.index - S.minJump + 1}]` 是 True → `cnt` 加 1' if S.f[S.index - S.minJump + 1] else f'新进窗口的右端 `f[{S.index - S.minJump + 1}]` 是 False → 不变'),
        'cnt += 1': '`cnt` → {cnt}',
        'return f[-1]': '`f[n-1] = {f[-1]}`',
    },
    cards=dict(
        one_liner='f[i] 只看窗口里有没有 True：窗口随 i 滑动，只维护个数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二进制串 `s`，从 0 出发，每步跳 `[minJump, maxJump]`，只能落在 `\'0\'`',
                 '问能否到达最后一个下标',
                 '本视频：`s="0110100"`，`minJump=2`，`maxJump=3` → `true`'],
        quote='对于f[i]，只需要检测f[i - maxJump]到f[i - minJump]之间是否有一个为true就行了。……这里区间是一个定长的区间，那么就可以使用滑动窗口。',
        quote_src='—— yiduobo 题解原文',
        idea=['`index` 能到 ⇔ 落脚点是 `0`，且 `[index-maxJump, index-minJump]` 里有 True',
              '窗口定长，用 `cnt` 记 True 的个数就不用枚举',
              '`index` 右移：左端 `index-maxJump` 出窗，右端 `index+1-minJump` 进窗'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：先用 `cnt` 判断 `f[index]`，再滑窗更新 `cnt`',
                 '`f[1..minJump-1]` 必为 False；`cnt` 初值 1 来自 `f[0]`',
                 '原文为 Python 2 风格，在 Python 3 下无需修改，已原样使用',
                 '对比灵神：灵神用 `sum_` 前缀和相减，yiduobo 用滑窗计数 `cnt`'],
    ),
)
