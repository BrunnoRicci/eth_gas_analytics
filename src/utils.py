import pandas as pd
import numpy as np
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def create_and_open_static_img(project_path, img_path, fig):
  ###Create static image for offline notebook usage###
  path = os.path.join(project_path, 'plots', img_path)
  fig.write_image(path)
  return Image.open(path)

#Functions
def get_latest_n_blocks(w3, num_blocks=10, offset=0):
  ###Get latest N blocks with an offset###
  #Get latest block
  block = w3.eth.getBlock('pending')
  #Latest block num
  latest_bloc_num = block.number
  blocks = []
  for b_num in range(latest_bloc_num - offset - num_blocks, latest_bloc_num - offset):
    block =  w3.eth.getBlock(b_num)
    blocks.append(block)
  return blocks

def get_all_transactions(w3, blocks):
  ###Get all transactions for a list of block###
  transactions = []
  for block in blocks:
    for trans_hash in block.transactions:
      transaction = w3.eth.get_transaction(trans_hash)
      transactions.append(transaction)
  return transactions

def convert_dictlist_to_df(dictlist, columns):
  #Coverts list of dicts to df
  rows=[]
  for dl in dictlist:
    row = []
    for key in columns:
      if key in dl.keys():
        row.append(dl[key])
      else:
        row.append(None)
    rows.append(row)
  #Create df
  df = pd.DataFrame(rows, columns=columns)
  return df

def create_block_df(blocks):
  ###Convert list of blocks to pandas df###
  columns = blocks[0].keys()
  #Converts list of dicts to df
  return convert_dictlist_to_df(blocks, columns)

def create_transaction_df(transactions):
  ###Converts list of trasactions to pandas df###
  columns = ['blockHash', 'blockNumber','from', 'gas',
             'gasPrice', 'maxFeePerGas', 'maxPriorityFeePerGas',
             'hash', 'input', 'nonce', 'to', 'transactionIndex',
             'value', 'type', 'accessList', 'chainId', 'v', 'r', 's', 'tokenId']
  #Coverts list of dicts to df
  return convert_dictlist_to_df(transactions, columns)

def create_one_block(text, text_class, color, font_file, font_size=80, w=300, h=300):
    ###Creates one image for text plot###
    #Create Image
    img_arr = np.zeros((h, w, 3), dtype=np.uint8)
    img_arr[:,:] = [32, 32, 32]
    img = Image.fromarray(img_arr, 'RGB')
    #Draw text
    draw = ImageDraw.Draw(img)
    #Value
    font = ImageFont.truetype(font_file, font_size)
    draw.text((60, 30), text, color, font=font)
    #GWEI
    font = ImageFont.truetype(font_file, 50)
    draw.text((80, 40 + font_size), 'GWEI', color, font=font)
    #Percetnage
    font = ImageFont.truetype(font_file, font_size)
    draw.text((65, 30 + 2*font_size), text_class, color, font=font)
    return img
