CONFIG = dict(
    num=2717, title='半有序排列', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='找 1 和 n 的位置分类讨论', tags=[],
    code='''
class Solution:
    def semiOrderedPermutation(self, nums: List[int]) -> int:
        n = len(nums)
        p = nums.index(1)
        q = nums.index(n)
        return p + n - 1 - q - (p > q)
''',
    call='Solution().semiOrderedPermutation([2,5,1,3,4])',
    expect=4,
    views=[
        dict(type='array', var='nums', pointers={'p': 'blue', 'q': 'pink'}, h=220,
             color=lambda S, i, v: 'blue' if v == 1 else 'pink' if v == S['n'] else None if 'n' in S else None),
        dict(type='text', h=110, fn=lambda S: (f"`1` 移到最左要 `p = {S['p']}` 步；`n` 移到最右要 `n-1-q = {S['n']-1-S['q']}` 步" if 'q' in S else '')),
    ],
    watch=[('n', 'n', 'yellow'), ('p', 'p', 'blue'), ('q', 'q', 'pink')],
    captions={
        'n = len': '排列长度 `n = {n}`，目标：开头是 `1`，结尾是 `{n}`',
        'p = nums.index(1)': '`1` 在下标 `p = {p}`，把它换到最左要 `{p}` 次相邻交换',
        'q = nums.index(n)': '`{n}` 在下标 `q = {q}`，把它换到最右要 `{n} - 1 - {q} = {n-1-q}` 次',
        'return': '`p + n - 1 - q = {p + n - 1 - q}`；`p > q` 是 {p > q}：{"1 在 n 右边，两者移动时会互相穿过，一次交换同时算了两边，要减 1" if p > q else "两者互不干扰，不用减"} → =={ret}==',
    },
    cards=dict(
        one_liner='1 往左挪、n 往右挪，两个数交错时少算一次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['排列第一个数是 `1`、最后一个数是 `n` 叫半有序',
                 '每次只能交换相邻两个元素，求最少操作次数',
                 '示例：`[2,4,1,3]` → `3`'],
        quote='如果 p>q，那么 1 和 n 在移动过程中会相遇，互相穿过对方，也就是只花费一次操作，就让两个数都移动了一步（互相穿过），所以操作次数比上面的情况要少 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设 `1` 的下标为 `p`，`n` 的下标为 `q`',
              '`p < q`：互不干扰，共 `p + (n-1-q)` 次',
              '`p > q`：途中相遇交换一次，共 `p + (n-1-q) - 1` 次'],
        after=[dict(heading='再看 p < q 的情形', lines=['`[2,1,4,3]`：`p = 1`，`q = 2`，1 在 n 左边', '1 左移 1 步，n（即 4）右移 1 步，互不相遇', '答案 `1 + (4-1-2) = 2`，不用减 1', '所以只有 `p > q` 才需要减 1'])],
        summary=['时间 `O(n)`，`index` 查找各扫一遍',
                 '==`(p > q)` 是布尔值，直接当 0/1 减掉==',
                 '易错：右移距离是 `n-1-q`，别漏掉 `-1`',
                 '只关心 1 和 n 的位置，其他数怎么排都不影响'],
    ),
)
