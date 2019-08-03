import argparse
import os


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--filepath', type=str, required=True)
  parser.add_argument('--names', nargs='+', required=True)
  parser.add_argument('--starts', nargs='+', type=int, required=True)
  parser.add_argument('--ends', nargs='+', type=int, required=True)
  parser.add_argument('--saved_root', type=str, required=True)
  args = parser.parse_args()
  return args

def main(filepath, names, starts, ends, saved_root):
  """

  :param filepath:
  :param names:
  :param starts:
  :param ends:
  :param saved_dirs:
  :return:
  """
  assert len(starts) == len(ends)
  if len(starts) == 1:
    num_name = len(names)
    starts = starts * num_name
    ends = ends * num_name
  assert os.path.exists(filepath)
  if not os.path.exists(saved_root):
    os.makedirs(saved_root)
  saved_files = [os.path.join(saved_root, '%s.fq'%name) for name in names]
  saved_fs = []
  for saved_file in saved_files:
    saved_fs.append(open(saved_file, 'w'))
  with open(filepath) as fileobject:
    file_iter = iter(fileobject)

    try:
      while True:
        first_line = next(file_iter)
        first_line = first_line.rstrip('\n')
        matched = False
        for idx, name in enumerate(names):
          if first_line.endswith(name):
            second_line = next(file_iter)
            third_line = next(file_iter)
            four_line = next(file_iter)
            saved_fs[idx].write(second_line[starts[idx], ends[idx]] + '\n')
            saved_fs[idx].write(third_line)
            saved_fs[idx].write(four_line[starts[idx], ends[idx]] + '\n')
            matched = True
            break
        if not matched:
          for _ in range(3):
            # no matching, deprecated three lines below
            next(file_iter)
    except StopIteration:
      pass
  for f in saved_fs:
    f.close()



if __name__ == '__main__':
  args = parse_args()
  main(**vars(args))