CONFIG = dict(
    num=349, title='两个数组的交集', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合 · 一次遍历',
    code='''
class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        st = set(nums1)
        ans = []
        for x in nums2:
            if x in st:
                st.remove(x)
                ans.append(x)
        return ans
''',
    call='Solution().intersection([4,9,5,9], [9,4,9,8,4])',
    expect=[9, 4],
    views=[
        dict(type='array', var='nums2', label='nums2（逐个枚举 x）', h=150),
        dict(type='set', var='st', label='st = set(nums1)（还没被答案“取走”的数）', fmt=lambda x: str(x), h=170),
        dict(type='array', var='ans', label='ans（交集，每个数只出现一次）', h=150),
    ],
    watch=[('x', 'x', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'st = set(nums1)': '把 `nums1` 放进哈希集合：以后判断“在不在 nums1 里”只要 `O(1)` → `st = {st}`',
        'ans = []': '`ans` 存交集',
        'for x in nums2': '只遍历 `nums2`：取出 `x = {x}`',
        'if x in st': lambda S, B, r: (f'`{S.x}` 在 `st` 里 → 它同时在两个数组中' if S.x in S.st else f'`{S.x}` 不在 `st` 里 → 要么不在 nums1，要么已经加进过答案，跳过'),
        'st.remove(x)': '把 `{B.x}` 从 `st` 删掉：==后面再遇到相同的数就不会重复加入答案==',
        'ans.append(x)': '`{x}` 加入答案 → `ans = {ans}`',
        'return ans': '`nums2` 扫完，答案 `{ret}`',
    },
    cards=dict(
        one_liner='集合装 nums1，命中就取走，天然去重',
        complexity='时间 `O(n+m)`，空间 `O(n)`',
        problem=['返回两个数组的交集，结果中每个元素==唯一==，顺序随意',
                 '示例：`nums1=[4,9,5]`，`nums2=[9,4,9,8,4]` → `[9,4]`',
                 '本视频：`[4,9,5,9]` 与 `[9,4,9,8,4]`'],
        quote='在 nums2[i] 加入答案列表的同时，把 nums2[i] 从哈希集合 st 中去掉，这样后面遍历到相同的元素时，由于其不在 st 中，所以不会加入答案列表。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums1` 变成集合 `st`，判断是否在 `nums1` 中是 `O(1)`',
              '命中后立刻 `st.remove(x)`：既保证去重，又不用再扫一遍答案',
              '`nums1`、`nums2` 各只遍历一次，所以叫“一次遍历”'],
        summary=['时间 `O(n+m)`，空间 `O(n)`；把短数组转集合可降到 `O(min(n,m))`',
                 '易错：不删除就会把 `9` 重复加入答案',
                 '另一种写法 `list(set(nums1) & set(nums2))` 更短，但不是一次遍历'],
    ),
)
