def _r(S):
    if 'c' not in S or 'cnt' not in S:
        return None
    k = sum(S['cnt'].values()) - (1 if S.get('_line') == 15 else 0)
    return min(k, len(S['capacity']) - 1)


CONFIG = dict(
    num=3728, title='边界与内部和相等的稳定子数组', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 哈希表，连续 0 扣除',
    tags=['灵神题单·常用数据结构', '难度分 1909'],
    code='''
class Solution(object):
    def countStableSubarrays(self, capacity):

        s = 0
        cnt = {}
        res = 0
        pre = None
        for c in capacity:
            s += c
            key = (s - c - c, c)
            res += cnt.get(key, 0)
            if c == 0 and pre == 0:
                res -= 1
            pre = c
            cnt[(s, c)] = cnt.get((s, c), 0) + 1
        
        return res
''',
    call='Solution().countStableSubarrays([9,3,3,3,9,0,0])',
    expect=2,
    views=[
        dict(type='array', var='capacity', label='capacity（箭头 = 当前右端点 right）', h=190,
             pointers={_r: 'blue'}, pointer_labels={_r: 'right'}, cell=90),
        dict(type='map', var='cnt', label='cnt：(s[left], capacity[left]) → 个数',
             fmt=lambda k, v: f'{k}: {v}', h=270, font=28),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"查找 `key = (s − 2c, c) = {S['key']}`，已有 `{S['cnt'].get(S['key'], 0)}` 个" if 'key' in S else '')),
    ],
    watch=['s', 'c', 'pre', ('res', 'res', 'green')],
    captions={
        's = 0': '`s` 是前缀和（包含当前元素）',
        's += c': '把 `{c}` 加进前缀和：`s = {s}`',
        'key = ': '右端点是 `{c}`：左端点 `s[left]` 需要等于 `s − 2c = {s - c - c}`，且 `capacity[left] = {c}` → 找 `{key}`',
        'res += cnt.get': '`cnt` 里有 `{cnt.get(key, 0)}` 个匹配的左端点 → `res = {res}`',
        'res -= 1': '特殊情况：连续两个 0，中间“和”为空 = 0，被误算成长度 2 的稳定数组，扣掉 1 → `res = {res}`',
        'pre = c': '记下当前元素，下一轮用来判断是不是连续的 0',
        'cnt[(s, c)] =': '把当前元素作为以后的左端点存入：`({s}, {c})` 出现 `{cnt[(s, c)]}` 次',
        'return res': '稳定子数组一共 =={res}== 个',
    },
    cards=dict(
        one_liner='转成前缀和之差，再单独扣掉连续 0 的误判',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['长度至少 3，首尾元素等于中间所有元素之和的子数组叫稳定数组',
                 '数出 `capacity` 里稳定子数组的数量',
                 '示例：`[9,3,3,3,9,0,0]` → 2'],
        quote='需要特别注意的是，上面的做法并没有考虑到长度至少为3这一条件，因此在遇到两个连续的0时会出现问题。',
        quote_src='—— yiduobo 题解',
        idea=['中间和写成 `s[right−1] − s[left]`，整理出 `s[left] = s[right] − 2·capacity[right]`',
              '哈希表按 `(s, c)` 记数，每个右端点直接查 `(s − 2c, c)`',
              '这样没管长度 ≥ 3：连续 `0, 0` 会被误算，遇到时答案减 1'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：先用 `cnt.get` 查，再把当前元素存入',
                 '易错点：只有连续两个 0 会出现长度 2 的误判',
                 '同类：560 和为 K 的子数组'],
    ),
)
