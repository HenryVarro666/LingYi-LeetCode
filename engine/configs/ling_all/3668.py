CONFIG = dict(
    num=3668, title='重排完成顺序', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合 + 列表推导式过滤',
    tags=[],
    code='''
class Solution:
    def recoverOrder(self, order: List[int], friends: List[int]) -> List[int]:
        st = set(friends)
        return [x for x in order if x in st]
''',
    call='Solution().recoverOrder([3, 1, 2, 5, 4, 7, 6], [1, 3, 4, 6])',
    expect=[3, 1, 4, 6],
    views=[
        dict(type='array', var='order', label='order（完成顺序，黄 = 正在看的人）', cell=90, h=170,
             color=lambda S, i, v: ('yellow' if S.get('x') == v else ('green' if v in S['st'] and 'x' in S else None)) if 'st' in S else None),
        dict(type='set', var='st', label='st（朋友集合）', fmt=lambda x: str(x), h=150, font=34),
        dict(type='text', h=90, size=32,
             fn=lambda S: f"已加入答案的朋友：==[{', '.join(str(v) for v in S['order'][:S['order'].index(S['x'])+1] if v in S['st'])}]==" if 'x' in S else ''),
    ],
    watch=[('friends', 'friends'), ('st', 'sorted(st) if "st" in S else ""', 'green')],
    captions={
        'st = set': '把 `friends` 转成集合，之后判断「是不是朋友」只要 `O(1)`：`st = {st}`',
        'return [x for x in order if x in st]': lambda S, B, r: (
            f'按 `order` 的完成顺序逐个看，`x = {S.x}`：' + ('在 `st` 中，==是朋友，收进答案==' if S.x in S.st else '不在 `st` 中，跳过')
            if 'x' in S and r is None else
            f'遍历结束，朋友们按完成顺序排好：==`{r}`=='),
    },
    cards=dict(
        one_liner='不排序了：顺着 order 走一遍，是朋友就收下',
        complexity='时间 `O(n)`，空间 `O(m)`',
        problem=['`order` 是比赛完成顺序（1 到 n 各出现一次），`friends` 是朋友的 ID（递增）',
                 '返回朋友们按 ==完成顺序== 排列的 ID',
                 '示例：`order=[3,1,2,5,4]`，`friends=[1,3,4]` → `[3,1,4]`'],
        quote='对于 order 中的数字 x，如果 x 在 friends 中，那么把 x 添加到答案中。把 friends 转成哈希集合（或者布尔数组），这样我们可以快速判断一个数是否在 friends 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`order` 本身就是完成顺序，按它遍历，得到的结果天然有序',
              '只需判断每个 `x` 是不是朋友：用集合 `st` 查询是 `O(1)`',
              '一行列表推导式：`[x for x in order if x in st]`'],
        after=[dict(heading='写法二：布尔数组', lines=['`is_friend = [False] * (n + 1)`，下标就是选手 ID', '把 `friends` 里的 ID 位置标成 `True`', '再 `[x for x in order if is_friend[x]]`', '效果和集合一样，查询都是 `O(1)`'])],
        summary=['时间 `O(n)`，空间 `O(m)`，`m` 是 `friends` 的长度',
                 '不要直接 `x in friends`：列表查询是 `O(m)`（本题 m ≤ 8，也能过）',
                 '写法二：开布尔数组 `is_friend[n+1]`，下标就是 ID，查询同样 `O(1)`',
                 '`friends` 的递增顺序在这里没有用处'],
    ),
)
