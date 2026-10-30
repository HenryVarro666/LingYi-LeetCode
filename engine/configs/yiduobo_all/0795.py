CONFIG = dict(
    num=795, title='区间子数组个数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='固定区间起点向右扩展', tags=['三指针', '难度分 1817'],
    code='''
class Solution(object):
    def numSubarrayBoundedMax(self, A, L, R):
        res = 0
        start_pos = None
        last_pos = None
        for index, now in enumerate(A):
            if now > R:
                start_pos = None
                last_pos = None
            else:
                if start_pos is None:
                    start_pos = index
                if now >= L:
                    last_pos = index
                if last_pos is not None:
                    res += last_pos - start_pos + 1

        return res
''',
    call='Solution().numSubarrayBoundedMax([2,9,2,5,6], 2, 8)',
    expect=7,
    views=[
        dict(type='text', size=30, fn=lambda S: (f"以 `{S['index']}` 结尾：起点 `{S['start_pos']}`，最后一个 >= L 的位置 `{S['last_pos']}` → ==`{S['last_pos'] - S['start_pos'] + 1}`== 个" if 'index' in S and S.get('start_pos') is not None and S.get('last_pos') is not None else f"范围 `[{S['L']}, {S['R']}]`")),
        dict(type='array', var='A', h=300, pointers={'index': 'green', 'start_pos': 'pink', 'last_pos': 'blue'},
             color=lambda S, idx, v: ('pink' if v > S['R'] else 'blue' if v >= S['L'] else None) if 'R' in S else None,
             dim=lambda S, idx, v: 'index' in S and idx > S['index']),
    ],
    watch=[('index', 'index', 'green'), ('start_pos', 'start_pos', 'pink'), ('last_pos', 'last_pos', 'blue'), ('res', 'res', 'green')],
    captions={
        4: '`start_pos`：当前区间的起点，None 表示还没有',
        5: '`last_pos`：区间里最右一个 >= L 的位置',
        'for index, now': '扫描到 `A[{index}] = {now}`',
        'if now > R': lambda S, B, r: (f'`{S.now} > {S.R}`：它==永远不能进答案==，之前的区间也不能越过它' if S.now > S.R else f'`{S.now} <= {S.R}`：可以放进区间'),
        8: '超过 R：起点清空，区间断开',
        9: '`last_pos` 也清空，后面要重新找 >= L 的数',
        'if start_pos is None': lambda S, B, r: (f'区间还没起点 → 以 `{S.index}` 作起点（小于 L 的数也可能被后面的大数带动）' if S.start_pos is None else f'已有起点 `{S.start_pos}`，不动'),
        'start_pos = index': '`start_pos` → {start_pos}',
        'if now >= L': lambda S, B, r: (f'`{S.now} >= {S.L}`：可以当最大值 → 记 `last_pos = {S.index}`' if S.now >= S.L else f'`{S.now} < {S.L}`：自己不能独立成答案，`last_pos` 不变'),
        'last_pos = index': '`last_pos` → {last_pos}',
        'if last_pos is not None': lambda S, B, r: ('区间里有 >= L 的数 → 可以数合法区间' if S.last_pos is not None else '还没有 >= L 的数，以此为右端点的合法区间为 0'),
        'res += ': '起点取 `{start_pos} … {last_pos}`，右端点 {index}：共 `{last_pos} - {start_pos} + 1 = {last_pos - start_pos + 1}` 个 → `res` = =={res}==',
        'return res': '共 `{res}` 个',
    },
    cards=dict(
        one_liner='区间起点固定，遇到 > R 就断开，数 [start, last] 之间的起点',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组 `A` 和范围 `[L, R]`，数最大值在范围内的连续子数组个数',
                 '示例：`[2,9,2,5,6]`，`L=2, R=8` → `7`'],
        quote='若now大于R，那么说明该节点无论如何都不可能加入到答案中，且以start_pos为起点的区间也没有可能再往右扩展了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now > R`：起点和 `last_pos` 都清空',
              '否则没有起点就以当前下标作起点，`now >= L` 就更新 `last_pos`',
              '以 index 为右端点的合法区间有 `last_pos - start_pos + 1` 个'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '小于 L 的数不能独立成答案，但可以被前面的大数带动',
                 '易错：`last_pos` 为 None 时不能累加，断开后两个变量都要清空',
                 '原文为 Python 2 风格，只删去了函数开头的空行',
                 '对比灵神：灵神用 i0、i1 做差，不需要 None'],
    ),
)
