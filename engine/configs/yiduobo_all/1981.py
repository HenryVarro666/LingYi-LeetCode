CONFIG = dict(
    num=1981, title='最小化目标值与所选元素的差', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='每行可达和的集合递推',
    tags=['动态规划', '难度分 2010'],
    code='''
class Solution(object):
    def minimizeTheDifference(self, mat, target):

        m = len(mat)

        f = set()
        for num in mat[0]:
            f.add(num)

        for i in range(1, m):
            g = f.copy()
            f = set()
            for num in mat[i]:
                for j in g:
                    f.add(j + num)

        res = None
        for num in f:
            if res is None or res > abs(num - target):
                res = abs(num - target)
        
        return res
''',
    call='Solution().minimizeTheDifference([[1,2],[3,4],[5,6]], 10)',
    expect=0,
    skip=['m = len', 'f = set()', 'g = f.copy()', 'for num in mat[0]', 'for num in mat[i]', 'for j in g'],
    max_steps=60,
    views=[
        dict(type='table', var='mat', label='mat：每行选一个', h=190, cell=62, cursors=[]),
        dict(type='set', var='f', label='f：前几行能选出的所有和（新加入的黄色）', h=260, fmt=lambda x: str(x)),
        dict(type='text', fn=lambda S: (f"目标 `target = {S['target']}`；当前最接近的差 `res = {S['res']}`" if S.get('res') is not None else f"目标 `target = {S['target']}`"), size=24, h=50),
    ],
    watch=['i', 'num', 'j', ('target', 'target', 'pink'), ('res', 'res', 'green')],
    captions={
        'f.add(num)': '第 0 行：每个数本身就是一种和，`f` = {sorted(f)}',
        'for i in range': lambda S, B, r: (f'第 `{S.i}` 行：把上一行的和集合 `f` 和这一行每个数两两相加' if S.i != B.get('i') else '所有行都处理完，`f` 是全部可能的和'),
        'f.add(j + num)': '`{j} + {num}` = =={j + num}== 加入 `f`（上一行的和 + 本行的数）',
        'res = None': '准备在 `f` 里找离 `target` 最近的和',
        'res = abs(num - target)': '更新 `res` = =={res}==',
        'return res': '最小绝对差 = =={ret}==',
    },
    cards=dict(
        one_liner='每行都把“已有的和”与“本行的数”两两相加',
        complexity='和的个数最多 `O(m·max)`，总共约 `O(m·n·sum)`',
        problem=['矩阵每行选一个数，使总和与 `target` 的绝对差最小',
                 '`m,n ≤ 70`，数值 `≤ 70`',
                 '示例：`[[1,2],[3,4],[5,6]]`，`target=10` → `0`'],
        quote='令f[i]表示前i行中，以第i行的数字结尾时能选出的数字和的集合，那么此时为了得到f[i]，就需要将f[i - 1]中的数字和与第i行的说有数进行组合，并将和加入到f[i]中。',
        quote_src='—— yiduobo 题解原文',
        idea=['原文先写 `f[i][j]` 表示“能否选出和为 j”',
              '这里换成集合写法：`f[i]` = 前 `i` 行能选出的所有和',
              '最后遍历 `f`，找离 `target` 最近的那个和'],
        summary=['和最大 `70·70 = 4900`，集合大小有上限，所以不会爆',
                 '易错：每行都要先 `g = f.copy()` 再清空 `f`，否则本行的和会叠加到本行自己',
                 '没做 `target × 2` 的剪枝，靠集合去重控制规模',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神用布尔数组 + `target×2` 封顶；这里用集合保存所有可达的和'],
    ),
)
