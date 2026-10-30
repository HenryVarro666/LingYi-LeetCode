def _top(S):
    if 'nums' not in S:
        return ''
    return '二进制 1 的个数：' + '  '.join(f'`{v}`→=={bin(v).count("1")}==' for v in S['nums'])


def _grp(S, i, v):
    return {1: 'blue', 2: 'green', 3: 'purple', 4: 'pink'}.get(bin(v).count('1'), 'orange') if 'ma' in S else None


def _chk(S, B, ret):
    v, pm = S.nums[S.index], S.pre_ma
    if v < pm:
        return f'`nums[{S.index}] = {v} < pre_ma = {pm}`：比上一组最大值还小，组间又不能换 → 无法有序'
    return f'`nums[{S.index}] = {v} ≥ pre_ma = {pm}`：没问题，继续'


CONFIG = dict(
    num=3011, title='判断一个数组是否可以变为有序', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='按 1 的个数分段 · 对比上一段最大值',
    tags=['灵神题单', '分组循环', '难度分 1497'],
    code='''
class Solution(object):
    def canSortArray(self, nums):

        def count(x):
            cnt = 0
            while x:
                if x % 2 == 1:
                    cnt += 1
                x //= 2
            return cnt

        pre_ma = 0
        ma = nums[0]
        cnt = count(nums[0])
        for index in range(1, len(nums)):
            v = count(nums[index])
            if v == cnt:
                ma = max(ma, nums[index])
            else:
                pre_ma = ma
                ma = nums[index]
                cnt = v

            if nums[index] < pre_ma:
                return False

        return True
''',
    call='Solution().canSortArray([8,4,2,30,15])',
    expect=True,
    skip=['while x:', 'if x % 2', 'cnt += 1', 'x //= 2', 'cnt = 0'],
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='array', var='nums', label='nums（同色 = 1 的个数相同 = 同一段）', cell=100,
             pointers={'index': 'pink'}, color=_grp),
        dict(type='text', fn=lambda S: (f"上一段最大 `pre_ma = {S['pre_ma']}`，当前段最大 `ma = {S['ma']}`，当前段 1 的个数 `cnt = {S['cnt']}`"
                                        if 'ma' in S else ''), size=26),
    ],
    watch=[('index', 'index', 'pink'), ('v', 'v', 'blue'), ('cnt', 'cnt'), ('ma', 'ma', 'green'), ('pre_ma', 'pre_ma', 'orange')],
    captions={
        'def count': '`count(x)`：数 `x` 二进制里 1 的个数（每次看最低位再除 2）',
        'return cnt': '`count` 返回 `{ret}`：这个数二进制里有 {ret} 个 1',
        'pre_ma = 0': '`pre_ma`：上一段的最大值，第一段前面没有，记 0',
        'ma = nums[0]': '`ma`：当前段的最大值，先放第一个数 `{ma}`',
        'cnt = count(nums[0])': '当前段的特征：1 的个数 `cnt = {cnt}`',
        'for index': lambda S, B, r: ('下标都看完了，循环结束' if B.get('index') == S.index and 'index' in B
                                      else f'看下标 `{S.index}` 的数 `{S.nums[S.index]}`，决定它属于当前段还是新的一段'),
        'v = count': '`nums[{index}] = {nums[index]}` 有 `{v}` 个 1',
        'if v == cnt': lambda S, B, r: (f'`v = {S.v} == cnt = {S.cnt}` → 同一段，能互相交换' if S.v == S.cnt
                                        else f'`v = {S.v} ≠ cnt = {S.cnt}` → 新的一段开始了'),
        'ma = max': '同一段内部可任意交换，只需记最大值：`ma = {ma}`',
        'pre_ma = ma': '上一段结束，它的最大值 `{pre_ma}` 成为门槛',
        'ma = nums[index]': '新段先只有这个数：`ma = {ma}`',
        'cnt = v': '当前段 1 的个数更新为 `{cnt}`',
        'if nums[index] <': _chk,
        'return False': '无法有序，返回 `False`',
        'return True': '每个数都不小于上一段最大值 → 段内排好序后整体有序，返回 `True`',
    },
    cards=dict(
        one_liner='按 1 的个数切成段：段内能随便换，段间的数不能越界',
        complexity='时间 `O(n log V)`，空间 `O(1)`',
        problem=['相邻且二进制 ==1 的个数相同== 的两个数可以交换，次数不限',
                 '能否把数组变成非降序？',
                 '示例：`[8,4,2,30,15]` → `true`'],
        quote='子数组内部由于可以任意交换，因此一定是可以变为有序的，那么如果要使得整个数组有序，就要求当前子数组中的所有数都大于等于上一个子数组的最大值。',
        quote_src='—— yiduobo 题解原文',
        idea=['数组按 1 的个数被切成若干子数组，==段与段之间的数永远换不过去==',
              '段内可排成有序，所以只需看：当前段每个数是否 `≥` 上一段最大值',
              '一趟遍历同时切段、算当前段最大值、和 `pre_ma` 比较'],
        summary=['时间 `O(n log V)`，`count` 每次循环二进制位数',
                 '易错：换段时先把 `ma` 转存给 `pre_ma`，再重置 `ma`',
                 '对比灵神：灵神用 `bit_count()` + 分组循环；这里手写 `count`，边遍历边比较',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '视频里 `count` 内部循环不逐行展示，只看返回值'],
    ),
)
