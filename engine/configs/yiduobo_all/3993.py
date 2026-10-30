CONFIG = dict(
    num=3993, title='交替数列的最大元素', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='构造 + 奇偶分情况推导',
    tags=[],
    code='''
class Solution(object):
    def maximumValue(self, n, s, m):
        
        if n == 1:
            return s
        return s + (m - 1) * (n // 2 - 1) + m
''',
    call='Solution().maximumValue(7, 3, 5)',
    expect=3+5+4*2,
    views=[
        dict(type='text', size=34, h=140, fn=lambda S: "构造：`s → s+m → s+m−1 → s+m−1+m → …`，多加 `m`，少减（只减 `1`）"),
        dict(type='text', size=34, h=140, fn=lambda S: (
            f"`n // 2 − 1` = `{S['n']//2-1}` 组「加 m 减 1」，再加一次 m：`{S['s']} + {S['n']//2-1}×{S['m']-1} + {S['m']}` = =={S['s']+(S['n']//2-1)*(S['m']-1)+S['m']}==" if 'n' in S and S['n'] > 1 else '')),
    ],
    watch=['n', 's', 'm'],
    captions={
        'if n == 1': '`n = {n}`：`n == 1` 要特判（公式假设至少有一次加 m），这里 `n ≥ 2`，往下算',
        'return s + (m': '`n = {n}` 时 `n // 2 − 1 = {n//2-1}` 次「加 m 减 1」，再加最后一个 `m` → =={ret}==',
    },
    cards=dict(
        one_liner='尽量多加 m、减法只减 1，按奇偶分析次数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给 `n`、`s`、`m`：序列首项 `s`，相邻升降交替，相邻差绝对值 `≤ m`',
                 '问所有有效序列中可能出现的最大元素',
                 '示例：`n=4, s=3, m=5` → `12`；本视频用 `n=7`'],
        quote='题目要求找出可能出现的最大元素，那么在这里就应该按照 s -> s + m -> s + m - 1 -> s + m - 1 + m -> ... 这样构造，也就是尽量多做加m，而减法则只减去1。',
        quote_src='—— yiduobo 题解原文',
        idea=['去掉首项 `s`，剩下 `n−1` 项两两一组，共 `(n−1)//2` 组',
              '`n−1` 为奇数：最后多一次加 m，它就是答案；`n−1` 为偶数：倒数第二次加 m 是答案',
              '两种情况还原到 `n`，次数都是 `n//2 − 1`，答案同为 `s + (n//2−1)(m−1) + m`'],
        summary=['时间、空间都是 `O(1)`',
                 '公式默认至少有一次加 m，所以 `n == 1` 必须单独返回 `s`',
                 '原文本身可直接在 Python 3 运行，未做修改',
                 '对比灵神：灵神先讲 `n=2` 再推广，yiduobo 按 `n` 的奇偶拆开推导'],
    ),
)
