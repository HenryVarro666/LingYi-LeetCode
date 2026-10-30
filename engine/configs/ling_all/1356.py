def _pc(v):
    return bin(v).count('1')


CONFIG = dict(
    num=1356, title='根据数字二进制下 1 的数目排序', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='双关键字排序',
    tags=['灵神题单', '位运算', '难度分 1258'],
    code='''
class Solution:
    def sortByBits(self, arr: List[int]) -> List[int]:
        arr.sort(key=lambda x: (x.bit_count(), x))
        return arr
''',
    call='Solution().sortByBits([7, 3, 8, 5, 6, 1, 2, 4])',
    expect=[1, 2, 4, 8, 3, 5, 6, 7],
    views=[
        dict(type='text', size=28, fn=lambda S: '排序后：每个数的 `bit_count`（二进制 1 的个数）' if S['_line'] >= 4 else '排序前：每个数的 `bit_count`（二进制 1 的个数）'),
        dict(type='array', var='arr', h=200, cell=90,
             color=lambda S, i, v: {1: 'green', 2: 'blue', 3: 'pink'}.get(_pc(v)) if S['_line'] >= 4 else None),
        dict(type='text', size=28, fn=lambda S: '`(1 的个数, 数值)`：' + ' '.join(f"({_pc(v)},{v})" for v in S['arr'])),
        dict(type='text', size=28, fn=lambda S: '颜色：绿 = 1 个 1，蓝 = 2 个 1，粉 = 3 个 1' if S['_line'] >= 4 else ''),
    ],
    watch=[('arr', 'arr', 'blue')],
    captions={
        'arr.sort': '按 `(x.bit_count(), x)` 排序：先比 ==1 的个数==，个数相同再比 ==数值==。`arr` 变成 `{arr}`',
        'return arr': '`1` 个 1 的 `1, 2, 4, 8` 在前，`2` 个 1 的 `3, 5, 6` 居中，`7` 排最后 → 返回 `{arr}`',
    },
    cards=dict(
        one_liner='双关键字排序：先比 1 的个数，再比数值',
        complexity='时间 `O(n log n)`，空间 `O(1)`（忽略排序栈开销）',
        problem=['把数组按二进制里 ==1 的个数== 升序排',
                 '个数相同的，按 ==数值== 升序',
                 '示例：`[0,1,2,3,4,5,6,7,8]` → `[0,1,2,4,8,3,5,6,7]`'],
        quote='双关键字排序。对于 arr 中的两个数：先比较二者的二进制 1 的个数是否相同，若不同，1 的个数少的排前面。若二进制 1 的个数相同，那么数值小的排前面。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序的 key 返回元组 `(x.bit_count(), x)`，Python 按元组字典序比较',
              '第一项就是 1 的个数，第二项是数值本身，正好对应题意的两条规则',
              '一行 `arr.sort(...)` 原地排序，再返回 `arr`'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '`int.bit_count()` 要 Python 3.10+，旧版本可用 `bin(x).count("1")`',
                 '`arr.sort` 是原地排序，返回的就是 `arr` 本身',
                 '易错：只按 1 的个数排会丢掉“数值升序”的要求（虽然稳定排序碰巧保持原顺序，但输入不是升序时就错了）'],
    ),
)
