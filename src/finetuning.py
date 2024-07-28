# In this program, we will finetune a bert transformer
# on our finalized data (resumes)
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    HfArgumentParser,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    pipeline
)
from tqdm import tqdm
from trl import SFTTrainer
import torch
import time
import pandas as pd
import numpy as np
from huggingface_hub import interpreter_login
from peft import LoraConfig, PeftModel, prepare_model_for_kbit_training
import os

interpreter_login()

cwd = os.getcwd()
data = pd.read_csv(cwd + "/FinetuneData/Resume.csv")
data = data.drop("Unnamed: 0",axis = 1)
print(data)

# Jsonify the data.
json_data = data.to_json(orient='records')

with open('data.json', 'w') as json_file:
    json_file.write(json_data)

# print(json_data)

base_model = "microsoft/phi-2"
new_model = "phi-2-talentmatch"

tokenizer = AutoTokenizer.from_pretrained(base_model,use_fast = True)
tokenizer.pad_token = tokenizer.unk_token
tokenizer.padding_side = "right"

model_name='microsoft/phi-2'
device_map = {"": 0}
original_model = AutoModelForCausalLM.from_pretrained(model_name, 
                                                      device_map=device_map,
                                                      quantization_config=bnb_config,
                                                      trust_remote_code=True,
                                                      use_auth_token=True)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=False,
)

model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=bnb_config,
    trust_remote_code=True,
    device_map={"": 0}
)

model.config.use_cache = False
model.config.pretraining_tp = 1