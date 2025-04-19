import sys
import io

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)

def solve():
    try:
        words = []
        for line in sys.stdin:
            word = line.strip()
            if word:
                words.append(word)
        print(f"Received words: {words}")  # Debug print

        if len(words) <= 1:
            print(-1)
            return

        max_combined_length = -1
        found_pair = False
        n = len(words)

        for i in range(n):
            word1 = words[i]
            if len(word1) < 2:
                continue
            print(f"Checking word1: '{word1}'") # Debug print
            for j in range(n):
                if i == j:
                    continue

                word2 = words[j]
                if len(word2) < 2:
                    continue
                print(f"  Comparing with word2: '{word2}'") # Debug print
                if word1[-2:] == word2[:2]:
                    found_pair = True
                    current_combined_length = len(word1) + len(word2) - 2
                    max_combined_length = max(max_combined_length, current_combined_length)
                    print(f"    Match found: '{word1[-2:]}' == '{word2[:2]}', combined length: {current_combined_length}") # Debug print

        print(max_combined_length)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        print(-1)

if __name__ == "__main__":
    solve()
