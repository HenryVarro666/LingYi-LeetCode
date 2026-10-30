def _poshow(S):
    if 'pos' not in S:
        return ''
    ks = sorted(S['pos'])
    s = '　'.join(f"pos[{k}]={list(reversed(S['pos'][k]))}" for k in ks)
    if 'mex' in S and 'now' in S:
        s += f"　｜　这一段 `now={S['now']}`，正在试 `mex={S['mex']}`，`nxt={S['nxt']}`"
    return s


CONFIG = dict(
    num=3948, title='字典序最大的 MEX 数组', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='哈希表记位置 · 逐段划分',
    tags=['难度分 2122'],
    code='''
class Solution(object):
    def maximumMEX(self, nums):
        
        pos = {}
        for index, v in enumerate(nums):
            if v not in pos:
                pos[v] = []
            pos[v].append(index)
        
        for v in pos:
            pos[v].reverse()

        res = []
        now = 0
        while now < len(nums):
            mex = 0
            nxt = now + 1
            while True:
                while mex in pos and pos[mex][-1] < now:
                    pos[mex].pop()
                    if not pos[mex]:
                        pos.pop(mex)
                
                if mex not in pos:
                    break
                
                nxt = max(nxt, pos[mex][-1] + 1)
                mex += 1

            res.append(mex)
            now = nxt
        
        return res
''',
    call='Solution().maximumMEX([0,1,0,2,0,1,0])',
    expect=[3, 2, 1],
    views=[
        dict(type='array', var='nums', label='nums', h=300, pointers={'now': 'blue'},
             window=('now', 'nxt'),
             dim=lambda S, k, v: 'now' in S and k < S['now']),
        dict(type='array', var='res', label='res', h=170, color=lambda S, k, v: 'green'),
        dict(type='text', fn=_poshow, size=26, h=120),
    ],
    watch=[('now', 'now', 'blue'), ('nxt', 'nxt', 'pink'), 'mex', ('res', 'res', 'green')],
    skip=['for v in pos', 'pos[v].reverse()', 'if v not in pos:', 'pos[v] = []', 'for index, v in', 'while True', 'break', 'mex += 1', 'if not pos[mex]:'],
    captions={
        'pos[v].append': '数字 `{v}` 出现在下标 `{index}`：`pos[{v}]` 记下所有位置',
        'res = []': '每个 `pos[v]` 已反转成降序，`pos[v][-1]` 就是最靠左的位置，`pop()` 即可删掉',
        'nxt = now + 1': '这一段从 `now={now}` 开始，至少含一个元素，所以下一段起点先设为 `nxt={nxt}`',
        'while mex in pos and pos[mex][-1] < now': lambda S, B, ret: (f"`pos[{S['mex']}]` 最左位置 `{S['pos'][S['mex']][-1]}` < `now={S['now']}`：在本段之前，已用掉，弹出" if S['mex'] in S['pos'] and S['pos'][S['mex']][-1] < S['now'] else f"`{S['mex']}` 在 `now={S['now']}` 及右侧的位置情况已经清理完"),
        'pos[mex].pop()': '弹出左侧的废位置：`pos[{mex}]` 还剩 `{pos.get(mex)}`',
        'pos.pop(mex)': '`{mex}` 在右侧已经一个都没有了，把它从 `pos` 里整个删掉',
        'if mex not in pos': lambda S, B, ret: (f"`now` 及右侧没有 `{S['mex']}` 了：这段的 mex 就定为 =={S['mex']}==，不能更大 → 切段" if S['mex'] not in S['pos'] else f"右侧还有 `{S['mex']}`，mex 还能变大，继续"),
        'nxt = max': '本段必须包含右侧最靠左的 `{mex}`（位置 `{pos[mex][-1]}`），所以 `nxt` 至少是 `{nxt}`；然后试 `mex = {mex+1}`',
        'res.append': '本段 mex = =={mex}==，加入结果 → `{res}`',
        'now = nxt': '下一段从 `{nxt}` 开始',
    },
    cards=dict(
        one_liner='每段让 mex 尽量大，同时段尽量短',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次取 `nums` 的前 `k` 个元素，把它们的 ==mex== 追加到 `result`，并把这 `k` 个元素删掉',
                 '求能得到的 ==字典序最大== 的 `result`',
                 '示例：`[0,1,0,2,0,1,0]` → `[3,2,1]`'],
        quote='每一轮操作，都应该让当前的nums[:k]能得到的MEX尽量大，同时这个k在MEX相同时应该尽量的小。',
        quote_src='—— yiduobo 题解',
        idea=['先遍历一次，用哈希表 `pos[v]` 记录每种数的所有下标（降序排列，方便从尾部弹）',
              '段起点 `now`，`mex` 从 0 往上试：`now` 右侧有 `mex` 就把最左边那个纳入本段，用 `nxt` 记下段尾 + 1',
              '右侧没有 `mex` 时本段的 mex 确定，加入结果，`now` 跳到 `nxt`'],
        summary=['时间 `O(n)`：每次试探成功都会让 `now` 至少前进一格，每个下标至多弹出一次',
                 '`pos[mex]` 被清空时要把键删掉，所以判断「有没有」只看 `mex in pos`',
                 '与「剩余元素里没有就切」等价：`nxt` 保存的是段尾后一位',
                 '原文就是 Python 3 可运行的写法，代码未改动'],
    ),
)
