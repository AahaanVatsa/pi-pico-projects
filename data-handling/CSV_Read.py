with open('/rf_log.csv', 'r') as f:
  lines = f.readlines()

clean_lines = []
for line in lines:
  clean_lines.append(line.strip())

print(' ')

for line in clean_lines:
  columns = line.split(',')
  print('\t'.join(columns))
