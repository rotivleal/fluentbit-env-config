import os

cfgs = {}

def is_fluent_bit_conf(key, idcs):
  if len(idcs) < 2:
    return False

  if key[:idcs[1]] == 'FLUENT_BIT_CFG':
    return True
  else:
    return False

def get_config_name_val(key, val, idcs):
  formatted_name = ''

  for x in range(3, len(idcs)):
    end_i = idcs[x + 1] if len(idcs) > x + 1 else len(key)

    if (x > 3):
      formatted_name += '_'

    formatted_name += key[idcs[x] + 1]
    
    for j in range(idcs[x] + 2, end_i):
      formatted_name += key[j].lower()
  
  return { formatted_name: val }

def merge_or_add(_id, _with, header):
  if _id not in cfgs:
    cfgs[_id] = { }

  if header not in cfgs[_id]:
    cfgs[_id] |= { header: {} }
  
  cfgs[_id][header] |= _with

def render():
  _str = ""

  for cfg_id, cfg_val in cfgs.items():
    for header, settings in cfg_val.items():
      _str += "[" + header + "]\n"
      for set_k, set_v in settings.items():
        _str += set_k + " " + set_v + "\n"

  return _str

for key, value in os.environ.items():
  idcs = [pos for pos, char in enumerate(key) if char == '_']

  if is_fluent_bit_conf(key, idcs):
    header = key[idcs[1] + 1:idcs[2]]
    _id = key[idcs[2] + 1:idcs[3]]

    config_val = get_config_name_val(key, value, idcs)

    merge_or_add(_id, config_val, header)

rendered = render()

cfg_file = open("/fluent-bit/etc/fluent-bit.conf", "w+")
cfg_file.write(rendered)
cfg_file.close()

print(rendered)
