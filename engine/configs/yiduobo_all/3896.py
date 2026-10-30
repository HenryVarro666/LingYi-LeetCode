NUMS = [1, 2, 3, 4]


def _isp(v):
    if v < 2:
        return False
    return all(v % d for d in range(2, int(v ** 0.5) + 1))


def _line(S):
    return list(range(0, 11))


def _color(S, i, v):
    return 'green' if _isp(v) else None


def _txt(S):
    if 'v' not in S or 'index' not in S:
        return '边走边检测：用字典 `p` 缓存每个数是不是质数'
    i, v = S['index'], S['v']
    need = '质数' if i % 2 == 0 else '非质数'
    return f'下标 `{i}` 要 =={need}==；当前 `v = {v}`，`flag = {S.get("flag")}`；已操作 `res = {S["res"]}` 次'


CONFIG = dict(
    num=3896, title='将数组转换为交替质数数组的最少操作次数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='一趟遍历 · 试除法检测质数',
    tags=['灵神题单·数学算法', '难度分 1435'],
    code='''
class Solution(object):
    def minOperations(self, nums):
        
        def check(v, p):
            if v not in p:
                if v == 1:
                    p[v] = False
                else:
                    x = 2
                    p[v] = True
                    while x * x <= v:
                        if v % x == 0:
                            p[v] = False
                            break
                        x += 1
            
            return p[v]

        p = {}
        res = 0
        for index, v in enumerate(nums):
            flag = check(v, p)
            if index % 2 == 0:
                while not flag:
                    res += 1
                    v += 1
                    flag = check(v, p)
            else:
                while flag:
                    res += 1
                    v += 1
                    flag = check(v, p)
        
        return res
''',
    call=f'Solution().minOperations({NUMS})',
    expect=3,
    max_steps=110,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=230, label='nums（蓝箭头 = 当前下标）'),
        dict(type='array', var=_line, pointers={'v': 'pink'}, color=_color, h=190, label='数轴 0..10（绿 = 质数，粉箭头 = 当前的 v）'),
        dict(type='map', var='p', h=150, fmt=lambda k, v: f'{k}: {"质数" if v else "非质数"}'),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'pink'), 'flag', ('res', 'res', 'green')],
    captions={
        'if v not in p': '`{v}` 还没检测过吗？没有就检测并缓存',
        'if v == 1': lambda S, B, r: ('`v == 1`：成立，`1` 不是质数' if S.v == 1 else f'`v = {S.v}`，不是 1：走试除'),
        7: '`1` 不是质数，缓存 False',
        'p[v] = True': '先假设 `{v}` 是质数：`p[{v}] = True`，再试除找因子',
        'x = 2': '从 `x = 2` 开始试除',
        'while x * x <= v': '只需试到 `x * x <= v`：`{x}×{x}` 与 `{v}` 比较',
        'if v % x == 0': '`{v} % {x} = {v % x}`：整除就说明有因子，是合数',
        13: '`{v}` 有因子 `{x}` → 非质数，缓存 False 并停止',
        'x += 1': '没整除，试下一个 `x = {x}`',
        'return p[v]': '`{v}` 是质数吗？`{ret}`',
        'flag = check': '`flag = {flag}`：`{v}` 是质数吗',
        'if index % 2 == 0': lambda S, B, r: (f'`index = {S.index}` 是偶数下标 → 需要质数' if S.index % 2 == 0
                                              else f'`index = {S.index}` 是奇数下标 → 需要非质数'),
        'while not flag': lambda S, B, r: ('`flag` 为假：还不是质数，要加 1' if not S.flag else '`flag` 为真：已经是质数，满足'),
        'while flag': lambda S, B, r: ('`flag` 为真：还是质数，要加 1' if S.flag else '`flag` 为假：已经是非质数，满足'),
        'res += 1': '加 1 花一次操作：`res` → {res}',
        'v += 1': '`v` 变成 {v}，重新检测',
        'return res': '检查完所有位置，最少 `{res}` 次',
    },
    cards=dict(
        one_liner='一趟遍历，不满足就不断加 1，直到满足',
        complexity='时间约 `O(n·G·√v)`，空间 `O(n)`',
        problem=['偶数下标要 ==质数==，奇数下标要 ==非质数==；一次操作可让任意元素加 1',
                 '求最少操作次数',
                 '示例：`[1,2,3,4]` → `3`'],
        quote='因为质数的分布不会太过离散，因此这里加1的次数不会太多。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个位置独立处理：不满足就 `v += 1` 再检测',
              '质数检测用试除，结果存进字典 `p`，同一个数不重复检测',
              '偶数位 `while not flag`，奇数位 `while flag`'],
        summary=['原文为 Python 2 风格，本题代码无需改动，直接运行',
                 '作者说也可以先筛出质数表，这里用的是试除 + 缓存',
                 '易错：`1` 不是质数，要单独判断',
                 '对比灵神：灵神预先用埃氏筛，yiduobo 边走边检测'],
    ),
)
