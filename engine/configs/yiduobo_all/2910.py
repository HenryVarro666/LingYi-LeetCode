CONFIG = dict(
    num=2910, title='合法分组的最少组数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='枚举最大组长 group_len',
    tags=['灵神题单', '难度分 2132'],
    code='''
class Solution(object):
    def minGroupsForValidAssignment(self, nums):

        cnt = {}
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
        
        group_len = min(cnt.values()) + 1
        while group_len > 1:
            flag = True
            res = 0
            for v in cnt:
                group_cnt = cnt[v] // group_len
                res += group_cnt

                rest_cnt = cnt[v] % group_len
                if rest_cnt > 0:
                    need = group_len - 1 - rest_cnt
                    if need > group_cnt:
                        flag = False
                        break
                    res += 1
                
            if flag:
                break
            
            group_len -= 1
        
        return res
''',
    call='Solution().minGroupsForValidAssignment([1,1,1,2,2,2,2,2,3,3,3])',
    expect=4,
    max_steps=110,
    views=[
        dict(type='map', var='cnt', h=190, label='cnt：每个数出现次数'),
        dict(type='text', h=80, fn=lambda S: (f"当前数 `{S['v']}`：`{S['cnt'][S['v']]}` 个，组长 `{S['group_len']}` 或 `{S['group_len']-1}`" if 'v' in S and 'group_len' in S and S['v'] in S['cnt'] else (f"尝试 group_len = `{S['group_len']}`" if 'group_len' in S else ''))),
        dict(type='text', h=70, fn=lambda S: (f"整组 group_cnt = `{S['group_cnt']}`，剩 rest_cnt = `{S['rest_cnt']}`，需补 need = `{S['need']}`" if 18 <= S['_line'] <= 22 and all(x in S for x in ('group_cnt', 'rest_cnt', 'need')) else '')),
    ],
    watch=['group_len', 'v', 'group_cnt', 'rest_cnt', 'need', ('res', 'res', 'green')],
    captions={
        'cnt[v] = cnt.get': '统计 `{v}` 的出现次数：`cnt[{v}] = {cnt[v]}`',
        'group_len = min': '`group_len` 的上限是最小出现次数加 1（再大最少的那个数就没法分）：从 =={group_len}== 开始往下试',
        'while group_len > 1': '试 `group_len = {group_len}`：每种数能否分成 `{group_len}` 或 `{group_len-1}` 大小的组',
        'flag = True': '先假设这个 `group_len` 可行，累计组数 `res` 清零',
        'for v in cnt': '检查数字 `{v}`，出现 `{cnt[v]}` 次',
        'group_cnt = ': '`group_cnt = {cnt[v]} // {group_len}` = {group_cnt} 个整组',
        'res += group_cnt': '先把 {group_cnt} 个整组计入：`res = {res}`',
        'rest_cnt = ': '剩余 `rest_cnt = {cnt[v]} % {group_len}` = {rest_cnt}',
        'if rest_cnt > 0': lambda S, B, ret: ('有剩余，要补成 `group_len - 1` 大小的新组' if S.rest_cnt > 0 else '刚好整除，不需要补'),
        'need = ': '要补成 `{group_len-1}` 需 `need = {group_len} - 1 - {rest_cnt}` = {need} 个，只能从整组里各抽 1 个',
        'if need > group_cnt': lambda S, B, ret: (f"`need = {S.need} > group_cnt = {S.group_cnt}`：整组不够抽 → ==这个 group_len 不行==" if S.need > S.group_cnt else f"`need = {S.need} ≤ group_cnt = {S.group_cnt}`：抽得出来 → 可以"),
        'flag = False': '标记失败，换更小的 `group_len`',
        'res += 1': '多出一个补成的小组：`res = {res}`',
        'if flag': lambda S, B, ret: ('全部通过：当前 group_len 就是最大可行值，结束' if S.flag else '没通过，继续往下减'),
        'group_len -= 1': '`group_len` 减到 {group_len}',
        'return res': '最少组数 =={res}==',
    },
    cards=dict(
        one_liner='组数最少 ⇔ 组长最大：从上限往下找第一个可行的 group_len',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['球按编号分盒，同盒编号相同，最大盒最多比最小盒多 1',
                 '示例：`[10,10,10,3,1,1]` → `4`',
                 '本视频：`[1,1,1,2,2,2,2,2,3,3,3]` → `4`'],
        quote='题目要求分组的数量最少，那么实际上就是要找出一个最大的group_len，问是否能将每种数分为大小为group_len或者group_len - 1的组。',
        quote_src='—— yiduobo 题解原文',
        idea=['`group_len` 最大是最小出现次数加 1，往下逐个检测',
              '出现 `cnt` 次：整组 `cnt // group_len` 个，余数要补到 `group_len-1` 才成组',
              '补的办法只能从整组里各抽 1 个，所以要 `need ≤ group_cnt`'],
        summary=['时间 `O(n)`：每个 group_len 只需检查约 n/ma 种数，单个 O(1)',
                 '`group_len = 2` 一定可行，所以不会无解',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '对比灵神：灵神 k 是小组大小、大组 k+1 并直接用 ceil；yiduobo 以大组 group_len 为准、余数向下补'],
    ),
)
