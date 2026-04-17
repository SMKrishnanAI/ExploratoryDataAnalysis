class univariate():
    def quanQual(self, dataset):
        qual=[]
        quan=[]
        for col_name in dataset.columns:
            if(dataset[col_name].dtype == 'O'):
                qual.append(col_name)
                #print("qual")
            else:
                quan.append(col_name)
                #print("quan")
        return(quan,qual)

    def freqTable(col_name, dataset):
        freqTable=pd.DataFrame(columns=["unique_values","Frequency", "RelFreq", "cumsum"])
        freqTable["unique_values"]=dataset[col_name].value_counts().index
        freqTable["Frequency"]=dataset[col_name].value_counts().values
        freqTable["RelFreq"]=(freqTable["Frequency"]/103)
        freqTable["cumsum"]=freqTable["RelFreq"].cumsum()
        return(freqTable)

        
    def univariate(self,dataset,quan):
        import pandas as pd
        import numpy as np
        descriptive = pd.DataFrame(index=['Mean','Median','Mode','Q1:25%','Q2:50%',
                                      'Q3:75%','99%','Q4:100%',"IQR","1.5rule",
                                      "Lesser","Greater","Min","Max","Kurtosis", "skew",
                                          "MinOutlier","MaxOutlier"],columns=quan)
        for col_name in quan:
            descriptive[col_name]["Mean"]    = dataset[col_name].mean()
            descriptive[col_name]["Median"]  = dataset[col_name].median()
            descriptive[col_name]["Mode"]    = dataset[col_name].mode()[0]
            descriptive[col_name]["Q1:25%"]  = dataset.describe()[col_name]["25%"]
            descriptive[col_name]["Q2:50%"]  = dataset.describe()[col_name]["50%"]
            descriptive[col_name]["Q3:75%"]  = dataset.describe()[col_name]["75%"]
            #
            #descriptive[col_name]["99%"]  = np.percentile(dataset[col_name],99)
            descriptive[col_name]["99%"] = np.nanpercentile(dataset[col_name], 99)
            #
            # The reason you are getting NaN for all columns in the 99% row 
            #(and potentially cascading into other calculations) is almost certainly due to Missing Values (Nulls) in your dataset.
            # By default, np.percentile() returns NaN if even a single value in the column is missing. 
            #This is a common issue with columns like salary where unplaced students might have empty entries.
            #1. The Direct Fix
            #To ignore NaN values while calculating the percentile, use [[[[ np.nanpercentile() ]]]] 
            #instead of np.percentile().
            # Python
            # Use nanpercentile to skip over null values
            #descriptive[col_name]["99%"] = np.nanpercentile(dataset[col_name], 99)
            #
            #
            descriptive[col_name]["Q4:100%"] = dataset.describe()[col_name]["max"]
            descriptive[col_name]["IQR"] = descriptive[col_name]["Q3:75%"] - descriptive[col_name]["Q1:25%"]
            descriptive[col_name]["1.5rule"] = 1.5 *  descriptive[col_name]["IQR"]
            descriptive[col_name]["Lesser"] =  descriptive[col_name]["Q1:25%"] - descriptive[col_name]["1.5rule"]
            descriptive[col_name]["Greater"] = descriptive[col_name]["Q3:75%"] + descriptive[col_name]["1.5rule"]
            descriptive[col_name]["Min"] = dataset[col_name].min()
            descriptive[col_name]["Max"] = dataset[col_name].max()
            descriptive[col_name]["Kurtosis"] = dataset[col_name].kurtosis()
            descriptive[col_name]["skew"] = dataset[col_name].skew()
            descriptive[col_name]["MinOutlier"] = descriptive[col_name]["Min"] < descriptive[col_name]["Lesser"]
            descriptive[col_name]["MaxOutlier"] = descriptive[col_name]["Max"] > descriptive[col_name]["Greater"]
        return(descriptive)


    def outlier_col(self,quan,descriptive):
        lesser,greater=[],[]
        for col_name in quan:
            if (descriptive[col_name]["Min"] < descriptive[col_name]["Lesser"]):
                lesser.append(col_name)
            if (descriptive[col_name]["Max"] > descriptive[col_name]["Greater"]):
                greater.append(col_name)       
        print(lesser)
        print(greater)
        return(lesser,greater)

    def col_99(self,quan,descriptive):
        lesser,greater=[],[]
        for col_name in quan:
            if (descriptive[col_name]["99%"] < descriptive[col_name]["median"]):
                lesser.append(col_name)
            if (descriptive[col_name]["Max"] > descriptive[col_name]["Greater"]):
                greater.append(col_name)       
        print(lesser)
        print(greater)
        return(lesser,greater)