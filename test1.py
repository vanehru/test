#!/usr/bin/env python3
import sys
from collections import Counter

def solve():
    """
    Reads input stick lengths and determines if a square can be formed
    using four distinct sticks of the same length.
    """
    try:
        # 標準入力からnを読み込む
        try:
            n = int(sys.stdin.readline().strip())
        except ValueError:
            print("Error: Invalid input format. Ensure numbers are integers.", file=sys.stderr)
            return

        # nが4未満の場合、正方形は作れない
        if n < 4:
            print("No")
            # 残りの入力を読み飛ばす（もしあれば）
            sys.stdin.readline()
        try:
            a = list(map(int, sys.stdin.readline().strip().split()))
        except ValueError:
            print("Error: Invalid input format. Ensure numbers are integers.", file=sys.stderr)
            return

        # 標準入力から棒の長さaのリストを読み込む
        # split()でスペース区切りにし、map(int, ...)で各要素を整数に変換
        a = list(map(int, sys.stdin.readline().split()))

        # 制約チェック (任意ですが、堅牢性を高めるため)
        if not (1 <= n <= 50):
             # エラー処理または制約違反時のデフォルト挙動
             # ここでは制約違反でも処理を続行するが、エラーメッセージを出してもよい
             pass # 例: print("Warning: n is out of bounds (1 <= n <= 50)", file=sys.stderr)

        if len(a) != n:
            # 入力された棒の数とnが一致しない場合のエラー処理
            print("Error: Number of sticks does not match n.", file=sys.stderr)
            return # または適切なエラー処理

        # 各棒の長さが制約内かチェック (任意)
        # for length in a:
        #     if not (1 <= length <= 50):
        #         # print(f"Warning: Stick length {length} is out of bounds (1 <= a_i <= 50)", file=sys.stderr)
        #         pass


        # --- 正方形が作れるか判定 ---

        # 方法1: Counterを使って各長さの棒の本数を数える
        counts = Counter(a)

        # 4本以上同じ長さの棒があるか確認
        can_form_square = False
        for length in counts:
            if counts[length] >= 4:
                can_form_square = True
                break # 見つかったらループを抜ける

        # # 方法2: 配列を使って頻度を数える (長さの最大値が小さい場合に有効)
        # max_length = 50 # 制約より
        # freq = [0] * (max_length + 1) # 長さ1から50までを格納するためサイズ51
        # for length in a:
        #      if 1 <= length <= max_length: # 念のため範囲チェック
        #          freq[length] += 1
        #
        # can_form_square = False
        # for count in freq:
        #      if count >= 4:
        #          can_form_square = True
        #          break

        # 結果を出力
        if can_form_square:
            print("Yes")
        else:
            print("No")

    except ValueError:
        # int()やmap(int, ...)で変換エラーが起きた場合
        print("Error: Invalid input format. Ensure numbers are integers.", file=sys.stderr)
    except Exception as e:
        # その他の予期せぬエラー
        print(f"An unexpected error occurred: {e}", file=sys.stderr)


# スクリプトとして直接実行された場合にsolve()関数を呼び出す
# これはPythonの標準的な書き方です
if __name__ == '__main__':
    solve()
