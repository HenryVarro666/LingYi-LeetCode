CONFIG = dict(
    num=2154, title='将找到的值乘以 2', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='哈希集合 · 枚举 original·2^k',
    tags=['灵神题单', '位运算'],
    code='''
class Solution:
    def findFinalValue(self, nums: List[int], original: int) -> int:
        st = set(nums)
        while original in st:
            original *= 2
        return original
''',
    call='Solution().findFinalValue([5,3,6,1,12], 3)',
    expect=24,
    views=[
        dict(type='array', var='nums', label='nums', h=190,
             color=lambda S, i, v: 'green' if 'original' in S and v == S['original'] else None),
        dict(type='set', var='st', label='st = set(nums)', h=230,
             fmt=lambda x: str(x)),
        dict(type='text', fn=lambda S: (f"当前要找的 original = ==`{S['original']}`==，它{'在' if S['original'] in S.get('st', ()) else '不在'} st 中"
                                        if 'st' in S else ''), size=34, h=100),
    ],
    watch=[('original', 'original', 'blue')],
    captions={
        'st = set': '把 `nums` 放进哈希集合，之后判断“在不在”只要 `O(1)`',
        'while original in st': lambda S, B, r: (f'`{S.original}` 在 `st` 中 → 找到了，要继续翻倍' if S.original in S.st
                                                 else f'`{S.original}` 不在 `st` 中 → 停止，它就是 ==最终值=='),
        'original *= 2': '找到了就乘 2：`original` = =={original}==，下一轮找 `original · 2^k` 的下一个',
        'return original': '返回第一个不在 `nums` 中的 `original · 2^k` = =={ret}==',
    },
    cards=dict(
        one_liner='枚举 original·2^k，返回第一个不在 nums 里的',
        complexity='时间 `O(n + log(U/original))`，空间 `O(n)`',
        problem=['在 `nums` 中找 `original`，找到就翻倍再找，找不到就停', '示例：`nums=[5,3,6,1,12]`，`original=3` → `24`（3→6→12→24）',
                 '示例：`nums=[2,7,9]`，`original=4` → `4`'],
        quote='返回不在 nums 中的最小的 original·2^k，其中 k 是非负整数。枚举 k=0,1,2,… 判断 original·2^k 是否在 nums 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把题意换个说法：找最小的、不在 `nums` 中的 `original·2^k`', '用哈希集合 `st` 记录 `nums`，判断是否存在只要 `O(1)`',
              '每次翻倍，最多 `log(U/original)` 轮'],
        after=[dict(heading='方法二、三：只记录可能值', lines=['只有 `x = original·2^k` 才有用：`x % original == 0` 且商是 2 的幂', '方法三把 `k` 压进 `mask`，答案是 mask 最低的 0 对应的 `2^k`'])],
        summary=['时间 `O(n + log(U/original))`，空间 `O(n)`',
                 '易错：题目是“找到才翻倍”，一旦找不到立刻停，不要继续往后找更大的倍数',
                 '`while original in st` 用 `list` 判断会退化成 `O(n)`，要用集合',
                 '相似题：2568. 最小无法得到的或值'],
    ),
)
