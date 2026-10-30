CONFIG = dict(
    num=1981, title='最小化目标值与所选元素的差', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='按行递推的可达和集合',
    tags=['灵神题单', '动态规划', '难度分 2010'],
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
    call='Solution().minimizeTheDifference([[1,2,3],[4,5,6],[7,8,9]], 13)',
    expect=0,
    views=[
        dict(type='grid', var='mat', h=190, cell=70),
        dict(type='set', var='f', label='f：能凑出的所有和', h=230),
        dict(type='text', fn=lambda S: f"目标 `target = {S['target']}`" + (f"；当前最接近：`res = {S['res']}`" if S.get('res') is not None else ''), size=26, h=60),
    ],
    watch=['i', 'num', 'j', 'target', ('res', 'res', 'green')],
    captions={
        6: '`f` 是集合：记录==前面几行各选一个==后，能凑出的所有和',
        'f.add(num)': '第 0 行：每个数本身就是一个可能的和，`f = {f}`',
        'g = f.copy()': '先把上一行的和存进 `g`：这一行要用旧集合，新集合 `f` 重新开始',
        12: '`f` 清空，准备装“前 {i+1} 行”的和',
        'f.add(j + num)': '上一行的和 `{j}` 加这一行的 `{num}` = `{j + num}`，放进 `f`',
        'if res is None': '`{num}` 离目标 `{target}` 的距离是 `{abs(num - target)}`；比当前最小 `{B.res}` 更小就更新',
        'res = abs': '更新答案：`res = {res}`',
        'return res': '最小绝对差 ==`{res}`==',
    },
    skip=['for num in mat[i]', 'for j in g'],
    cards=dict(
        one_liner='每行选一个数，能凑出哪些和？最后挑离 target 最近的',
        complexity='时间约 `O(m·S·n)`，`S` 为和的取值数；空间 `O(S)`',
        problem=['矩阵 `mat` 每一行必须选一个整数', '让所选元素之和与 `target` 的绝对差最小，求这个最小差',
                 '示例：`[[1,2,3],[4,5,6],[7,8,9]], target=13` → `0`'],
        quote='令f[i]表示前i行中，以第i行的数字结尾时能选出的数字和的集合，那么此时为了得到f[i]，就需要将f[i - 1]中的数字和与第i行的说有数进行组合，并将和加入到f[i]中。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想二维布尔 DP：`f[i][j]` 表示前 `i` 行能否凑出和 `j`', '作者换成集合写法：直接存==能凑出的和==，只保留上一行',
              '最后枚举集合里每个和，取离 `target` 最近的'],
        summary=['时间 `O(m·n·S)`，`S` 为不同和的个数，空间 `O(S)`',
                 '易错：新一行必须用旧集合 `g` 生成，不能边遍历边改 `f`',
                 '`res` 初值是 `None`，第一次直接赋值',
                 '原文就是 Python 3 可运行的写法，未做修改；集合没有剪枝（和超过 `target` 太多可以丢掉）'],
    ),
)
