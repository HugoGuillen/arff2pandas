import pandas as pd
from pandas import DataFrame
from scipy.io import arff
import numpy as np


def load(arff_file,decode_str=True):
    """Reads an ARFF file via scipy and returns a pandas DataFrame.
    Note: same as scipy.io.arff.load, this function does not support ARFF string types.
    
    Parameters
    ----------
    arff_file : str
        Path to ARFF file.
    decode_str : bool
        Wether or not sanitize resulting strings (removes the b'')
        
    Returns
    -------
    pandas.DataFrame
        Columns are ARFF attributes, rows correspond to instances.
    """
    data, meta = arff.loadarff(arff_file) 
    df = DataFrame(data,columns = meta.names())
    if decode_str:        
        df_str = df.select_dtypes(include=['object'])        
        if not df_str.empty:
            df[df_str.columns] = df_str.applymap(lambda x:x.decode('utf-8'))      
    return df


def _get_arff_meta_dict(dataframe):
    """Generates a dictionary with the ARFF metadata from a pandas DataFrame.    
    
    Parameters
    ----------
    dataframe : pandas.DataFrame
        DataFrame returned by `arff2pandas`.    
        
    Returns
    -------
    dict
        Keys: `_attributes`: attribute list; `_n`: number of instances. Left keys are the attributes properties.
    """    
    meta = {'_attributes':list(dataframe.columns)}
    meta['_n'] = dataframe.shape[0]
    for c in dataframe.columns:
        #print(c,df[c].dtype)
        meta[c] = {'dtype':str(dataframe[c].dtype)}
        if dataframe[c].dtype == 'object':
            meta[c]['type'] = 'nominal'
            meta[c]['values'] = list(dataframe[c].unique())
            meta[c]['min'] = np.NaN
            meta[c]['max'] = np.NaN
            meta[c]['mean'] = np.NaN
            meta[c]['std'] = np.NaN
        elif dataframe[c].dtype  == 'float64':            
            meta[c]['type'] = 'numeric'
            meta[c]['values'] = len(dataframe[c].unique())
            meta[c]['min'] = dataframe[c].min()
            meta[c]['max'] = dataframe[c].max()
            meta[c]['mean'] = dataframe[c].mean()
            meta[c]['std'] = dataframe[c].std()
        elif str(dataframe[c].dtype).startswith('date'):            
            meta[c]['type'] = 'date'
            meta[c]['values'] = len(dataframe[c].unique())
            meta[c]['min'] = dataframe[c].min()
            meta[c]['max'] = dataframe[c].max()
            meta[c]['mean'] = np.NaN
            meta[c]['std'] = np.NaN
    return meta


def get_meta(dataframe):
    """Generates a DataFrame with from the ARFF metadata from a pandas DataFrame.    
    
    Parameters
    ----------
    dataframe : pandas.DataFrame
        DataFrame returned by `arff2pandas`.    
        
    Returns
    -------
    DataFrame
        Rows are attributes, columns are properties.
    """    
    meta = _get_arff_meta_dict(dataframe)
    meta.pop('_n',None)
    attr_order = meta.pop('_attributes',None)
    _df = DataFrame.from_dict(meta,orient='index')
    _df = _df.reindex(attr_order)
    return _df