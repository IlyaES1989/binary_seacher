import timeit
import mmap


def binary_search(arr, x, left, right, len_x, len_row):
    while left < right:
        mid_row = int((left+right)/2)
        mid_bytes = mid_row * len_row

        if arr[mid_bytes:mid_bytes + len_x] < x:
            left = mid_row + 1
        else:
            right = mid_row

    left_bytes = left*len_row
    if arr[left_bytes:left_bytes + len_x] == x:
        return left_bytes
    else:
        raise ValueError('No results have been found for this search.')


def find_recommendation(path, sku, rank=None):
    with open(path, mode="r", encoding="utf-8") as file_obj:
        sku = bytes(sku, 'utf-8')
        if rank:
            rank = str(rank)
        value_dict = {}

        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as file:
            len_sku = file.find(b',')
            len_row = file.find(b'\n') + 1
            len_file = int(file.size() / len_row)

            start = binary_search(file,
                                  sku,
                                  left=0,
                                  right=len_file,
                                  len_x=len_sku,
                                  len_row=len_row)

            while file[start: start+len_sku] == sku:
                row = file[start: start+len_row-1].decode('utf-8').split(',')
                value = row[1]
                key = row[2]

                if value_dict.get(key):
                    value_dict[key] = value_dict.get(key) + [value, ]
                else:
                    value_dict[key] = [value, ]
                start += len_row
    if rank:
        value_list = value_dict.get(rank)
    else:
        value_list = []
        for key in value_dict:
            value_list += value_dict[key]

    return value_list


if __name__ == '__main__':
    test_data = ('0000qtZc3F', 'aTlK8A8gMm', '3nF6FijOVA', 'Q2RgLO85tR', '0000qtZc3F', 'zzzzJtUDad', 'T5116l54qW',
                 'dtZUeXFEEc', 'NbOFDESwLU', 'CYFPUMDWff', 'Ia5f7aPUpM', 'TZDrb4lIlk',)
    tt = []
    for data in test_data:
        sku = data
        filename = 'sorted_recommends.csv'
        a = timeit.repeat('find_recommendation(filename, sku)',
                          repeat=1,
                          number=1,
                          setup='from __main__ import find_recommendation, filename, sku')
        tt += a
    avr_time = sum(tt)/len(tt)
    min_time = min(tt)
    max_time = max(tt)

    print(' min time: \t\t%.2f ms \n' % (1000*min_time),
          'avr time:\t\t%.2f ms\n' % (1000*avr_time),
          'max time:\t\t%.2f ms\n' % (1000 * max_time),
          )
