def _bin(x):
    return format(x, 'b')


def _status(S):
    if 'now' not in S or 'p' not in S or 'index' not in S:
        return ''
    n = len(S['nums'])
    suf = S['suffix'][S['p'] + 1] if S['p'] + 1 < n else 0
    return (f"窗口 `[{S['index']}, {S['p']}]` 或值 now = ==`0b{_bin(S['now'])}`==　　"
            f"右侧后缀或 = `0b{_bin(suf)}`　→ " + ('右侧还有新的 1，要扩' if (S['now'] | suf) != S['now'] else '右侧没有新的 1，停'))


CONFIG = dict(
    num=2411, title='按位或最大的最小子数组长度', difficulty='Medium', category='位运算',
    author='yiduobo', technique='滑动窗口 · 后缀或 + 每位计数',
    tags=['灵神题单·位运算', '难度分 1938'],
    code='''
class Solution(object):
    def smallestSubarrays(self, nums):

        suffix = [nums[-1]]
        n = len(nums)
        for index in range(n - 2, -1, -1):
            suffix.append(suffix[-1] | nums[index])
        suffix.reverse()

        res = []
        cnt = [0] * 31
        p = -1
        now = 0

        for index in range(n):
            if p < index:
                p = index
                now = nums[index]
                tmp = now
                pos = 0
                while tmp:
                    if tmp % 2 == 1:
                        cnt[pos] += 1
                    tmp //= 2
                    pos += 1
            
            while p + 1 < n and (now | suffix[p + 1]) != now:
                p += 1
                now |= nums[p]
                tmp = nums[p]
                pos = 0
                while tmp:
                    if tmp % 2 == 1:
                        cnt[pos] += 1
                    tmp //= 2
                    pos += 1
            
            res.append(p - index + 1)
            remove = 0
            tmp = nums[index]
            pos = 0
            while tmp:
                if tmp % 2 == 1:
                    cnt[pos] -= 1
                    if cnt[pos] == 0:
                        remove |= (1 << pos)
                tmp //= 2
                pos += 1
            
            now ^= remove
        
        return res
''',
    call='Solution().smallestSubarrays([1,0,2,1,3])',
    expect=[3, 3, 2, 2, 1],
    skip=['tmp', 'pos', 'cnt[pos]', 'remove |='],
    views=[
        dict(type='text', fn=_status, h=60),
        dict(type='array', var='nums', label='nums（蓝框 = 当前窗口 [index, p]）', pointers={'index': 'blue', 'p': 'pink'},
             window=('index', 'p'), h=250,
             dim=lambda S, i, v: 'p' in S and 'index' in S and not (S['index'] <= i <= S['p'])),
        dict(type='array', var='suffix', label='suffix[i]：nums[i..] 的后缀或值', h=170,
             color=lambda S, i, v: 'orange' if 'p' in S and i == S['p'] + 1 else None),
        dict(type='array', var='res', label='res', h=170),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('now', 'now', 'green'), ('now 二进制', lambda S: format(S['now'], 'b') if 'now' in S else '', 'green')],
    captions={
        'suffix = [nums[-1]]': '先预处理后缀或：`suffix[i]` = `nums[i..n-1]` 的按位或，代表「右边最多还能带来哪些 1」',
        'suffix.append': '`suffix` 倒着累积，`suffix[{index}]` 对应原下标 `{index}` 到末尾的或值',
        'suffix.reverse': '翻转后 `suffix[i]` 对应从 `i` 到末尾：`{suffix}`',
        'cnt = [0] * 31': '`cnt[pos]`：窗口里第 `pos` 位为 1 的数有几个——左端点出窗时靠它判断这一位要不要从 now 里去掉',
        'p = -1': '`p` 是窗口右端点，只增不减',
        6: lambda S, B, r: ('后缀或预处理完了' if len(S.suffix) == len(S.nums) else f'从倒数第二个往前，`index = {S.index}`'),
        15: lambda S, B, r: ('所有左端点都处理完了' if len(S.res) == len(S.nums) else f'左端点 `index = {S.index}`'),
        'if p < index': lambda S, B, r: (f'`p = {S.p} < index = {S.index}`：窗口是空的，要重新开一个' if S.p < S.index
                                         else f'`p = {S.p} ≥ index`：窗口里已经有元素，沿用上一轮的窗口'),
        'p = index': '窗口先只含自己：右端点 `p = {p}`',
        'now = nums[index]': '`now = {now}`（二进制 `{bin(now)[2:]}`），同时把它的每一位计入 `cnt`',
        'while p + 1 < n': lambda S, B, r: (
            '`p + 1` 已到末尾，不能再扩' if S.p + 1 >= len(S.nums) else
            (f'`now | suffix[{S.p+1}] = {S.now | S.suffix[S.p+1]}` ≠ `now = {S.now}`：右边还有 now 没有的 1 → ==还得扩=='
             if (S.now | S.suffix[S.p + 1]) != S.now else
             f'`now | suffix[{S.p+1}] = {S.now | S.suffix[S.p+1]}` == `now`：右边所有 1 窗口里都有了 → ==停下==，不用再扩')),
        'p += 1': '右端点右移到 `p = {p}`',
        'now |= nums[p]': '把 `nums[{p}] = {nums[p]}` 或进来：`now = {now}`（`{bin(now)[2:]}`）',
        'res.append': '以 `{index}` 开头最短长度 = `p - index + 1 = {p} - {index} + 1` = =={p - index + 1}==',
        'remove = 0': '准备把 `nums[index]` 移出窗口：`or` 不能用异或直接撤销，要靠 `cnt` 看哪些位彻底没人了',
        'now ^= remove': lambda S, B, r: (f'移除后只有计数归零的位（`{bin(S.remove)[2:]}`）才从 now 去掉：`now` = `{S.now}`'
                                          if S.remove else f'`nums[{S.index}]` 的 1 在窗口里别的数也有 → now 不变 `{S.now}`'),
        'return res': '全部左端点处理完：`{res}`',
    },
    cards=dict(
        one_liner='左端点右移时，右端点只会不动或右移 → 滑动窗口',
        complexity='时间 `O(n log U)`，空间 `O(n)`',
        problem=['对每个下标 `i`，求以 `i` 开头、按位或值最大的 ==最短== 子数组长度',
                 '示例：`[1,0,2,1,3]` → `[3,3,2,2,1]`'],
        quote='若这个结果等于now，说明suffix中所有为1的位都在now中出现过，此时子数组的右边界就没有必要向后移动的。',
        quote_src='—— yiduobo 题解原文',
        idea=['左边界右移，右边界==只增不减==（原文用反证法证明），所以能用滑动窗口',
              '`now | suffix[p+1] == now`：右边所有的 1 窗口里都有了 → 右端点停下',
              '去掉左端点时不能用异或，要用 `cnt[pos]` 记每一位上 1 的个数，==归零的位==才从 now 去掉'],
        summary=['时间 `O(n log U)`，每个数最多按 31 位拆分三次',
                 '原文为 Python 2 写法，整数除法 `tmp /= 2` 已改为 `tmp //= 2`',
                 '易错点：左端点出窗时，`now` 里的位只有在 `cnt` 归零时才能删',
                 '对比灵神：灵神原地更新 nums 的后缀或（LogTrick），yiduobo 用后缀或 + 每位计数的滑窗'],
    ),
)
