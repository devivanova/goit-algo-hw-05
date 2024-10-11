import gdown
import timeit

urls = {
    "стаття_1.txt": "https://drive.google.com/uc?export=download&id=18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh",
    "стаття_2.txt": "https://drive.google.com/uc?export=download&id=18BfXyQcmuinEI_8KDSnQm4bLx6yIFS_w"
}

texts = {}
for filename, url in urls.items():
    gdown.download(url, filename, quiet=False)
    with open(filename, "r", encoding="ISO-8859-1") as f:
        texts[filename] = f.read()


# Алгоритм Кнута-Морріса-Пратта
def kmp_search(text, pattern):
    def compute_prefix_function(pattern):
        prefix = [0] * len(pattern)
        j = 0
        for i in range(1, len(pattern)):
            while j > 0 and pattern[i] != pattern[j]:
                j = prefix[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            prefix[i] = j
        return prefix

    prefix = compute_prefix_function(pattern)
    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = prefix[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == len(pattern):
            return i - j + 1
    return -1


# Алгоритм Боєра-Мура
def boyer_moore_search(text, pattern):
    def bad_character_table(pattern):
        table = {}
        length = len(pattern)
        for i in range(length - 1):
            table[pattern[i]] = length - i - 1
        return table

    table = bad_character_table(pattern)
    m = len(pattern)
    n = len(text)
    i = m - 1
    while i < n:
        j = m - 1
        while j >= 0 and text[i] == pattern[j]:
            i -= 1
            j -= 1
        if j < 0:
            return i + 1
        i += table.get(text[i], m)
    return -1


# Алгоритм Рабіна-Карпа
def rabin_karp_search(text, pattern, prime=101):
    m = len(pattern)
    n = len(text)
    hash_pattern = 0
    hash_text = 0
    h = 1

    for i in range(m - 1):
        h = (h * 256) % prime

    for i in range(m):
        hash_pattern = (256 * hash_pattern + ord(pattern[i])) % prime
        hash_text = (256 * hash_text + ord(text[i])) % prime

    for i in range(n - m + 1):
        if hash_pattern == hash_text:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            hash_text = (
                256 * (hash_text - ord(text[i]) * h) + ord(text[i + m])) % prime
            if hash_text < 0:
                hash_text += prime
    return -1


# Підрядки для тестування
existing_substring = "алгоритм"
non_existing_substring = "неіснуючийпідрядок"


# Функція для вимірювання часу виконання
def measure_time(search_func, text, pattern):
    start_time = timeit.default_timer()
    search_func(text, pattern)
    return timeit.default_timer() - start_time


# Замір часу для кожного тексту та підрядка
for filename, text in texts.items():
    print(f"\nРезультати для файлу {filename}:")
    time_kmp_existing = measure_time(kmp_search, text, existing_substring)
    time_boyer_moore_existing = measure_time(
        boyer_moore_search, text, existing_substring)
    time_rabin_karp_existing = measure_time(
        rabin_karp_search, text, existing_substring)

    time_kmp_non_existing = measure_time(
        kmp_search, text, non_existing_substring)
    time_boyer_moore_non_existing = measure_time(
        boyer_moore_search, text, non_existing_substring)
    time_rabin_karp_non_existing = measure_time(
        rabin_karp_search, text, non_existing_substring)

    print("Існуючий підрядок:")
    print(f"KMP: {time_kmp_existing:.6f} секунд")
    print(f"Boyer-Moore: {time_boyer_moore_existing:.6f} секунд")
    print(f"Rabin-Karp: {time_rabin_karp_existing:.6f} секунд")

    print("Вигаданий підрядок:")
    print(f"KMP: {time_kmp_non_existing:.6f} секунд")
    print(f"Boyer-Moore: {time_boyer_moore_non_existing:.6f} секунд")
    print(f"Rabin-Karp: {time_rabin_karp_non_existing:.6f} секунд")
