from pyspark.sql import SparkSession

import sys
import time
import os

#Exercise: use what you have learned in the LoadingData.ipynb notebook to load a set of CSV datasets 
#and find movies where Tom Hanks played in

def main(args):
    start  = time.time()
 
    spark = SparkSession.builder.appName("LoadCsv").getOrCreate()
    delimiter = "|"

    #Load 3 csv files into spark dataframe   
    person_df = spark.read.options(header='true', inferschema='true',delimiter=delimiter).csv('/scratch/network/alexeys/BigDataCourse/csv/person_nodes.csv')
    movie_df = spark.read.options(header='true', inferschema='true',delimiter=delimiter).csv('/scratch/network/alexeys/BigDataCourse/csv/movie_nodes.csv')
    relationships_df = spark.read.options(header='true', inferschema='true',delimiter=delimiter).csv('/scratch/network/alexeys/BigDataCourse/csv/acted_in_rels.csv')

    #Prepare a linked dataset of people, movies and the roles for people who played in those movies
    df = person_df.join(relationships_df, person_df.id == relationships_df.person_id) 
    combined_df = df.join(movie_df,movie_df.id == df.movie_id)

    #Use where statement analogous to that in Pandas dataframes to find movies associated with name "Tom Hanks"
    answer = combined_df.where(combined_df.name == "Tom Hanks")

    #Return only actor name, movie title and roles
    print (answer.select('name','title','roles').show())

    #Save the answer in JSON format 
    answer.coalesce(1).select('name','title','roles').write.json(os.environ.get('SCRATCH_PATH')+"/json/")

    end = time.time()
    print ("Elapsed time: ", (end-start))


if __name__ == "__main__":
    main(sys.argv)
