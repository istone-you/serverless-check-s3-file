import boto3
import os
from datetime import date, datetime, timedelta

def lambda_handler(event, context):

    # S3クライアントを作成する
    s3_client = boto3.client('s3')

    # バケット名を取得
    backet_name = os.environ["BUCKET_NAME"]

    # オブジェクトの接頭辞を取得
    objects_prefix = os.environ["OBJECT_PREFIX"]

    # 今の時間を取得
    now = datetime.now() + timedelta(hours=9)

    # 時間を文字列に変換(分まで)
    minutes_number = now.strftime("%Y%m%d%H%M")

    loop_count = int(os.environ["INVOKE_TIME_INTERVAL"]) + 1

    for i in range(2, loop_count):
        time = now - timedelta(minutes=i)

        time_number = time.strftime("%Y%m%d%H%M")
        # print(time_number)

        # オブジェクトのリストを取得する
        response = s3_client.list_objects_v2(Bucket=backet_name, Prefix=f"{objects_prefix}{time_number[0:8]}/{time_number}")

        try:
            # リストを最新順にソートする
            objects = sorted(response['Contents'], key=lambda obj: obj['LastModified'], reverse=True)

            # 最新の2つのオブジェクトのキーを取得する
            latest_objects = [obj['Key'] for obj in objects[:2]]
        except:
            # ファイルが存在しない場合エラーになります。
            raise Exception("ファイルが抜けています！")

    return ("ファイルは正常に作成されています！")



