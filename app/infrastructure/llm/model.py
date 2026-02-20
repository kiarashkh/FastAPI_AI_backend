from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LLMModel:
    def __init__(self, model_name:str = "microsoft/phi-2"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None

    def load(self):
        """Load LLM model"""
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name, torch_dtype=torch.float16, device_map="auto")
        
    def generate(self, prompt:str, max_tokens:int = 100):
        """Generate text with model"""
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens= max_tokens)
        return self.tokenizer.decode(outputs[0]), len(inputs["input_ids"][0])