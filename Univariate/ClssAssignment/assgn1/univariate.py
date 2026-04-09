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
    