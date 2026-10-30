def _txt(S):
    if 'res' in S and 'index' in S:
        return f"`res = res × {S['index']} % mod`，目前 ==res = {S['res']}==（累乘 1..{S['index']}）"
    if 'v' in S:
        return f"检查 `v = {S['v']}`，对比 `complexity[0] = {S['complexity'][0]}`"
    return '建树的视角：0 号是根，值必须是整棵树里最小的'


CONFIG = dict(
    num=3577, title='统计计算机解锁顺序排列数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='建树观察 · (n-1)!',
    tags=['灵神题单', '贪心与思维', '难度分 1750'],
    code='''
class Solution(object):
    def countPermutations(self, complexity):
        
        for v in complexity[1:]:
            if v <= complexity[0]:
                return 0
        
        res = 1
        mod = 10 ** 9 + 7
        for index in range(1, len(complexity)):
            res = res * index % mod
        return res
''',
    call='Solution().countPermutations([2,3,5,4,6])',
    expect=24,
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='array', var='complexity', h=260, label='complexity',
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'orange' if i == 0 else (
                 'blue' if 'index' in S and i == S['index'] else
                 ('blue' if 'v' in S and 'index' not in S and i > 0 and S['complexity'][i] == S['v'] else
                  ('green' if 'index' in S and 0 < i < S['index'] else None)))),
    ],
    watch=['v', 'index', ('res', 'res', 'green')],
    captions={
        'for v in': '遍历 0 号右边的每台电脑 `v`',
        'if v <= complexity[0]': '`v = {v}` {"<=" if v <= complexity[0] else ">"} `complexity[0] = {complexity[0]}`：{"0 号不是最小，解锁不了 → 返回 0" if v <= complexity[0] else "比 0 号大，0 号能直接解锁 → 继续"}',
        'return 0': '有一台电脑的复杂度不超过 0 号，无法解锁，答案 ==0==',
        'res = 1': '全都比 0 号大：都能由 0 号直接解锁，开始累乘排列数',
        'mod =': '结果要取模 `10^9+7`',
        'res = res * index': '`res = res × {index} % mod = {res}`：再放入一台电脑，多 {index} 种插法',
        'return res': '其余 `n-1` 台可任意顺序解锁，排列数 ==(n-1)! = {res}==',
    },
    cards=dict(
        one_liner='把解锁关系连成树，0 号是最小的根，其余任意排',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['0 号电脑已解锁，用编号更小且复杂度更小的电脑去解锁别的电脑',
                 '问有多少种 `0..n-1` 的排列是合法的解锁顺序，对 `10^9+7` 取模',
                 '本视频：`[2,3,5,4,6]` → `24`'],
        quote='将所有计算机和其解锁时依赖的计算机之间连上一条边的话，就可以得到一颗树，这棵树的每个节点值都大于其根节点的值，而整棵树的根节点为0号节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['依赖关系连边得到一棵根为 0 号的树，孩子的复杂度都比父亲大',
              '所以 0 号是全树最小的，==能直接解锁所有==；解不了的别人也解不了',
              '一趟遍历：有 `v <= complexity[0]` 答案为 0，否则是 `(n-1)!`'],
        summary=['时间 `O(n)`，空间 `O(1)`（切片 `complexity[1:]` 会多占 `O(n)`）',
                 '先扫一遍判 0，再循环累乘 `1..n-1`，每步取模',
                 '`<=` 不能写成 `<`：复杂度相等也无法解锁',
                 '原文为 Python 2 风格，代码未做改动',
                 '对比灵神：灵神把判断和累乘合在一个循环里，这里分成两步'],
    ),
)
