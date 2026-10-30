CONFIG = dict(
    num=779, title='第K个语法符号', difficulty='Medium', category='位运算',
    author='yiduobo', technique='统计 K-1 中 1 的个数奇偶',
    code='''
class Solution(object):
    def kthGrammar(self, N, K):

        cnt = 0
        K -= 1
        while K:
            K &= K - 1
            cnt += 1
        
        return cnt % 2
''',
    call='Solution().kthGrammar(4, 5)',
    expect=1,
    setup='',
    views=[
        dict(type='text', fn=lambda S: '第 4 行 = `01101001`，要找的下标 = K-1 = `4`', size=34),
        dict(type='text', fn=lambda S: (f"`K` 二进制 = ==`{S['K']:b}`==，已剥掉 `{S['cnt']}` 个 1" if S.get('K', 0) > 0 else f"`K` = 0，共剥掉 ==`{S['cnt']}`== 个 1") if 'cnt' in S and 'K' in S else '', size=34),
        dict(type='string', var=lambda S: '01101001', label='第 4 行（下标 0 起），目标 = 下标 4', h=200,
             color=lambda S, i, v: 'yellow' if i == 4 else None),
    ],
    watch=['N', 'K', ('cnt', 'cnt', 'green')],
    captions={
        'cnt = 0': '`cnt` 记录剥离了几个最低位的 1',
        'K -= 1': '改成从 0 计数：`K` = {K}，二进制 `{K:b}`',
        'while K': lambda S, B, r: (f'`K = {S.K}` 还不为 0，继续剥' if S.K else '`K` 已经是 0，剥完了'),
        'K &= K - 1': '`K & (K-1)` 去掉最低位的 1：`{B.K:b}` → `{K:b}`（每剥一次，结果取反一次）',
        'cnt += 1': '`cnt` → {cnt}',
        'return cnt % 2': '剥了 `{cnt}` 次，奇数次取反 → 答案 `{ret}`',
    },
    cards=dict(
        one_liner='每行是上一行加上它的取反，K-1 里 1 的个数奇偶就是答案',
        complexity='时间 `O(log K)`，空间 `O(1)`',
        problem=['第 1 行是 `0`，之后每行把上一行的 `0→01`、`1→10`',
                 '求第 `N` 行第 `K` 个字符',
                 '示例：`N=4, K=5` → 第 4 行 `01101001` 的第 5 个字符 `1`'],
        quote='每一行的字符串就是将上一行复制一遍，然后逐位取反一遍再拼接在一起',
        quote_src='—— yiduobo 题解原文',
        idea=['`K` 从 0 计数：后半段第 `k` 位 = 前半段第 `k - 2^(p-1)` 位取反',
              '减去 `2^(p-1)` 就是剥掉 `K` 最高位的 1，每剥一次翻转一次',
              '剥哪一位都一样，用 `K &= K - 1` 逐个剥最低位的 1，数奇偶即可'],
        summary=['时间 `O(log K)`，空间 `O(1)`',
                 '先 `K -= 1`，让下标从 0 起，否则奇偶会错',
                 '答案其实就是 `K-1` 的二进制 1 的个数 mod 2（Thue-Morse 序列）',
                 '原文为 Python 2 风格，代码无需改动，`N` 在代码里未使用'],
    ),
)
