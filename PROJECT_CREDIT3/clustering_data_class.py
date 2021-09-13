
from kneed import KneeLocator
from sklearn.cluster import KMeans
import pickle

class Clusterning_Data:
    
    def __init__(self,file_obj,logger_obj):
        
    
        self.file_obj = file_obj
        self.logger_obj = logger_obj
        
        
        self.logger_obj.log(self.file_obj,"\n Entered clustering_data class")
    def clustering(self,x):
        
        try:
            self.logger_obj.log(self.file_obj,"\n Entered clustering method in  clustering_data class")
            sse = []
            for i in range(1,10):
                kms = KMeans(n_clusters=i)
                kms.fit(x)
                sse.append(kms.inertia_)
            self.logger_obj.log(self.file_obj,"\n Kmeans inertia"+str(sse))

            kn = KneeLocator(range(1, 10), sse, curve='convex', direction='decreasing')

            kms = KMeans(n_clusters=kn.knee)
            kms.fit(x)
            cluster = kms.predict(x)
            x['cluster'] = cluster
            print(len(x.columns))
            
            #Saving KMeans model to Models folder
            self.logger_obj.log(self.file_obj,"\n Model for Clustering created successfully in  clustering_data class")
            file = open("models/Kmeans.pkl" , "wb")
            pickle.dump(kms,file)
            file.close
            self.logger_obj.log(self.file_obj,"\n Clustering done successfully in  clustering_data class")
            return x, kn.knee
        
        except Exception as e:
            self.logger_obj.log(self.file_obj,"\n Exception occured while Clustering  in  clustering_data class"+str(e))
            raise Exception()
            
            
            
            
            