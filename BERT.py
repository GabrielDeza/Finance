import pandas as pd
from sklearn.model_selection import train_test_split
import torch
import apex #useful for distributed training on fast_bert
from pytorch_pretrained_bert.tokenization import BertTokenizer
from fast_bert.data_cls import BertDataBunch #Useful Wrapper for BERT
from fast_bert.learner_cls import BertLearner
from fast_bert.metrics import accuracy

path = "~/something"
df = pd.read_hdf(path)


#Only taking a fraction of 1.6M tweets (160 000 tweets)
df = df.sample(frac = 0.05, random_state = 2020)



train, valid = train_test_split(df, test_size=0.2)

# Save back to .csv format
train.to_csv('/content/drive/My Drive/Colab Notebooks/data/train.csv', index=False)
valid.to_csv('/content/drive/My Drive/Colab Notebooks/data/valid.csv', index=False)

labels = ["0", "4"]
lb = pd.DataFrame(labels)
lb.to_csv('/content/drive/My Drive/Colab Notebooks/label/labels.csv',index=False)

#Default Arguments
args = {
    "max_seq_length": 512,
    "do_lower_case": True,
    "train_batch_size": 8,
    "learning_rate": 6e-5,
    "num_train_epochs": 12.0,
    "warmup_proportion": 0.002,
    "local_rank": -1,
    "gradient_accumulation_steps": 1,
    "fp16": True,
    "loss_scale": 128
}
bert_model = 'bert-base-uncased'

# The tokenizer object is used to split the text into tokens used in training
tokenizer = BertTokenizer.from_pretrained(bert_model,do_lower_case=args['do_lower_case'])
print(1)
# Check for GPU
device = torch.device('cuda')

# BertDataBunch contains the training, validation, and tests sets, alongside
# arguments and the tokenizer used in training
DATA_PATH = '/content/drive/My Drive/Colab Notebooks/data'
LABEL_PATH ='/content/drive/My Drive/Colab Notebooks/label'

databunch = BertDataBunch(DATA_PATH, LABEL_PATH,
                          tokenizer = 'bert-base-uncased',
                          train_file='train.csv',
                          val_file='valid.csv',
                          label_file='labels.csv',
                          text_col = 'text',
                          label_col='label',
                          batch_size_per_gpu = args['train_batch_size'],
                          max_seq_length = args['max_seq_length'],
                          multi_gpu=False,
                          multi_label=False,
                          model_type='bert')

# Choose the metrics used for the error function in training
metrics = []
metrics.append({'name': 'accuracy', 'function': accuracy})

import logging

logger = logging.getLogger()
OUTPUT_DIR = "/content/drive/My Drive/Colab Notebooks/output"

# The learner contains the logic for training loop, validation loop,
# optimiser strategies and key metrics calculation
learner = BertLearner.from_pretrained_model(databunch,
                                            bert_model,
                                            metrics=metrics,
                                            device=device,
                                            logger=logger,
                                            output_dir=OUTPUT_DIR,
                                            finetuned_wgts_path=None,
                                            is_fp16=args['fp16'],
                                            loss_scale=args['loss_scale'],
                                            multi_gpu=multi_gpu,
                                            multi_label=False)

# Train the model
learner.fit(6, lr=args['learning_rate'],
            schedule_type="warmup_cosine")

# Save the model into a file
learner.save_and_reload(MODEL_PATH, "trained_model_name")