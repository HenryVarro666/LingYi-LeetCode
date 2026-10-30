CONFIG = dict(
    num=3190, title='使所有元素都可以被 3 整除的最少操作数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='按模 3 余数分类',
    tags=[],
    code='''
class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        return sum(x % 3 != 0 for x in nums)
''',
    call='Solution().minimumOperations([1,2,3,4,6,8])',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: '按 `x % 3` 分类：余 0 不用动（绿），余 1 减一、余 2 加一，都只要 ==1 次== 操作', size=30, h=110),
        dict(type='array', var='nums', h=260, label='nums',
             color=lambda S, i, v: 'green' if v % 3 == 0 else 'orange'),
        dict(type='text', fn=lambda S: '余数：' + '  '.join(f'`{v}%3={v % 3}`' for v in S['nums']), size=28, h=110),
    ],
    watch=[('不是 3 的倍数的个数', 'sum(x % 3 != 0 for x in nums)', 'green')],
    captions={
        'return sum': '逐个判断 `x % 3 != 0`：不是 3 的倍数的元素各要 1 次操作，共有 =={sum(x % 3 != 0 for x in nums)}== 个，返回它',
    },
    cards=dict(
        one_liner='不是 3 的倍数的数，加一或减一就够了，答案就是它们的个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次操作可把任意一个元素 `+1` 或 `-1`',
                 '求让所有元素都能被 `3` 整除的最少操作数',
                 '示例：`[1,2,3,4]` → `3`'],
        quote='对于不是 3 的倍数的元素，只需操作一次就可以变成 3 的倍数。所以答案为不是 3 的倍数的元素个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按模 `3` 的余数分三类：`3k`、`3k+1`、`3k+2`',
              '`3k+1` 减一、`3k+2` 加一，都是 ==一步到位==',
              '所以逐个数 `x % 3 != 0` 就行，一行代码'],
        after=[dict(heading='思考题：把 3 改成 m', lines=['余数 `r = x % m`：减 `r` 次，或加 `m - r` 次', '每个数的代价是 `min(r, m - r)`', '`m = 3` 时 `r` 只能是 1 或 2，代价恒为 1', '所以才能写成「数个数」这样的一行'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`x % 3 != 0` 是布尔值，`sum` 直接把 True 当 1 累加',
                 '思考题：改成 `m`，余数 `r` 的代价是 `min(r, m - r)`，要逐个累加',
                 '本例 `[1,2,3,4,6,8]`：1、2、4、8 各一次，共 4'],
    ),
)
