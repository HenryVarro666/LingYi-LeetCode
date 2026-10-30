def _info(S):
    if 'index' not in S:
        return '`cnt`：当前段里负数个数；`neg_pos`：第一个负数的位置；`l`：上一个 0 的位置'
    return (f"当前段从 `{S['l'] + 1}` 开始，负数 `cnt = {S['cnt']}` 个"
            f"（{'偶数，整段为正' if S['cnt'] % 2 == 0 else '奇数，去掉第一个负数前的部分'}）；最长 `res` = =={S['res']}==")


CONFIG = dict(
    num=1567, title='乘积为正数的最长子数组长度', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='一趟扫描 · 记录首个负数位置',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def getMaxLen(self, nums):

        neg_pos = None
        cnt = 0
        res = 0
        l = -1
        for index, num in enumerate(nums):
            if num == 0:
                neg_pos = None
                cnt = 0
                l = index
            elif num > 0:
                if cnt % 2 == 0:
                    res = max(res, index - l)
                else:
                    res = max(res, index - neg_pos)
            else:
                cnt += 1
                if cnt % 2 == 0:
                    res = max(res, index - l)
                elif cnt == 1:
                    neg_pos = index
                else:
                    res = max(res, index - neg_pos)
        
        return res
''',
    call='Solution().getMaxLen([1,-2,-3,4,-1,0,2,3])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums', h=200, cell=90,
             pointers={'index': 'blue', 'neg_pos': 'pink'},
             window=('l + 1', 'index'),
             color=lambda S, i, v: ('yellow' if v == 0 else 'pink' if v < 0 else None) if 'index' in S else None,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='text', fn=_info, size=26, h=100),
    ],
    watch=[('index', 'index', 'blue'), ('cnt', 'cnt', 'pink'), ('neg_pos', 'neg_pos', 'orange'), ('l', 'l', 'yellow'), ('res', 'res', 'green')],
    captions={
        4: '`neg_pos`：当前段==第一个负数==的下标，还没遇到',
        5: '`cnt`：当前段负数个数',
        6: '`res` 记录答案',
        7: '`l`：上一个 0 的下标，没有 0 时是 `-1`，所以段长 = `index - l`',
        'if num == 0': '`num = {num}`：{"是 0，乘积必为 0，把数组在这里切开" if num == 0 else "不是 0，继续延长当前段"}',
        10: '0 把数组切断：`neg_pos` 清空',
        11: '`cnt` 清零，重新数负数',
        12: '新的一段从 `{index + 1}` 开始：`l = {l}`',
        'elif num > 0': '`num = {num}`：{"正数，不改变负数个数的奇偶" if num > 0 else "负数，要给 cnt 加一"}',
        'if cnt % 2 == 0': lambda S, B, r: (f'`cnt = {S.cnt}` 是偶数：从段首到 `index` 乘积为正' if S.cnt % 2 == 0
                                           else f'`cnt = {S.cnt}` 是奇数：要去掉到第一个负数为止的前缀'),
        'res = max(res, index - l)': '整段为正，长度 `{index} − ({l}) = {index - l}`：`res = max({B.res}, {index - l}) = =={res}==`',
        'res = max(res, index - neg_pos)': '去掉第一个负数（下标 `{neg_pos}`）及之前：长度 `{index} − {neg_pos} = {index - neg_pos}`，`res` → =={res}==',
        'cnt += 1': '遇到负数，`cnt` → {cnt}',
        'elif cnt == 1': lambda S, B, r: ('这是本段第 1 个负数：自己单独乘积为负，不能更新答案，记下 `neg_pos`' if S.cnt == 1
                                         else f'`cnt = {S.cnt}` 不是 1：用 `index - neg_pos` 更新'),
        'neg_pos = index': '记下第一个负数的位置 `neg_pos = {neg_pos}`',
        'return res': '最长长度 `{res}`',
    },
    cards=dict(
        one_liner='遇 0 就切段；段内负数个数为偶数，整段为正，否则去掉首个负数之前的部分',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给整数数组 `nums`，求==乘积为正数==的最长子数组长度',
                 '本视频：`[1,-2,-3,4,-1,0,2,3]` → `4`（`[1,-2,-3,4]`）',
                 '乘积是否为正，只看有没有 0 和负数个数的奇偶'],
        quote='那么只需要排除掉以数组中首个奇数所在位置为结尾的前缀，那么剩下的子数组中含有的负数个数就是偶数个了。',
        quote_src='—— yiduobo 题解原文',
        idea=['含 0 乘积必为 0：把数组按 0 切成若干段',
              '段内一趟扫描，记负数个数 `cnt` 和首个负数下标 `neg_pos`',
              '`cnt` 偶数用 `index - l`；奇数用 `index - neg_pos`，答案取最大'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '遇 0：`cnt`、`neg_pos` 清零，`l = index`',
                 '易错：段内第 1 个负数不能更新答案，只记 `neg_pos`；边界差一',
                 '原文思路段把“负数”笔误写成“奇数”，代码无需修改'],
    ),
)
