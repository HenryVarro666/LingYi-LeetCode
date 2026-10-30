CONFIG = dict(
    num=540, title='有序数组中的单一元素', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分 · 按左右段长度奇偶性收缩',
    tags=['灵神题单·二分算法'],
    code='''
class Solution(object):
    def singleNonDuplicate(self, nums):

        l = 0
        r = len(nums) - 1
        while l < r:
            mid = (l + r) // 2
            if mid > l and nums[mid] == nums[mid - 1]:
                if (mid - l - 1) % 2 == 0:
                    l = mid + 1
                else:
                    r = mid - 2
            elif mid < r and nums[mid] == nums[mid + 1]:
                if (r - mid - 1) % 2 == 0:
                    r = mid - 1
                else:
                    l = mid + 2
            else:
                return nums[mid]
        
        return nums[l]
''',
    call='Solution().singleNonDuplicate([1,1,2,2,3,4,4,5,5,6,6])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums', h=330,
             pointers={'l': 'blue', 'r': 'pink', 'mid': 'yellow'},
             window=('l', 'r'),
             dim=lambda S, i, v: 'l' in S and not (S['l'] <= i <= S['r'])),
        dict(type='text', h=70, fn=lambda S: (f"搜索区间 `[{S['l']}, {S['r']}]`，长度 ==`{S['r']-S['l']+1}`==（含答案时必为奇数）" if 'l' in S and 'r' in S else '')),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow')],
    captions={
        'l = 0': '`l = 0`',
        'r = len': '`r = len(nums) - 1 = {r}`',
        'while l < r': lambda S, B, rr: f'`l = {S.l} < r = {S.r}`，区间里还有多个数，继续' if S.l < S.r else f'`l = r = {S.l}`：只剩一个数，它就是答案',
        'mid = (l + r)': '取中点 `mid = {mid}`，`nums[mid] = {nums[mid]}`',
        'if mid > l and nums[mid] == nums[mid - 1]': lambda S, B, rr: (f'`nums[{S.mid}] == nums[{S.mid-1}] = {S.nums[S.mid]}` → ==情况 1==：`mid` 是一对的右半' if S.mid > S.l and S.nums[S.mid] == S.nums[S.mid-1] else f'`mid` 不是某对的右半（或在左端），看情况 2'),
        'if (mid - l - 1) % 2 == 0': lambda S, B, rr: f'左边 `l ~ mid-2` 长度 `{S.mid - S.l - 1}`，' + ('==偶数== → 左边都是整对，答案在右边' if (S.mid - S.l - 1) % 2 == 0 else '==奇数== → 答案藏在左边'),
        'l = mid + 1': '答案在右边：`l = {l}`',
        'r = mid - 2': '答案在 `l ~ mid-2`：`r = {r}`',
        'elif mid < r and nums[mid] == nums[mid + 1]': lambda S, B, rr: (f'`nums[{S.mid}] == nums[{S.mid+1}] = {S.nums[S.mid]}` → ==情况 2==：`mid` 是一对的左半' if S.mid < S.r and S.nums[S.mid] == S.nums[S.mid+1] else f'`nums[{S.mid}]` 和左右都不相等 → ==情况 3=='),
        'if (r - mid - 1) % 2 == 0': lambda S, B, rr: f'右边 `mid+2 ~ r` 长度 `{S.r - S.mid - 1}`，' + ('==偶数== → 右边都是整对，答案在左边' if (S.r - S.mid - 1) % 2 == 0 else '==奇数== → 答案藏在右边'),
        'r = mid - 1': '答案在左边：`r = {r}`',
        'l = mid + 2': '答案在右边 `mid+2 ~ r`：`l = {l}`',
        'return nums[mid]': '`nums[mid]` 和两边都不同，它就是单一元素 → ==`{ret}`==',
        'return nums[l]': '二分结束，剩下的 `nums[{l}]` 就是答案 → ==`{ret}`==',
    },
    cards=dict(
        one_liner='看 mid 左右段长度的奇偶性，答案一定在奇数长度的那一边',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['有序数组里每个数出现两次，只有一个数出现一次，找出它',
                 '要求 `O(log n)` 时间',
                 '本视频：`[1,1,2,2,3,4,4,5,5,6,6]` → `3`'],
        quote='题目描述每个元素出现两次，而其中有一个只出现了一次，那么就有一个隐藏条件，即数组长度的奇偶性。',
        quote_src='—— yiduobo 题解原文',
        idea=['`nums[mid]` 若和左邻相等，就把 `mid-1, mid` 当一对，看 `l ~ mid-2` 的长度',
              '该段长度为奇数，说明答案在里面；偶数则答案在右边',
              '和右邻相等同理；和两边都不等，`nums[mid]` 本身就是答案'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '收缩时要跳过整对：`r = mid - 2`、`l = mid + 2`',
                 '原文为 Python 2 写法，`mid = (l + r) / 2` 已改为 `//`',
                 '对比灵神：灵神只查偶数下标，判断 `nums[2k] != nums[2k+1]`，更短'],
    ),
)
