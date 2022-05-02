import urllib.request
import json
import boto3
from datetime import datetime


# fecha y hora


def handler(event, context):

    print("Extrayendo bbc y cnn...")
    now = datetime.now()
    dataBBC = urllib.request.urlopen(
        "https://www.bbc.com/").read()

    dataCNN = urllib.request.urlopen(
        "https://www.cnn.com/").read()

    s3 = boto3.client("s3")

    s3.put_object(
        Body=(dataBBC),
        Bucket="proyecto02-punto01",
        Key="headlines/raw/periodico=bbc/year=" +
            str(now.year)+"/month="+str(now.month)+"/day="+str(now.day)
        + "/" + str(now.year) + "_" + str(now.month) + "_" + str(now.day) +
        "_"+str(format(now.hour))+"_" + str(format(now.minute))+"_"+"bbc.hmtl"
    )

    s3.put_object(
        Body=(dataCNN),
        Bucket="proyecto02-punto01",
        Key="headlines/raw/periodico=cnn/year=" +
            str(now.year)+"/month="+str(now.month)+"/day="+str(now.day)
        + "/" + str(now.year) + "_" + str(now.month) + "_" + str(now.day) +
        "_"+str(format(now.hour))+"_" + str(format(now.minute))+"_"+"cnn.html"
    )
    # print(data)
    return {}


handler(None, None)
