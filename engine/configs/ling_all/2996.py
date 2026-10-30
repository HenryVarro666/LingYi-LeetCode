def _xi(S):
    x = S.get('x')
    if x is None or x not in S['nums']:
        return None
    return S['nums'].index(x)


def _txt(S):
    if 'st' in S:
        return f"`s = {S['s']}`：在不在 nums 里？" + (' ==在，继续加 1==' if S['s'] in S['st'] else ' ==不在，就是答案==')
    if 'x' in S:
        return f"当前前缀和 `s = {S['s']}`，比较相邻两项 `{S['x']}` 和 `{S['y']}`"
    return f"`s = nums[0] = {S['s']}`，单个元素本身就是顺序前缀"


def _col(S, i, v):
    xi = _xi(S)
    if 'st' in S:
        return 'yellow' if v == S['s'] else None
    if xi is None:
        return 'green' if i == 0 else None
    if i <= xi:
        return 'green'
    if i == xi + 1:
        return 'blue'
    return None


CONFIG = dict(
    num=2996, title='大于等于顺序前缀和的最小缺失整数', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='找最长顺序前缀 + 哈希集合',
    code='''
class Solution:
    def missingInteger(self, nums: List[int]) -> int:
        s = nums[0]
        for x, y in pairwise(nums):
            if x + 1 != y:
                break
            s += y

        st = set(nums)
        while s in st:  # 至多循环 n 次，例如 1324567
            s += 1
        return s
''',
    call='Solution().missingInteger([3,4,5,1,12,14,13])',
    expect=15,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', color=_col, h=230),
        dict(type='set', var='st', h=200, fmt=lambda x: str(x)),
    ],
    watch=[('s', 's', 'green'), 'x', 'y'],
    captions={
        's = nums[0]': '单个元素也是顺序前缀：`s = nums[0] = {s}`',
        'if x + 1 != y': lambda S, B, r: (f'`{S.x} + 1 = {S.x + 1}`，`y = {S.y}`，相邻差 1 → ==顺序前缀继续=='
                                          if S.x + 1 == S.y else
                                          f'`{S.x} + 1 = {S.x + 1} ≠ {S.y}`：顺序断了 → ==break=='),
        's += y': '`y = {y}` 属于前缀，累加：`s = {s}`',
        'st = set': '前缀和 `s = {s}`，把 nums 放进哈希集合，O(1) 判断是否存在',
        'while s in st': lambda S, B, r: (f'`{S.s}` 在 nums 里 → 还不能当答案，继续 +1' if S.s in S.st
                                          else f'`{S.s}` 不在 nums 里 → ==停下，它就是最小缺失整数=='),
        's += 1': '还在 nums 里，`s` 加 1 → {s}',
        'return s': '答案：`{s}`',
    },
    cards=dict(
        one_liner='先累加最长顺序前缀，再从前缀和往上找第一个不在数组里的数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['顺序前缀：从 `nums[0]` 开始，每项都比前一项大 1',
                 '求 ==不在 nums 中== 且 ==≥ 最长顺序前缀和== 的最小整数',
                 '示例：`[3,4,5,1,12,14,13]` → 前缀和 12，12 13 14 都在 → `15`'],
        quote='遍历 nums，寻找最长前缀。在此过程中累加遍历过的元素，得到 s。找到最长前缀后，反复把 s 增加 1，直到 s 不在 nums 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`pairwise` 每次看相邻两项，`x + 1 != y` 就 break，否则 `s += y`',
              '用哈希集合 `st` 判断 `s` 是否出现过，出现就 `s += 1`'],
        summary=['时间 `O(n)`，空间 `O(n)`（哈希集合）',
                 '`s` 初始是 `nums[0]`，只有一个元素也算顺序前缀',
                 '第二个循环至多 n 次，例如 `1324567`：前缀和 1，之后 1 到 7 都在数组里',
                 '易错：是「≥ 前缀和」，前缀和本身不在数组里就直接返回'],
    ),
)
