def _txt(S):
    if 'x' not in S:
        return '集合 `s` 同时装下原数和反转后的数，自动去重'
    if 'rev' in S and S['_line'] in (7, 8, 9, 10):
        return f"正在反转：剩余 `x = {S['x']}`，已拼出 `rev = {S['rev']}`"
    return ''


CONFIG = dict(
    num=2442, title='反转之后不同整数的数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合 · 数位反转',
    tags=[],
    code='''
class Solution:
    def countDistinctIntegers(self, nums: List[int]) -> int:
        s = set()
        for x in nums:
            s.add(x)
            rev = 0
            while x:
                rev = rev * 10 + x % 10
                x //= 10
            s.add(rev)
        return len(s)
''',
    call='Solution().countDistinctIntegers([1,13,10,12,31])',
    expect=6,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='array', var='nums', label='nums（绿 = 已经在集合里）', cell=90,
             color=lambda S, i, v: 'green' if v in S.get('s', ()) else None),
        dict(type='set', var='s', label='s（黄框 = 刚加入）', fmt=lambda x: str(x)),
    ],
    watch=['x', 'rev', ('len(s)', 'len(s)', 'green')],
    captions={
        's = set()': '用集合 `s` 存所有出现过的数，重复的自动去掉',
        'for x in nums': '取出原数组里的 `x = {x}`',
        's.add(x)': '先把原数 `{x}` 放进集合',
        'rev = 0': '`rev` 用来拼反转后的数，从 0 开始',
        'while x': lambda S, B, r: (f'`x = {S.x}` 还有数位没取完，继续' if S.x else '`x` 变成 0，数位取完了'),
        'rev = rev * 10': '取末位 `{B.x % 10}` 接到 `rev` 后面：`{B.rev} * 10 + {B.x % 10} = {rev}`',
        'x //= 10': '去掉 `x` 的末位，剩下 `{x}`',
        's.add(rev)': '反转后的 `{rev}` 也放进集合（如 10 反转成 01，就是 1）；集合现在有 `{len(s)}` 个数',
        'return len(s)': '集合大小就是不同整数的个数：`{ret}`',
    },
    cards=dict(
        one_liner='原数和反转数一起丢进集合，数集合大小',
        complexity='时间 `O(n log U)`，空间 `O(n)`',
        problem=['把 `nums` 每个数的数位反转，追加到数组末尾，求结果数组里不同整数的个数',
                 '反转 `10` 得到 `01`，即 `1`',
                 '示例：`[1,13,10,12,31]` → `6`'],
        quote='不用字符串 + 一次遍历：',
        quote_src='—— 灵茶山艾府题解（第二种写法）',
        idea=['不转字符串：用 `x % 10` 取末位、`rev * 10 + 末位` 拼出反转数',
              '一次遍历里同时把 `x` 和 `rev` 加进集合 `s`',
              '末尾 `len(s)` 即答案'],
        result='集合里是 `{1, 10, 12, 13, 21, 31}`，共 6 个 ✓',
        summary=['时间 `O(n log U)`，`U` 是最大值，每个数有 `log U` 位；空间 `O(n)`',
                 '易错：循环里 `x` 被改掉了，所以必须==先==把原数 `add` 进去',
                 '灵神还给了一行写法：`len(set(nums) | set(int(str(x)[::-1]) for x in nums))`，利用 C 层字符串反转，更快',
                 '末尾带 0 的数反转后前导零自然消失'],
    ),
)
