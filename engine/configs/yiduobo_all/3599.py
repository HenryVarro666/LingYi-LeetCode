N0 = [2, 3, 3, 2]
K0 = 3


def _cell(S, r, c, v):
    i, p = S.get('index'), S.get('p')
    if i is None or p is None or c == 0:
        return None
    if (r, c) == (i, p):
        return 'yellow'
    cp = S.get('cut_pos')
    if cp is not None and p > 1 and S.get('_line') in (14, 15, 16, 17) and (r, c) == (cp - 1, p - 1):
        return 'blue'
    return 'green' if v is not None else None


def _txt(S):
    i, p, cp = S.get('index'), S.get('p'), S.get('cut_pos')
    if i is None or p is None:
        return '`f[index][p]`：前 index+1 个数分成 p 段，==最大段异或==的最小值'
    if p > 1 and cp is not None and S.get('_line') in (14, 15, 16, 17):
        nums = S['nums']
        return (f'最后一段 `nums[{cp}..{i}]` 异或 = ==`{S["xor"]}`==，'
                f'前面 `f[{cp - 1}][{p - 1}]` = `{S["f"][cp - 1][p - 1]}` → 取大 ==`{v_max(S)}`==')
    return f'`f[{i}][{p}]`：前 {i + 1} 个数分成 {p} 段'


def v_max(S):
    return max(S['f'][S['cut_pos'] - 1][S['p'] - 1], S['xor'])


CONFIG = dict(
    num=3599, title='划分数组得到最小 XOR', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='划分型 DP · 倒着枚举最后一段',
    tags=['灵神核心路线', '灵神题单·图论算法', '难度分 1955'],
    code='''
class Solution(object):
    def minXor(self, nums, k):
        
        n = len(nums)

        f = [[None] * (k + 1) for _ in range(n)]
        for index in range(n):
            for p in range(1, k + 1):
                if p == 1:
                    if index == 0:
                        f[index][p] = nums[index]
                    else:
                        f[index][p] = f[index - 1][p] ^ nums[index]
                else:
                    xor = 0
                    for cut_pos in range(index, p - 2, -1):
                        xor ^= nums[cut_pos]
                        v = max(f[cut_pos - 1][p - 1], xor)
                        if f[index][p] is None or f[index][p] > v:
                            f[index][p] = v

        return f[-1][-1]
''',
    call=f'Solution().minXor({N0!r}, {K0})',
    expect=2,
    skip=['n = len(nums)', 'for p in range', 'else:'],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = index，粉 = 最后一段起点 cut_pos）', h=190, cell=90,
             pointers={'index': 'blue', 'cut_pos': 'pink'},
             color=lambda S, i, v: ('pink' if S.get('cut_pos') is not None and S.get('p', 1) > 1 and S.get('_line') in (14, 15, 16, 17) and S['cut_pos'] <= i <= S['index'] else None)),
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='table', var='f', label='f[index][p]（行 = index，列 = p；黄 = 当前，蓝 = 依赖）', h=300, cell=90,
             rows=lambda S: [str(i) for i in range(len(S['nums']))], cols=lambda S: [str(j) for j in range(S['k'] + 1)],
             color=_cell),
    ],
    max_steps=56,
    watch=[('index', 'index', 'blue'), ('p', 'p', 'yellow'), ('cut_pos', 'cut_pos', 'pink'), ('xor', 'xor', 'cyan'), ('v', 'v', 'orange')],
    captions={
        'f = [[None]': '`f[index][p]`：前 `index+1` 个数分成 `p` 段时，==最大段异或==的最小值；`None` = 还没算',
        'for index in range': lambda S, B, r: (f'`index = {S.index}`：算前 {S.index + 1} 个数的所有分段数 `p`' if S.get('index') != B.get('index') else '所有 `index` 都算完了'),
        'if p == 1': lambda S, B, r: (f'`p = 1`：只有一段，整个前缀就是这一段' if S.p == 1 else f'`p = {S.p} > 1`：枚举最后一段的起点 `cut_pos`'),
        'if index == 0': lambda S, B, r: ('第一个数：`f[0][1] = nums[0]`' if S.index == 0 else '前面已有 `f[index-1][1]`，再异或上 `nums[index]`'),
        'f[index][p] = nums[index]': '`f[{index}][1] = {nums[index]}`',
        'f[index][p] = f[index - 1][p] ^': '一段的异或前缀：`f[{index}][1] = f[{index-1}][1] ^ {nums[index]}` = =={f[index][p]}==',
        'xor = 0': '最后一段的异或从 0 开始，==倒着==枚举起点，每次只多异或一个数',
        'for cut_pos in range': lambda S, B, r: ('这一组 `p` 的起点都试完了' if S.get('cut_pos') is not None and S.cut_pos == B.get('cut_pos') and S.xor == B.get('xor')
                                                 else f'`cut_pos` 最小到 `p-1 = {S.p - 1}`：前面还要给 `p-1` 段留 `p-1` 个数'),
        'xor ^= nums[cut_pos]': '最后一段 `nums[{cut_pos}..{index}]` 的异或 `xor` = =={xor}==',
        'v = max(': '这种分法：前面 `f[{cut_pos-1}][{p-1}] = {f[cut_pos-1][p-1]}`，最后一段 `{xor}` → 最大段 `v` = =={v}==',
        'if f[index][p] is None': lambda S, B, r: ('`f[{}][{}]` 还没值 → 直接记下 `v = {}`'.format(S.index, S.p, S.v) if S.f[S.index][S.p] is None
                                                  else (f'`f[{S.index}][{S.p}] = {S.f[S.index][S.p]} > v = {S.v}` → ==更小，更新==' if S.f[S.index][S.p] > S.v
                                                        else f'`f[{S.index}][{S.p}] = {S.f[S.index][S.p]} <= v = {S.v}` → 不更新')),
        'f[index][p] = v': '`f[{index}][{p}]` = =={v}==',
        'return f[-1][-1]': '前 `{n}` 个数分 `{k}` 段，最大段异或最小 = =={ret}==',
    },
    cards=dict(
        one_liner='枚举最后一段，取「前面最大」与「这一段」的较大者，再取最小',
        complexity='时间 `O(k·n^2)`，空间 `O(n·k)`',
        problem=['把整数数组 `nums` 分成 `k` 个非空子数组，每段算按位异或',
                 '求这 `k` 段异或值中的 ==最大值== 的 ==最小值==',
                 '示例：`nums = [2,3,3,2], k = 3` → `2`（`[2] [3,3] [2]`，异或 2、0、2）'],
        quote='经典的划分类问题，令f[index][p]表示将前index个数划分成p个子数组时，这些子数组中最大异或值的最小值……由于是从后往前枚举，因此这个异或值只需在之前的基础上再异或当前元素就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p = 1`：一段到底，就是前缀异或',
              '`p > 1`：从后往前枚举最后一段的起点 `cut_pos`，`xor` 每次只多异或一个数',
              '`f[index][p] = min(max(f[cut_pos-1][p-1], xor))`'],
        summary=['时间 `O(k·n^2)`，空间 `O(n·k)`',
                 '易错：`cut_pos` 下界是 `p-1`，要给前面的 `p-1` 段留数',
                 '「最大值的最小值」：单种分法取 `max`，所有分法取 `min`',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
