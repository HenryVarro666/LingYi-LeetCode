NUMS = [-1, 10, 6, 7, -7, 1]


def _col(S, i, v):
    if 'x' not in S or S['_line'] == 9:
        return None
    # 当前遍历位置：按 s 中的元素数判断（元素互不相同）
    cur = len(S['s']) if S['_line'] != 8 else len(S['s']) - 1
    if i == cur:
        return 'yellow'
    if i < cur:
        return 'cyan'
    return None


def _if(S, B, ret):
    x = S.x
    if -x in S.s:
        return f'`-x = {-x}` 在哈希表里：左边出现过它的相反数 → ==找到一对 ±{abs(x)}=='
    return f'`-x = {-x}` 不在哈希表里：左边没有 {x} 的相反数'


CONFIG = dict(
    num=2441, title='与对应负数同时存在的最大正整数', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左 · 哈希集合',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1168'],
    code='''
class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        ans = -1
        s = set()
        for x in nums:
            if -x in s:
                ans = max(ans, abs(x))
            s.add(x)
        return ans
''',
    call=f'Solution().findMaxK({NUMS})',
    expect=7,
    views=[
        dict(type='text', h=80, size=28,
             fn=lambda S: (f"右边当前 `x = {S['x']}`，去左边（哈希表）里找 `{-S['x']}`" if 'x' in S
                           else '一边遍历，一边在==左边出现过的数==里找相反数')),
        dict(type='array', var='nums', label='nums（黄 = 当前 x，青 = 已放入哈希表）', cell=110, h=220, color=_col),
        dict(type='set', var='s', label='s：已遍历过的数', fmt=lambda x: str(x), h=180),
    ],
    watch=['x', ('ans', 'ans', 'green')],
    captions={
        'ans = -1': '`ans = -1`：找不到时直接返回 -1',
        's = set()': '哈希集合 `s` 记录==左边出现过的数==',
        'for x in nums': lambda S, B, r: ('nums 遍历完了' if 'x' in B and B.x == S.x else f'枚举右：`x = {S.x}`'),
        'if -x in s': _if,
        'ans = max': '用 `|x| = {abs(x)}` 更新答案：`ans = max({B.ans}, {abs(x)}) = {ans}`',
        's.add(x)': '把 `{x}` 加入哈希表，供右边的数查询',
        'return ans': '最大的 k 是 =={ans}==',
    },
    cards=dict(
        one_liner='枚举右，维护左：边遍历边查相反数是否出现过',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `nums` 不含 0，找最大的正整数 `k`，使 `k` 和 `-k` 都在数组中',
                 '不存在返回 `-1`',
                 '示例：`[-1,10,6,7,-7,1]` → `7`（1 和 7 都有相反数，7 更大）'],
        quote='用一个哈希表记录出现过的数字。一边遍历，一边看 `-nums[i]` 是否在哈希表中，如果在，就更新答案的最大值为 `|nums[i]|`。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一对 `±k` 里，==后出现的那个==负责找先出现的那个',
              '所以只需查左边：`-x in s`，查到就用 `abs(x)` 更新答案',
              '先查询再 `s.add(x)`，一次遍历搞定'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '后出现的可能是负数，所以更新答案要用 `abs(x)`，不能用 `x`',
                 '和「两数之和」同一个套路：枚举右，维护左'],
    ),
)
