import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)


source_node = glueContext.create_dynamic_frame.from_catalog(
    database = 'cloudtech-etl-glue-database',
    table_name = 'cloudtech_etl_source_bucket'
)


destination_node = glueContext.write_dynamic_frame.from_options(
    frame=source_node,
    connection_type="s3",
    format="json",
    connection_options={"path": "s3://cloudtech-etl-destination-bucket/transformed_data", "partitionKeys": []}
)

job.commit()
