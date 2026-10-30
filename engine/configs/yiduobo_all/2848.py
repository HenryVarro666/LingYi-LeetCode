def _txt(S):
    if 'nowx' not in S:
        return ''
    s = f"当前合并区间 `[{S['nowx']}, {S['nowy']}]`"
    if 'x' in S and S.get('_line') in (7, 8, 9):
        s += f"，新区间 `[{S['x']}, {S['y']}]`"
    if 'res' in S:
        s += f"，已结算长度 =={S['res']}=="
    return s


CONFIG = dict(
    num=2848, title='与车相交的点', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='排序 + 合并区间',
    tags=['差分', '难度分 1230'],
    code='''
class Solution(object):
    def numberOfPoints(self, nums):

        nums.sort()
        nowx, nowy = nums[0]
        res = 0
        for x, y in nums[1:]:
            if x <= nowy:
                nowy = max(nowy, y)
            else:
                res += nowy - nowx + 1
                nowx, nowy = x, y
        
        return res + nowy - nowx + 1
''',
    call='Solution().numberOfPoints([[3,6],[1,5],[8,9],[4,7],[11,12]])',
    expect=11,
    views=[
        dict(type='intervals', var='nums', pointer='nums.index([x, y])', h=330, label='nums（排序后，黄=正在看的区间）'),
        dict(type='text', fn=_txt, size=26, h=70),
    ],
    watch=[('nowx', 'nowx', 'blue'), ('nowy', 'nowy', 'pink'), ('res', 'res', 'green')],
    captions={
        'nums.sort()': '按起点从小到大排序：这样后面区间的起点都 `≥` 前面的，只需要和「最后一个区间」比较',
        'nowx, nowy = nums[0]': '用最左边的区间做初始：`[nowx, nowy] = [{nowx}, {nowy}]`',
        'if x <= nowy': '新区间起点 `{x}` {"≤" if x <= nowy else ">"} 当前终点 `{nowy}` → ==' '{"重叠，要合并" if x <= nowy else "不重叠"}==',
        'nowy = max': '重叠：左边界 `{nowx}` 不变（排序保证），右边界取较大者 → `nowy = {nowy}`',
        'res += ': '不重叠：`[{B.nowx}, {B.nowy}]` 不会再和后面任何区间相交，结算长度 `{B.nowy} - {B.nowx} + 1 = {res - B.res}`，累计 =={res}==',
        'nowx, nowy = x, y': '以新区间 `[{x}, {y}]` 作为新的「最后一个区间」',
        'return res': '遍历完还剩最后一个区间 `[{nowx}, {nowy}]`，把它的长度也加上，总共 =={ret}== 个点',
    },
    cards=dict(
        one_liner='排序后合并区间，所有合并区间长度之和就是答案',
        complexity='时间 `O(n log n)`，空间 `O(1)`（原地排序）',
        problem=['`nums[i] = [start, end]` 是车在数轴上占的整数点',
                 '求被任意一辆车覆盖的整数点个数',
                 '示例：`[[3,6],[1,5],[4,7]]` → `7`；这里用 5 个区间演示合并与断开'],
        quote='经典的区间合并问题。将所有区间按起点从小到大排序，使用变量 nowx, nowy 记录之前遍历过的最后这个区间的起点和终点。',
        quote_src='—— yiduobo 题解',
        idea=['若 `x <= nowy`：重叠，合并，右边界取 `max(nowy, y)`',
              '若 `x > nowy`：断开，因为起点有序，后面区间也碰不到它，==先结算再换新区间==',
              '最后别忘了结算手里的那一段'],
        summary=['复杂度：排序 `O(n log n)`，遍历 `O(n)`',
                 '易错点：循环结束后还要再加最后一个区间的长度',
                 '长度是 `nowy - nowx + 1`，整数点要 +1',
                 '原文已是 Python 3 写法，未做修改'],
    ),
)
