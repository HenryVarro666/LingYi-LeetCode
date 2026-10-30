def _win_left(S):
    if S.get('_line') in (16, 17) and 'key' in S and S['key'] in S['first'] and S['first'][S['key']] < S['index']:
        return S['first'][S['key']] + 1
    return None


def _parity_color(S, i, v):
    if 'index' not in S or i > S['index']:
        return None
    return 'green' if v % 2 == 0 else 'pink'


def _txt(S):
    if 'index' not in S:
        return '`diff` = 前缀里偶数个数 − 奇数个数；`xor` = 前缀异或值；`first` 记每种 (xor, diff) 首次出现的下标'
    ln = S['_line']
    v = S['v']
    head = f"`v = {v}`（=={'偶' if v % 2 == 0 else '奇'}数==）"
    if ln <= 8:
        return head
    if ln == 9:
        return head + f"：`xor = {S['xor']}`"
    if ln <= 13:
        return head + f"：`xor = {S['xor']}`，`diff = {S['diff']}`"
    key, first = S['key'], S['first']
    if ln == 19:
        return f"`first[{key}] = {S['index']}`：这个组合第一次出现"
    if key in first and first[key] < S['index']:
        return f"`{key}` 首次在下标 {first[key]} → 子数组 `nums[{first[key] + 1}..{S['index']}]` 合法"
    return f'`key = {key}`：`first` 里还没有'


def _key_cap(S, B, ret):
    key, first = S.key, S.first
    if key in first:
        return f'`{key}` 在 `first` 里：==两个前缀的 xor 和 diff 都一样==，中间那段异或为 0、奇偶数量相等'
    sx = [k for k in first if k[0] == key[0]]
    sd = [k for k in first if k[1] == key[1]]
    if sx:
        return f'`{key}` 不在 `first` 里（xor 和 `{sx[0]}` 相同，但 diff 不同）'
    if sd:
        return f'`{key}` 不在 `first` 里（diff 和 `{sd[0]}` 相同，但 xor 不同）→ 必须==两个都相同=='
    return f'`{key}` 不在 `first` 里，是新组合'


CONFIG = dict(
    num=3755, title='最大平衡异或子数组的长度', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀异或 + 偶奇之差 · 哈希表记首次位置',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def maxBalancedSubarray(self, nums):
        
        first = {(0, 0): -1}
        diff = 0
        xor = 0
        res = 0
        for index, v in enumerate(nums):
            xor ^= v
            if v % 2 == 0:
                diff += 1
            else:
                diff -= 1
            
            key = (xor, diff)
            if key in first:
                res = max(res, index - first[key])
            else:
                first[key] = index
        
        return res
''',
    call='Solution().maxBalancedSubarray([3,2,8,5,4,14,9,15])',
    expect=8,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 偶数，粉 = 奇数；框 = 合法子数组）', cell=84, pointers={'index': 'blue'},
             window=(_win_left, 'index'), color=_parity_color, h=190),
        dict(type='map', var='first', label='first：(xor, diff) → 首次出现的下标', fmt=lambda k, v: f'{k}: {v}', h=210, font=26),
        dict(type='text', h=110, size=28, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v'), ('xor', 'xor', 'cyan'), ('diff', 'diff', 'orange'), ('res', 'res', 'green')],
    captions={
        'first = {': '`first`：每个 (xor, diff) 首次出现的下标。空前缀 `(0, 0)` 记成 `-1`',
        'diff = 0': '`diff`：前缀中==偶数个数 − 奇数个数==',
        'xor = 0': '`xor`：前缀异或值，初始为 0',
        'res = 0': '`res`：答案，不存在合法子数组就是 0',
        'for index, v': lambda S, B, r: (f'`index = {S.index}`，先处理 `v = {S.v}`' if 'index' in S and ('index' not in B or S.index != B.index)
                                         else '遍历结束'),
        'xor ^= v': '`xor = {B.xor} ^ {v}` → =={xor}==：区间异或为 0 ⇔ 两端的前缀异或值相等',
        'if v % 2 == 0': lambda S, B, r: (f"`{S.v} % 2 == 0` → =={'成立' if S.v % 2 == 0 else '不成立'}==，"
                                          f"{'偶数让 diff 加 1' if S.v % 2 == 0 else '奇数让 diff 减 1'}"),
        'diff += 1': '偶数：`diff` {B.diff} → =={diff}==',
        'diff -= 1': '奇数：`diff` {B.diff} → =={diff}==',
        'key = (xor, diff)': '当前组合 `key = ({xor}, {diff})`',
        'if key in first': _key_cap,
        'res = max': '子数组长度 = `index − first[key]` = `{index} − ({first[key]})` = `{index - first[key]}`，`res` → =={res}==',
        'first[key] = index': '第一次见到 `{key}`：`first[key] = {index}`，以后再遇到就能算出一段',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='两个前缀的 (异或值, 偶奇之差) 一样，中间就是合法子数组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找最长子数组：按位异或为 0，且奇数偶数个数相等，没有则返回 0',
                 '示例：`[3,2,8,5,4,14,9,15]` → `8`（整个数组）',
                 '本视频就用这个示例'],
        quote='若nums[left: right + 1]的异或值为0，且其中奇数与偶数的数量相同，那么就说明nums[:left]的异或值与nums[:right + 1]的异或值相同，同时这两个前缀数组中偶数与奇数数量之差也相同。',
        quote_src='—— yiduobo 题解原文',
        idea=['拆成前缀问题：区间合法 ⇔ 两个前缀的 `xor` 相同 ==且== `diff` 相同',
              '一趟遍历，哈希表 `first` 记每个 `(xor, diff)` 第一次出现的位置',
              '再次遇到同一个组合：`index − first[key]` 就是以 `index` 结尾的最长合法子数组'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '这里 `diff` 是偶数个数减奇数个数（灵神是奇减偶），含义对称',
                 '`first[(0, 0)] = -1` 不能少，否则从下标 0 开头的子数组会漏掉',
                 '组合已存在时不更新 `first`：保留最早位置，区间才最长',
                 '代码与原文一致，Python 3 可直接运行'],
    ),
)
