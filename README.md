# StockBuff

Definition


## StockBuff Model Directory and Loading

### Model Directory Structure

```yaml
└── data
└── models
    ├── finbert_v1
        ├── config.json
        ├── gitattributes.txt
        ├── pytorch_model.bin
        ├── special_tokens_map.json
        ├── tokenizer_config.json
        ├── vocab.txt
        ├── README.md
    ├── Resources
        ├── chatwords.txt
        ├── ...
    └── en_core_web_lg
        ├── __init__.py
        ├── meta.json
        └── en_core_web_lg-2.2.5
            ├── config.cfg
            ├── meta.json
            └── ...
```

### Model Path Setting

```bash
# PATH:
root_dir = os.path.abspath("../")
data_dir = os.path.join(root_dir, "data")
output_dir = os.path.join(root_dir, "outputs")
PATH_SPACY_MODEL = os.path.join(os.path.join(os.path.join(root_dir, "models"), "en_core_web_lg”), “en_core_web_lg-2.2.5”)
PATH_RES_DIR = os.path.join(os.path.join(root_dir, "models"), "resources")
PATH_BERT_MODEL = os.path.join(os.path.join(root_dir, "models"), "finbert_v1")
```

### Model Loading

```bash
# 1. Load Spacy Model:
import spacy
spacy_model_data_path = PATH_SPACY_MODEL
nlp = spacy.load(spacy_model_data_path, disable=['ner'])
from spacy import displacy
from spacy.matcher import Matcher
from spacy.lang.en import English
print("Spacy loaded.")
```

```bash
# 2. Load NLP Resources:
resources_dir_path = PATH_RES_DIR
```

```bash
3. Load sent.BERT model:
bert_model_fp = PATH_BERT_MODEL
```
