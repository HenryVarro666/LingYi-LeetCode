CONFIG = dict(
    num=899, title='有序队列', difficulty='Hard', category='字符串',
    author='yiduobo', technique='K=1 枚举旋转，K>=2 直接排序',
    tags=['字符串排序'],
    code='''
class Solution(object):
    def orderlyQueue(self, S, K):

        if K >= 2:
            return ''.join(sorted(list(S)))
        
        n = len(S)
        S += S
        res_pos = 0
        for index in range(1, n):
            if S[res_pos:res_pos + n] > S[index:index + n]:
                res_pos = index
        
        return S[res_pos:res_pos + n]
''',
    call='Solution().orderlyQueue("baacb", 1)',
    expect='aacbb',
    views=[
        dict(type='string', var='S', h=230,
             window=('res_pos', 'res_pos+n-1'),
             pointers={'res_pos': 'green', 'index': 'blue'}),
        dict(type='text', fn=lambda S: (f"当前最优旋转 `{S['S'][S['res_pos']:S['res_pos']+S['n']]}`，候选 `{S['S'][S['index']:S['index']+S['n']]}`" if 'index' in S else (f"当前最优旋转 `{S['S'][S['res_pos']:S['res_pos']+S['n']]}`" if 'res_pos' in S else ''))),
    ],
    watch=['K', 'n', ('res_pos', 'res_pos', 'green'), ('index', 'index', 'blue')],
    captions={
        'if K >= 2': lambda S, B, r: '`K = %d`：只能取前 1 个放到末尾，== 只能旋转 ==，下面枚举所有旋转' % S.K if S.K < 2 else '`K = %d >= 2`：能交换任意两个字符，答案就是排序' % S.K,
        'n = len(S)': '`n = {n}`，一共 `n` 种旋转',
        'S += S': '`S` 拼两遍 → `{S}`：任意长为 `n` 的窗口就是一个旋转',
        'res_pos = 0': '`res_pos` 记录目前字典序最小旋转的起点，先设为 0',
        'if S[res_pos': lambda S, B, r: '`%s` vs `%s`：当前最优%s' % (S.S[S.res_pos:S.res_pos+S.n], S.S[S.index:S.index+S.n], '更大 → 换成新的' if S.S[S.res_pos:S.res_pos+S.n] > S.S[S.index:S.index+S.n] else '不更大 → 保留'),
        'res_pos = index': '更小的旋转起点是 `{index}` → `res_pos = {res_pos}`',
        'return S[res_pos': '最小旋转是 `{S[res_pos:res_pos + n]}`',
    },
    cards=dict(
        one_liner='K=1 只能旋转；K>=2 能交换任意两字符，直接排序',
        complexity='K=1：时间 `O(n^2)`；K>=2：`O(n log n)`',
        problem=['字符串 `S`，每步取前 `K` 个字符之一放到末尾，求能得到的字典序最小字符串',
                 '示例：`"baacb"`, `K=1` → `"aacbb"`',
                 '本视频演示 `K = 1`；`K >= 2` 一行排序'],
        quote='当k >= 2时，……我们就有了交换S中任意两个字符的能力，因此当k>=2时，答案就是将S中的字符按字典序排序后输出。',
        quote_src='—— yiduobo 题解原文',
        idea=['`K=1`：每次只能把首字符挪到末尾，等于旋转，枚举 `n` 种取最小',
              '`S += S` 后，每个旋转都是长为 `n` 的切片',
              '`K>=2`：作者用 4 步操作证明能交换任意 `p`、`q` 位置的字符'],
        summary=['`K=1` 枚举旋转，切片比较，`O(n^2)`',
                 '`K>=2` 排序即可，`O(n log n)`',
                 '易错：`K=1` 时不能排序；`S += S` 后下标范围只到 `n-1`'],
    ),
)
