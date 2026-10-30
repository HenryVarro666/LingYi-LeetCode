_cnt = {}


def _forcap(key, n, what):
    def f(S, B, r):
        c = _cnt.get(key, 0) + 1
        _cnt[key] = c
        if c > n:
            return f'{what}都处理完了，退出这个循环'
        return f'{what}：`index = {c - 1}`'
    return f


def _color(S, i, v):
    if 'odd' not in S or 'even' not in S:
        return None
    odd, even = S['odd'], S['even']
    if i < odd:
        return 'green'
    if i >= odd + 1 and i < odd + even * 2 and (i - odd) % 2 == 1:
        return 'blue'
    return None


CONFIG = dict(
    num=3457, title='吃披萨', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='降序排序 + 分奇偶天累加',
    tags=['灵神题单', '难度分 1704'],
    code='''
class Solution(object):
    def maxWeight(self, pizzas):
        
        pizzas.sort(reverse=True)
        n = len(pizzas)
        n //= 4
        even = n // 2
        odd = n - even

        res = 0
        for index in range(odd):
            res += pizzas[index]
        for index in range(even):
            res += pizzas[odd + index * 2 + 1]
        
        return res
''',
    call='Solution().maxWeight([4,1,8,3,6,2,7,5,9,1,3,2])',
    expect=23,
    views=[
        dict(type='array', var='pizzas', h=230, cell=68, label='pizzas（降序）', color=_color,
             dim=lambda S, i, v: 'odd' in S and 'even' in S and _color(S, i, v) is None),
        dict(type='text', h=130, fn=lambda S: ('奇数天 ==%d== 天吃最重的（绿），偶数天 ==%d== 天各取次重的（蓝）' % (S['odd'], S['even'])) if 'odd' in S else ''),
    ],
    watch=['n', 'even', 'odd', ('res', 'res', 'green')],
    captions={
        'pizzas.sort': '从大到小排序：`{pizzas}`',
        'n = len': '披萨总数 `n = {n}`',
        'n //= 4': '每天吃 4 个，一共 `n = {n}` 天',
        'even = n // 2': '偶数天 `even = {even}` 天',
        'odd = n - even': '奇数天 `odd = {odd}` 天：奇数天吃最重的 + 最轻的三个，==最重的 odd 个披萨都在奇数天吃==',
        'res = 0': '`res` 累计增加的体重',
        'for index in range(odd)': _forcap('a', 2, '奇数天'),
        'for index in range(even)': _forcap('b', 1, '偶数天'),
        'res += pizzas[index]': '奇数天吃第 `{index}` 重的披萨 `{pizzas[index]}`，`res` → {res}',
        'res += pizzas[odd': '偶数天：这一天最重的被浪费，保住次重的 `pizzas[{odd + index * 2 + 1}] = {pizzas[odd + index * 2 + 1]}`，`res` → {res}',
        'return res': '总增重 =={res}==',
    },
    skip=[],
    max_steps=40,
    cards=dict(
        one_liner='奇数天吃最重的，偶数天吃次重的：先排序，再按位置累加',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每天吃 4 个披萨：奇数天增重==最大==的，偶数天增重==第二大==的',
                 '求吃完所有披萨后增重的最大值',
                 '本视频：`[4,1,8,3,6,2,7,5,9,1,3,2]` → `23`'],
        quote='每天吃掉的4个披萨中只有一个的重量会被累加到答案中，因此对于白吃的另外三个披萨，就应该让这些披萨的重量尽可能的小。',
        quote_src='—— yiduobo 题解原文',
        idea=['奇数天：吃最重的 + 最轻的三个，白吃的尽量轻',
              '偶数天：最重的被浪费，但要保住次重的；奇数天更赚，故奇数天先拿最重的 `odd` 个',
              '偶数天从剩下的里每次取最重两个：增重是第 `odd+2`、`odd+4`… 重的（下标 `odd + 2*i + 1`）'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '`n //= 4` 之后 `n` 是天数；`even = n // 2`，`odd = n - even`',
                 '偶数天取 `pizzas[odd + index * 2 + 1]`，注意 `+ 1`',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改',
                 '对比灵神：灵神一行切片求和；yiduobo 用两个循环，并用交换法证明奇数天更优'],
    ),
)
