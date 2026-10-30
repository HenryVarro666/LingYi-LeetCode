def _top(S):
    if 'res' not in S:
        return ''
    n = S['rowIndex']
    line = S.get('_line')
    if 'index' in S and line == 6:
        i = S['index']
        return f'`C({n}, {i}) = C({n}, {i-1}) × ({n} − {i} + 1) ÷ {i}` = =={S["res"][-1]}=='
    return f'第 `{n}` 行 = `C({n},0), C({n},1), …, C({n},{n})`，只算前一半，后一半镜像'


CONFIG = dict(
    num=119, title='杨辉三角 II', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='组合数 + 左右对称',
    code='''
class Solution(object):
    def getRow(self, rowIndex):

        res = [1]
        mid = rowIndex // 2
        for index in range(1, mid + 1):
            res.append(res[-1] * (rowIndex - index + 1) // index)
        
        res.extend([res[index] for index in range((rowIndex - 1) // 2, -1, -1)])
        return res
''',
    call='Solution().getRow(5)',
    expect=[1, 5, 10, 10, 5, 1],
    views=[
        dict(type='text', fn=_top, size=26, h=60),
        dict(type='array', var='res', label='res', cell=90, h=240),
    ],
    watch=['rowIndex', 'mid', 'index', ('res', 'res', 'green')],
    captions={
        'res = [1]': '第 `k` 行第 0 个数是 `C(k,0) = 1`',
        'mid = ': '`C(m,n) = C(m,m-n)`：行是对称的，只算前一半，`mid = {mid}`',
        6: lambda S, B, ret: (f'算第 `{S.index}` 个数' if len(S.res) <= S.mid else f'前 `{S.mid + 1}` 个数（下标 0 到 {S.mid}）算完了'),
        'res.append': '`C(n,i) = C(n,i-1) × (n−i+1) ÷ i`：`{res[-2]} × {rowIndex - index + 1} ÷ {index}` = =={res[-1]}==（整除，先乘后除）',
        'res.extend': '后一半是前一半的镜像：从下标 `{(rowIndex - 1) // 2}` 倒着复制到 `0`，补全成 `{res}`',
        'return res': '第 `{rowIndex}` 行 = =={ret}==',
    },
    cards=dict(
        one_liner='杨辉三角第 k 行就是组合数 C(k,0)…C(k,k)',
        complexity='时间 `O(k)`，空间 `O(1)`（不计结果）',
        problem=['给定 `rowIndex`，返回杨辉三角第 `rowIndex` 行（从 0 开始）',
                 '示例：`rowIndex = 3` → `[1,3,3,1]`',
                 '本视频：`rowIndex = 5` → `[1,5,10,10,5,1]`'],
        quote='杨辉三角本质上就是二项式定理，即(x + 1)^k展开之后，x按次数排列之后的系数，第k行分别为C(k, 0), C(k, 1)...，C(k, k)。',
        quote_src='—— yiduobo 题解原文',
        idea=['不用逐行递推：直接按公式 `C(k,i) = C(k,i-1) × (k-i+1) / i` 一个个算',
              '`C(m,n)` 与 `C(m,m-n)` 相等，只算前半行，==反过来复制==后半行'],
        summary=['时间 `O(k)`，额外空间 `O(1)`，比逐行递推的 `O(k^2)` 时间更省',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '易错点：必须==先乘后除==，这样每一步都能整除',
                 '镜像起点是 `(rowIndex-1)//2`：奇偶行中间那个数不能重复复制',
                 '对比灵神：灵神预处理整个三角形，查询 `O(1)`；这里直接按公式算一行'],
    ),
)
