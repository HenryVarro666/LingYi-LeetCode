CONFIG = dict(
    num=1985, title='找出数组中的第 K 大整数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='自定义比较排序（Go 原文转写）',
    setup='from functools import cmp_to_key',
    code='''
class Solution:
    def kthLargestNumber(self, a: List[str], k: int) -> str:
        a.sort(key=cmp_to_key(lambda s, t: -1 if len(s) > len(t) or len(s) == len(t) and s > t else 1))
        return a[k - 1]
''',
    call="Solution().kthLargestNumber(['2','21','12','1','10'], 3)",
    expect='10',
    views=[
        dict(type='text', size=28, h=110, fn=lambda S: '比较规则：==位数多的更大==；位数相同再比字符串字典序（`len(s) > len(t)` 或 `len` 相等且 `s > t`）'),
        dict(type='array', var='a', h=260, label='a（排序后：从大到小）', cell=110,
             pointers={'k - 1': 'green'} ,
             color=lambda S, i, v: 'green' if S.get('_line') == 4 and i == S['k'] - 1 else None),
        dict(type='text', size=30, h=110, fn=lambda S: (f"第 `{S['k']}` 大 = 下标 `{S['k']-1}` 的元素 ==`{S['a'][S['k']-1]}`==" if S.get('_line') == 4 else '')),
    ],
    watch=[('k', 'k', 'blue'), ('a', 'a', 'green')],
    captions={
        'a.sort': lambda S, B, r: f"按规则从大到小排序：位数多的在前，位数相同比字典序（数字串等长时字典序 = 数值大小）。`a` 变成 `{S.a}`",
        'return a[k - 1]': '降序后第 `k` 大就在下标 `k - 1`：`a[{k - 1}]` = =={a[k - 1]}==',
    },
    cards=dict(
        one_liner='字符串不能直接转整数比较：先比长度，再比字典序',
        complexity='时间 `O(nm log n)`，空间 `O(log n)`（m 为串长）',
        problem=['`nums` 里每个字符串都是不含前导零的整数，返回第 `k` 大的那个字符串',
                 '重复的数字算不同元素',
                 '示例：`["3","6","7","10"], k=4` → `"3"`'],
        quote='sort.Slice(a, func(i, j int) bool { s, t := a[i], a[j]; return len(s) > len(t) || len(s) == len(t) && s > t })',
        quote_src='—— 灵茶山艾府题解代码（Go）',
        idea=['没有前导零：位数多的数一定更大',
              '位数相同，字符串字典序就是数值大小',
              '按这个规则降序排序，答案就是 `a[k-1]`'],
        after=[dict(heading='为什么这样比', lines=['`"10"` 和 `"9"`：字典序 `"10" < "9"`，但数值 `10 > 9`', '所以先比位数：`2` 位 > `1` 位，`"10"` 更大', '位数相同（如 `"21"`、`"12"`）再比字典序，结果和数值一致'])],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`sort.Slice` 的 less 函数用 `functools.cmp_to_key` 表达，返回 -1 表示排前面）',
                 '时间 `O(nm log n)`，比较两个串最坏 `O(m)`',
                 '易错点：不能直接比字符串（"10" < "9"）；降序后取下标 `k-1`',
                 '无前导零是比较规则成立的前提'],
    ),
)
