def _txt(S):
    if 'j' in S and 'now' in S and 'i' in S:
        return f"山峰 `i = {S['i']}`（高 {S['maxHeights'][S['i']]}）：当前高度 `now = {S['now']}`，这一侧累计 `s = {S['s']}`"
    if 'i' in S:
        return f"枚举山峰 `i = {S['i']}`，历史最优 `res = {S['res']}`"
    return ''


def _color(S, k, v):
    if 'i' not in S:
        return None
    if k == S['i']:
        return 'blue'
    if 'j' in S and k == S['j']:
        return 'pink'
    return None


CONFIG = dict(
    num=2865, title='美丽塔 I', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='枚举山峰 + 向两侧取最小值',
    tags=[],
    code='''
class Solution(object):
    def maximumSumOfHeights(self, maxHeights):

        res = 0
        n = len(maxHeights)
        for i in range(n):
            now = s = maxHeights[i]
            for j in range(i - 1, -1, -1):
                if maxHeights[j] < now:
                    now = maxHeights[j]
                s += now
            
            now = maxHeights[i]
            for j in range(i + 1, n):
                if maxHeights[j] < now:
                    now = maxHeights[j]
                s += now
            res = max(res, s)
        
        return res
''',
    call='Solution().maximumSumOfHeights([4,2,5,3])',
    expect=12,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='array', var='maxHeights', label='maxHeights（蓝 = 山峰 i，粉 = 正在向外走的 j）', pointers={'i': 'blue', 'j': 'pink'}, h=260,
             color=_color),
        dict(type='text', size=26, fn=lambda S: f"当前这一侧的高度：`now = {S['now']}` = 走过位置的 maxHeights 最小值" if 'now' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('now', 'now', 'cyan'), ('s', 's', 'green'), ('res', 'res', 'orange')],
    captions={
        'res = 0': '`res` 记录各个山峰里的最大高度和',
        'for i in range(n)': '枚举山峰下标 `i = {i}`',
        'now = s = maxHeights[i]': '山峰高度取满：`now = s = {maxHeights[i]}`',
        'for j in range(i - 1, -1, -1)': lambda S, B, r: ('`i = 0`：左边没有塔，不用走' if S.i == 0 else
                                                         ('左侧走完' if S.j == B.j == 0 else f'向左走：`j = {S.j}`')),
        'for j in range(i + 1, n)': lambda S, B, r: ('`i` 已是最右一座：右边没有塔' if S.i == len(S.maxHeights) - 1 else
                                                    ('右侧走完' if S.j == B.j == len(S.maxHeights) - 1 else f'向右走：`j = {S.j}`')),
        'if maxHeights[j] < now': lambda S, B, r: (
            f'`maxHeights[{S.j}] = {S.maxHeights[S.j]}` < `now = {S.now}` → 上限更低，高度被迫降到 `{S.maxHeights[S.j]}`'
            if S.maxHeights[S.j] < S.now else
            f'`maxHeights[{S.j}] = {S.maxHeights[S.j]}` ≥ `now = {S.now}` → 不能比邻居高，高度仍是 `{S.now}`'),
        'now = maxHeights[j]': '`now` 降为 `{now}`：往外只能不更高',
        's += now': '位置 `{j}` 取高度 `{now}`，`s` → =={s}==',
        'now = maxHeights[i]': '回到山峰，高度重新取 `{now}`，开始向右',
        'res = max': '山峰在 `{i}`：总和 `{s}`，`res = max({B.res}, {s})` = =={res}==',
        'return res': '最大高度和 =={ret}==',
    },
    skip=['n = len'],
    cards=dict(
        one_liner='枚举山峰，从峰顶向两侧走，高度只降不升',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['`maxHeights[i]` 是第 `i` 座塔的高度上限，只能削低', '要排成山形（先不降、后不增），求高度和的最大值',
                 '示例：`[5,3,4,1,1]` → `13`', '本视频：`[4,2,5,3]` → `12`，即 `[2,2,5,3]`'],
        quote='山峰位置是最特殊的，因此在这里就应该尝试枚举山峰的下标，然后计算选择当前下标作为山峰时两侧山坡上数值之和的最大值。',
        quote_src='—— yiduobo 题解原文',
        idea=['峰顶定下后，从峰顶向左向右走，每个位置的高度 = `min(上限, 靠近峰顶一侧邻居的高度)`',
              '这只和相邻位置有关，所以不需要 `h` 数组，用变量 `now` 迭代即可',
              '两侧对称：左边走一遍，右边走一遍，累加到同一个 `s`'],
        summary=['时间 `O(n^2)`（每个山峰各扫一遍），空间 `O(1)`；本题 `n ≤ 1000` 够用',
                 '易错：山峰自己的高度取满 `maxHeights[i]`，右侧开始前 `now` 要重置',
                 '`s` 里山峰只算一次，左右两遍都不重复加',
                 '原文已是 Python 3 可运行写法，代码未改动',
                 '对比灵神：灵神用单调栈把每个峰的左右和降到 `O(n)`；这里是朴素枚举'],
    ),
)
