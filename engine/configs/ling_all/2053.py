ARR = ['d', 'b', 'c', 'b', 'c', 'a']

CONFIG = dict(
    num=2053, title='数组中第 K 个独一无二的字符串', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表计数 + 按序数第 k 个（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def kthDistinct(self, a: List[str], k: int) -> str:
        cnt = defaultdict(int)
        for s in a:
            cnt[s] += 1
        for s in a:
            if cnt[s] == 1:
                k -= 1
                if k == 0:
                    return s
        return ""
''',
    call=f'Solution().kthDistinct({ARR}, 2)',
    expect='a',
    views=[
        dict(type='array', var='a', label='a（蓝 = 当前扫描的字符串）', cell=96, h=190,
             color=lambda S, i, v: 'blue' if 's' in S and S['_line'] >= 4 and S.get('s') == v else None),
        dict(type='map', var='cnt', label='cnt（字符串 → 出现次数）', fmt=lambda k, v: f"'{k}': {v}", h=190, font=34),
        dict(type='text', h=90, size=30,
             fn=lambda S: f"还差 `k = {S['k']}` 个独一无二的字符串" if S['_line'] >= 6 else '第一遍：统计每个字符串出现几次'),
    ],
    watch=[('s', 's', 'blue'), ('k', 'k', 'orange')],
    captions={
        'cnt = defaultdict': '先建一个计数的哈希表 `cnt`',
        'cnt[s] += 1': "`'{s}'` 出现次数 +1 → `{cnt[s]}`",
        4: "第一遍：取 `'{s}'`",
        6: "第二遍：==按原数组顺序==看 `'{s}'`（题目要的是出现顺序的第 k 个）",
        'if cnt[s] == 1': lambda S, B, ret: (f"`'{S.s}'` 只出现 1 次 → 独一无二" if S.cnt[S.s] == 1
                                            else f"`'{S.s}'` 出现了 {S.cnt[S.s]} 次 → 不是独一无二，跳过"),
        'k -= 1': '又找到一个独一无二的：还差 `k` → {k}',
        'if k == 0': lambda S, B, ret: (f'`k = 0`：刚好是第 k 个，就是它' if S.k == 0 else f'`k = {S.k}`，还没数够，继续往后找'),
        'return s': "第 k 个独一无二的字符串是 `'{s}'`",
        'return ""': '扫完都不够 k 个 → 返回空字符串',
    },
    cards=dict(
        one_liner='先数次数，再扫一遍，把 k 减到 0 的那个就是答案',
        complexity='时间 `O(L)`，空间 `O(L)`，`L` 为所有字符串总长',
        problem=['只出现 ==一次== 的字符串叫独一无二',
                 '返回数组中按原顺序的第 `k` 个独一无二字符串，不足 `k` 个返回 `""`',
                 '示例：`["d","b","c","b","c","a"]`，`k = 2` → `"a"`'],
        idea=['第一遍：`cnt` 记录每个字符串的出现次数',
              '第二遍：按原顺序扫，`cnt[s] == 1` 就 `k -= 1`',
              '`k` 减到 0 的那个字符串就是第 k 个'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`map[string]int` → `defaultdict(int)`，`if k--; k == 0` 拆成两行）',
                 '时间 `O(L)`，空间 `O(L)`',
                 '易错：要按数组顺序扫，不能遍历哈希表',
                 '不足 `k` 个时 Go 返回零值空串，Python 里显式 `return ""`'],
    ),
)
