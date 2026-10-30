ARR = [1, 5, 7, 8, 6, 3, 4, 2, 9]
DIFF = -2


def _idx(S):
    return S['arr'].index(S['num']) if 'num' in S else None


def _col(S, i, v):
    if 'num' not in S:
        return None
    if v == S['num']:
        return 'blue'
    if 'pre' in S and v == S['pre'] and i < _idx(S):
        return 'orange'
    return None


def _txt(S):
    if 'pre' not in S or 'num' not in S:
        return '`f[x]` = 以 `x` 结尾的最长定差子序列长度；转移 `f[x] = f[x − difference] + 1`'
    num, pre = S['num'], S['pre']
    have = S['f'].get(pre, 0)
    if S.get('now') is not None and S.get('_line', 0) in (7, 8):
        return f'`f[{num}] = f[{pre}] + 1` = `{have} + 1` = =={S["now"]}=='
    return f'`num = {num}` 的前一项应是 `{num} − ({DIFF}) = {pre}`，`f[{pre}]` = =={have}=='


CONFIG = dict(
    num=1218, title='最长定差子序列', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='线性 DP · 字典代替二维表',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def longestSubsequence(self, arr, difference):

        f = {}
        for num in arr:
            pre = num - difference
            now = f.get(pre, 0) + 1
            f[num] = now
        
        return max(f.values())
''',
    call=f'Solution().longestSubsequence({ARR!r}, {DIFF})',
    expect=4,
    views=[
        dict(type='array', var='arr', label='arr（蓝 = 当前数，橙 = 它的前一项 pre）', h=200, cell=90, color=_col),
        dict(type='map', var='f', label='f（键 = 结尾的数，值 = 最长长度）', fmt=lambda k, v: f'{k}: {v}', h=190, font=30),
        dict(type='text', fn=_txt, size=26, h=90),
    ],
    watch=[('num', 'num', 'blue'), ('pre', 'pre', 'orange'), ('now', 'now', 'green')],
    captions={
        'f = {}': '`f[x]`：以 `x` 结尾的最长定差子序列长度。每一轮只依赖上一轮，所以==省掉一维==，用字典存',
        'for num in arr': lambda S, B, r: (f'依次处理 `num = {S.num}`：把它放在某个子序列的末尾' if S.num != B.get('num')
                                           else '所有数都处理完了'),
        'pre = num - difference': '公差是 `{difference}`，所以 `{num}` 的前一项必须是 `{num} − ({difference}) = {pre}`',
        'now = f.get': lambda S, B, r: (f'`f[{S.pre}]` 存在（长度 {S.f[S.pre]}）→ 接在它后面：`now = {S.f[S.pre]} + 1 = {S.now}`' if S.pre in S.f
                                        else f'前面没出现过 `{S.pre}` → `{S.num}` 只能自己做开头：`now = 0 + 1 = 1`'),
        'f[num] = now': '记下 `f[{num}] = {now}`',
        'return max': '答案是所有结尾里最长的：`max(f.values())` = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='每个数只问一句：它的前一项 num−d 结尾的链有多长',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定整数数组 `arr` 和整数 `difference`',
                 '求 `arr` 中最长的等差子序列，相邻两项之差恰好等于 `difference`',
                 '示例：`[1,5,7,8,5,3,4,2,1]`，`difference = -2` → `4`；本视频：`[1,5,7,8,6,3,4,2,9]` → `4`'],
        quote='令f[i][j]表示前i个数中，以j为结尾时最长定差子序列的长度，那么对于f[i][j]而言，其上一位必然是f[i - 1][j - diff]。由于这里每一轮的结果都是从上一轮得来的，因此可以省去一维。',
        quote_src='—— yiduobo 题解原文',
        idea=['公差固定，所以以 `num` 结尾的链，上一项必然是 `num − difference`',
              '前 i 个数最多 i 个不同结尾，用字典代替大数组',
              '遍历顺序保证 `f[pre]` 里存的都是出现在 `num` 左边的数'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`pre = num - difference`，公差为负时 `pre` 比 `num` 大',
                 '`f.get(pre, 0) + 1`：没有前一项时长度为 1',
                 '重复数值：后出现的覆盖先出现的，因为靠右的更有机会接更长',
                 '对比等差数列题 1027：公差固定，所以不用二维状态'],
    ),
)
