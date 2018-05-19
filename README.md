# arff2pandas
---
Load an ARFF file as a pandas DataFrame.

## Features
- Reads an ARFF file and loads it in-memory as a pandas `DataFrame`.
- Returns ARFF metadata as `DataFrame` or Python `dict`.
- Supports `numeric`, `real`, `nominal`, and `date` types. 

## Dependencies
- numpy
- scipy
- pandas

## Usage
```
import arff2pandas
df = arff2pandas.load('data/iris.arff')
df_meta = arff2pandas.get_meta(df)
```

For more examples, see the [Tutorial](tutorial.ipynb)

---

Created by Hugo Guillen, 2018.
