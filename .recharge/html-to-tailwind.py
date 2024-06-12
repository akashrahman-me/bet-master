import os
import warnings
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppresses most TensorFlow logging
warnings.filterwarnings('ignore')  # Suppresses Python warnings

# Install SentencePiece (you only need to do this once in your environment)
# !pip install sentencepiece

# Example data: list of (disorganized_html, organized_html) pairs
data = [
    ("<div class='w-[411px] h-[424px] relative bg-white'><div class='left-[56px] top-[19px] absolute text-black text-2xl font-bold font-[Inter]'>Latest Articles</div></div>",
     "<section class='max-w-sm mx-auto p-4 bg-white'><h2 class='text-2xl font-bold text-black mb-4'>Latest Articles</h2></section>")
    # Add more pairs as needed...
]

# Initialize the tokenizer
tokenizer = T5Tokenizer.from_pretrained('t5-small')

# Preprocess the data
def preprocess_data(data):
    inputs = [item[0] for item in data]
    targets = [item[1] for item in data]
    
    input_encodings = tokenizer(inputs, padding=True, truncation=True, return_tensors="pt")
    target_encodings = tokenizer(targets, padding=True, truncation=True, return_tensors="pt")
    
    return input_encodings, target_encodings

input_encodings, target_encodings = preprocess_data(data)

# Initialize the model
model = T5ForConditionalGeneration.from_pretrained('t5-small')

# Create a custom dataset
class HTMLDataset(torch.utils.data.Dataset):
    def __init__(self, input_encodings, target_encodings):
        self.input_encodings = input_encodings
        self.target_encodings = target_encodings

    def __getitem__(self, idx):
        return {key: val[idx] for key, val in self.input_encodings.items()}, {key: val[idx] for key, val in self.target_encodings.items()}

    def __len__(self):
        return len(self.input_encodings.input_ids)

train_dataset = HTMLDataset(input_encodings, target_encodings)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=5,
    per_device_train_batch_size=2,
    save_steps=10_000,
    save_total_limit=2,
    logging_dir='./logs',
    logging_steps=200,
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

# Train the model
trainer.train()

# Define a function for inference
def clean_html(input_html):
    input_ids = tokenizer.encode(input_html, return_tensors='pt')
    outputs = model.generate(input_ids, max_length=512, num_beams=4, early_stopping=True)
    organized_html = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return organized_html

# Test the model
disorganized_html = "<div class='w-[411px] h-[424px] relative bg-white'><div class='left-[56px] top-[19px] absolute text-black text-2xl font-bold font-[Inter]'>Latest Articles</div></div>"
organized_html = clean_html(disorganized_html)
print(organized_html)
