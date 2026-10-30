CONFIG = dict(
    num=2605, title='从两个数字数组里生成最小数字', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 · 交集 / 最小值拼接',
    tags=[],
    code='''
class Solution:
    def minNumber(self, nums1: List[int], nums2: List[int]) -> int:
        s = set(nums1) & set(nums2)
        if s: return min(s)  # 有交集
        x, y = min(nums1), min(nums2)
        return min(x * 10 + y, y * 10 + x)
''',
    call='Solution().minNumber([4, 1, 3], [5, 7])',
    expect=15,
    views=[
        dict(type='array', var='nums1', label='nums1', h=150,
             color=lambda S, i, v: 'green' if 'x' in S and v == S['x'] else None),
        dict(type='array', var='nums2', label='nums2', h=150,
             color=lambda S, i, v: 'green' if 'y' in S and v == S['y'] else None),
        dict(type='set', var='s', fmt=lambda x: str(x), label='交集 s', h=150),
        dict(type='text', fn=lambda S: (f"两种拼法：`{S['x']}{S['y']}` 和 `{S['y']}{S['x']}`，取小的" if 'x' in S else ('有交集：取交集里最小的' if S.get('s') else ('' if 's' not in S else '交集为空：只能一个数位来自 nums1、另一个来自 nums2'))), size=32),
    ],
    watch=['s', 'x', 'y'],
    captions={
        's = set(nums1)': '`set(nums1) & set(nums2)` = `{s}`：两个数组共有的数字',
        'if s: return': lambda S, B, r: ('交集 `{}` 非空：单个数字就同时满足两个数组 → 取最小的 ==' + str(min(S.s)) + '==') if S.s else '交集为空 `set()` → 一位数不可能同时在两个数组里，要拼两位数',
        'x, y = min': '各取最小值：`x = {x}`（nums1），`y = {y}`（nums2）：两位数要尽量小，两个数位都取最小',
        'return min(x * 10': '两位数的十位更重要：`{x}{y}` = {x*10+y}，`{y}{x}` = {y*10+x}，取较小者 =={ret}==',
    },
    cards=dict(
        after=[dict(heading='有交集时', lines=['`nums1=[3,5,2,6], nums2=[3,1,7]`：交集 `{3}`', '`if s: return min(s)` 直接返回 `3`，后面两行不会执行', '一位数一定比任何两位数小'])],
        one_liner='有交集取交集最小值，没交集就拼两个最小值',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['两个数组，元素是 1 到 9 的互不相同数字',
                 '求最小的数，使两个数组都至少含它的某个数位',
                 '示例：`nums1=[4,1,3], nums2=[5,7]` → `15`'],
        quote='如果 nums1 与 nums2 有交集，那么答案就是交集的最小值。如果没有交集，设 nums1 的最小值为 x，nums2 的最小值为 y，答案就是 min(10x+y, 10y+x)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['有公共数字 `c`：一位数 `c` 就满足，没有比一位数更小的',
              '没有公共数字：至少要两位，每个数组各出一个数位，各自取最小值',
              '两个数位怎么摆：试 `10x+y` 与 `10y+x`，取较小的'],
        summary=['时间 `O(n+m)`，空间 `O(1)`（数字只有 1 到 9）',
                 '易错点：有交集时答案是一位数，必须先判断交集再拼两位数',
                 '灵神还提到方法二：用位运算当集合，交集就是按位与'],
    ),
)
