class Solution:
    def countGoodTriplets(self, arr: List[int], a: int, b: int, c: int) -> int:
        n = len(arr)
        ans = 0
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if abs(arr[i] - arr[j]) <= a and abs(arr[j] - arr[k]) <= b and abs(arr[i] - arr[k]) <= c:
                        ans += 1
        return ans
    



####################

## 前缀和

class Solution:
    def countGoodTriplets(self, arr: List[int], a: int, b: int, c: int) -> int:
        mx = max(arr)
        s = [0] * (mx + 2)  # cnt 数组的前缀和（值域前缀和）
        ans = 0
        for j, y in enumerate(arr):
            for z in arr[j + 1:]:
                if abs(y - z) > b:
                    continue
                l = max(y - a, z - c, 0)
                r = min(y + a, z + c, mx)
                ans += max(s[r + 1] - s[l], 0)  # 如果 l > r + 1，s[r + 1] - s[l] 可能是负数
            for v in range(y + 1, mx + 2):
                s[v] += 1  # 把 y 加到 cnt 数组中，更新所有受到影响的前缀和
        return ans
##############################3


## 排序 + 枚举中间 + 三指针
class Solution:
    def countGoodTriplets(self, arr: List[int], a: int, b: int, c: int) -> int:
        idx = sorted(range(len(arr)), key=lambda i: arr[i])

        ans = 0
        for j in idx:
            y = arr[j]
            left = [arr[i] for i in idx if i < j and abs(arr[i] - y) <= a]
            right = [arr[k] for k in idx if k > j and abs(arr[k] - y) <= b]

            k1 = k2 = 0
            for x in left:
                while k2 < len(right) and right[k2] <= x + c:
                    k2 += 1
                while k1 < len(right) and right[k1] < x - c:
                    k1 += 1
                ans += k2 - k1
        return ans